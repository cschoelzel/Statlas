"""Anthropic-backed, resumable extraction with reserved-budget and exact-span gates.
Run: python -m navigator.extract --doc D069 --max-docs 1
Long corpus runs belong on gymscraper-act in a named tmux window.
"""
from __future__ import annotations
import argparse,datetime,hashlib,json,os,re,urllib.request,urllib.error
from pathlib import Path
from .sources import ROOT
MODEL='claude-haiku-4-5-20251001'
CATEGORIES=['rent_increase_limits','just_cause_eviction','security_deposits','application_screening_fees','screening_restrictions','algorithmic_rent_setting']
PROMPT='''Extract every distinct rental-housing legal obligation relevant to the six categories, including coverage, exemptions, preemption, sanctions, dates, bill status. Use only supplied document. Category identifiers exactly: rent_increase_limits,just_cause_eviction,security_deposits,application_screening_fees,screening_restrictions,algorithmic_rent_setting. Do not turn motions, bills, search snippets, or proposed ordinances into enacted law. Query date 2026-10-01. Preserve pending and failed. Uncertain status must be flagged. Return JSON object {"rules":[],"gaps":[]} only. Each rule needs jurisdiction (state CA/NJ/MA or City, ST), level state/city, category, status in_force/not_yet_effective/pending/failed, title, requirement, key_value string/null, coverage_conditions string/null, exemptions string/null, effective_date YYYY-MM-DD/null, citation, quoted_span EXACT contiguous source substring at least 20 characters, confidence, conflict_flag, conflict_note, sanctions, logic {coverage:expr,exemptions:expr}. DSL expr is boolean, {all:[expr]}, {any:[expr]}, {not:expr}, or {fact:name,op:eq/ne/lt/lte/gt/gte/in/not_in/exists,value:literal}. Coverage must include spatial condition legal_city or state; do not use jurisdiction as a fact. State fact is CA, NJ, or MA, legal_city fact is city name without state suffix. Use certificate_of_occupancy_date instead of construction year where statute requires occupancy. Unknown conditions use {fact:"unresolved_legal_condition_DOC_SECTION",op:"eq",value:true}; never assume true or false. Fact names should be descriptive snake_case. In exemptions false means no statutory exemptions; unknown exemptions require unresolved fact. Do not invent quantitative limits or fixed CPI. Include all operative sections, not just headline. Gaps identify missing cross-reference, historical status or text. No challenge tests are provided. Include evidence_json as a JSON array of {field,quoted_span} for every material field requirement, coverage_conditions, exemptions, effective_date, status, formula. Quotes must each be contiguous source substrings. If source does not establish condition/date mark unresolved, do not infer from retrieval. logic may additionally have formula using numeric literal {value:number,unit:USD/percent/scalar}, variable {fact:name,unit:USD/percent/scalar}, or arithmetic {op:min/max/add/sub/mul/div,args:[nodes]}. min/max/add/sub units must agree; mul one scalar factor; percentages are percent values not fractions. Example lesser CPI+5% or10% {op:min,args:[{op:add,args:[{fact:cpi_percent,unit:percent},{value:5,unit:percent}]},{value:10,unit:percent}]}. Variable CPI remains unknown until official CPI is provided. enacted_at, operative_date and end_date distinguish enactment, effective operation and sunset. conflicting dates temporal_conflict true in logic requires source review.'''
def secret():
    values={}
    p=ROOT/'.env'
    if p.exists():
        for line in p.read_text().splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                k,v=line.split('=',1);values[k.strip()]=v.strip().strip('\"\'')
    key=os.environ.get('ANTHROPIC_API_KEY') or values.get('ANTHROPIC_KEY') or values.get('ANTROPIC_KEY')
    if not key: raise RuntimeError('Anthropic key unavailable')
    return key

def api(path,payload=None):
    req=urllib.request.Request('https://api.anthropic.com/v1/'+path,data=json.dumps(payload).encode() if payload is not None else None,headers={'x-api-key':secret(),'anthropic-version':'2023-06-01','content-type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=55) as response:return json.load(response)
    except urllib.error.HTTPError as e:
        body=json.loads(e.read());raise RuntimeError('Anthropic HTTP %s: %s'%(e.code,body.get('error',{}).get('message','request failed'))) from None

def ledger():
    p=ROOT/'data/extraction_costs.json'
    return json.loads(p.read_text()) if p.exists() else {'budget_usd':25.0,'pricing':None,'calls':[]}

def save_ledger(v):
    p=ROOT/'data/extraction_costs.json';p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')

def reserve(input_tokens,max_output,doc_id,batch=False):
    v=ledger();price=v.get('model_prices',{}).get(MODEL) or v.get('pricing')
    if not price or not price.get('verified_source'):raise RuntimeError('Verified official pricing required in data/extraction_costs.json before paid calls')
    amount=(input_tokens*price['input_per_million']+max_output*price['output_per_million'])/1e6*(0.5 if batch else 1)
    spent=sum(c.get('actual_usd',c['reserved_usd']) for c in v['calls'])
    if spent+amount>v['budget_usd']:raise RuntimeError('Budget guard: requested reservation exceeds authorized budget')
    call={'doc_id':doc_id,'reserved_usd':round(amount,6),'model':MODEL,'input_per_million':price['input_per_million'],'output_per_million':price['output_per_million'],'batch':batch,'state':'reserved','at':datetime.datetime.now(datetime.timezone.utc).isoformat()};v['calls'].append(call);save_ledger(v);return len(v['calls'])-1

def settle(index,response):
    v=ledger();u=response.get('usage',{});c=v['calls'][index];p={'input_per_million':c.get('input_per_million',v['pricing']['input_per_million']),'output_per_million':c.get('output_per_million',v['pricing']['output_per_million'])};c.update(state='completed',usage=u,actual_usd=(u.get('input_tokens',0)*p['input_per_million']+u.get('output_tokens',0)*p['output_per_million'])/1e6*(0.5 if c.get('batch') else 1));save_ledger(v)

def valid_expr(e):
    if isinstance(e,bool):return True
    if not isinstance(e,dict):return False
    if set(e)=={'all'} or set(e)=={'any'}:
        return isinstance(next(iter(e.values())),list) and all(valid_expr(x) for x in next(iter(e.values())))
    if set(e)=={'not'}:return valid_expr(e['not'])
    return set(e).issubset({'fact','op','value'}) and bool(e.get('fact')) and e.get('op') in ['eq','ne','lt','lte','gt','gte','in','not_in','exists']

def validate(rule,source,text,ordinal):
    errors=[]
    for k in ['jurisdiction','level','category','status','title','requirement','citation','quoted_span']:
        if not rule.get(k):errors.append('missing '+k)
    if rule.get('category') not in CATEGORIES:errors.append('unsupported category')
    if rule.get('status') not in ['in_force','not_yet_effective','pending','failed']:errors.append('unsupported status')
    quote=rule.get('quoted_span','');start=text.find(quote) if len(quote)>=20 else -1
    if start<0 and len(quote)>=20:
        # Whitespace-only realignment recovers original contiguous bytes; no fuzzy paraphrase acceptance.
        pieces=re.split(r'\s+',quote.strip());pattern=r'\s+'.join(re.escape(x) for x in pieces)
        match=re.search(pattern,text)
        if match:
            start=match.start();rule['quote_alignment']='whitespace_only';quote=match.group();rule['quoted_span']=quote
    if start<0:errors.append('quoted_span is not exact original source substring')
    logic=rule.get('logic',{})
    if not valid_expr(logic.get('coverage')) or not valid_expr(logic.get('exemptions')):errors.append('invalid logic DSL')
    if errors:return None,errors
    span_evidence=[]
    for item in rule.get('field_evidence',[]):
        if not isinstance(item,dict):continue
        q=item.get('quoted_span','');m=re.search(r'\s+'.join(re.escape(x) for x in re.split(r'\s+',q.strip())),text) if len(q)>=20 else None
        if m:span_evidence.append({'field':item.get('field'),'quoted_span':m.group(),'start_char':m.start(),'end_char':m.end()})
    rule['field_evidence']=span_evidence
    supported={e['field'] for e in span_evidence}
    missing=[]
    for field in ['coverage_conditions','exemptions','effective_date']:
        if rule.get(field) and field not in supported:missing.append(field)
    if logic.get('formula') and 'formula' not in supported:missing.append('formula')
    if missing:
        rule['evidence_gaps']=missing
        # Facts cannot resolve source interpretation: this predicate forces an explicit legal review.
        logic['coverage']={'all':[logic['coverage'],{'fact':'unresolved_legal_evidence_'+source['doc_id']+'_'+str(ordinal),'op':'eq','value':True}]}
    if isinstance(logic.get('temporal_conflict'),bool):rule['temporal_conflict']=logic['temporal_conflict']
    rule.update(team_rule_id=f"{source['doc_id']}-r{ordinal:03d}",source_doc_id=source['doc_id'],source_url=source['url'],retrieved_at=source.get('retrieved_at'),query_date='2026-10-01',review_status='unreviewed',evidence={'source_doc_id':source['doc_id'],'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'start_char':start,'end_char':start+len(quote),'quoted_span':quote,'retrieved_at':source.get('retrieved_at'),'original_file':source.get('original_file')})
    return rule,[]

def payload_for(source,text,max_output=12000,claims=None):
    prompt=PROMPT.replace('logic {coverage:expr,exemptions:expr}', 'logic_json string containing JSON {coverage:expr,exemptions:expr}')
    props={k:{'type':'string'} for k in ['jurisdiction','level','category','status','title','requirement','citation','quoted_span','logic_json','evidence_json']}
    props['category']['enum']=CATEGORIES;props['status']['enum']=['in_force','not_yet_effective','pending','failed'];props['level']['enum']=['state','city']
    props.update({k:{'type':['string','null']} for k in ['key_value','coverage_conditions','exemptions','effective_date','conflict_note','sanctions','enacted_at','operative_date','end_date']})
    props.update(confidence={'type':'number'},conflict_flag={'type':'boolean'})
    schema={'type':'object','properties':{'rules':{'type':'array','items':{'type':'object','properties':props,'required':list(props),'additionalProperties':False}},'gaps':{'type':'array','items':{'type':'string'}}},'required':['rules','gaps'],'additionalProperties':False}
    return {'model':MODEL,'max_tokens':max_output,'system':prompt,'messages':[{'role':'user','content':json.dumps({'doc_id':source['doc_id'],'jurisdictions':source['jurisdictions'],'source_type':source['source_type'],'source':text,'cited_claims':claims})}],'output_config':{'format':{'type':'json_schema','schema':schema}}}

def citations_payload(source,text):
    return {'model':MODEL,'max_tokens':6000,'messages':[{'role':'user','content':[{'type':'document','source':{'type':'text','media_type':'text/plain','data':text},'title':source['doc_id'],'citations':{'enabled':True}},{'type':'text','text':'Identify every operative rental housing obligation and exemption across rent caps, just cause eviction, deposits, application/screening fees, screening restrictions, algorithmic pricing. Include status, dates, sanctions, coverage. Cite source for each claim. Distinguish proposed/failed from enacted. As of 2026-10-01. No external knowledge.'}]}]}

def cited_claims(source,text):
    payload=citations_payload(source,text)
    tokens=api('messages/count_tokens',{k:v for k,v in payload.items() if k!='max_tokens'})['input_tokens'];n=reserve(tokens,6000,source['doc_id']+':citations');response=api('messages',payload);settle(n,response)
    directory=ROOT/'data/extraction';directory.mkdir(exist_ok=True);(directory/(source['doc_id']+'.citations.response.json')).write_text(json.dumps(response,indent=2))
    if response.get('stop_reason')=='max_tokens':raise RuntimeError('Citations truncated; retry/split required')
    return response['content']

def extract(source,max_output=12000):
    text=(ROOT/source['text_file']).read_text();claims=cited_claims(source,text);payload=payload_for(source,text,max_output,claims)
    count=api('messages/count_tokens',{k:v for k,v in payload.items() if k!='max_tokens'})['input_tokens'];index=reserve(count,max_output,source['doc_id']);response=api('messages',payload);settle(index,response)
    return process_response(source,text,response)

def process_response(source,text,response):
    raw=''.join(x.get('text','') for x in response['content']);directory=ROOT/'data/extraction';directory.mkdir(exist_ok=True);(directory/(source['doc_id']+'.response.json')).write_text(json.dumps(response,indent=2))
    if response.get('stop_reason')=='max_tokens':raise RuntimeError('Truncated extraction retained; requires retry/split, never accepted')
    clean=re.sub(r'^```(?:json)?\s*|\s*```$','',raw.strip());result=json.loads(clean);accepted=[];rejected=[]
    for n,r in enumerate(result.get('rules',[]),1):
        try: r['logic']=json.loads(r.pop('logic_json'));r['field_evidence']=json.loads(r.pop('evidence_json'))
        except (ValueError,KeyError): r['logic']={}
        rule,errors=validate(r,source,text,n)
        if errors:rejected.append({'rule':r,'errors':errors})
        else:accepted.append(rule)
    artifact={'doc_id':source['doc_id'],'model':MODEL,'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'rules':accepted,'rejected':rejected,'gaps':result.get('gaps',[]),'status':'needs_review'};(directory/(source['doc_id']+'.json')).write_text(json.dumps(artifact,indent=2)+'\n');return artifact

def combine():
    artifacts=[json.loads(p.read_text()) for p in sorted((ROOT/'data/extraction').glob('D*.json')) if re.fullmatch(r'D\d+\.json',p.name)];rules=[r for a in artifacts for r in a['rules']];(ROOT/'data/rules.json').write_text(json.dumps(rules,indent=2)+'\n');return rules

def submit_batch(stage='citations',limit=100):
    index=json.loads((ROOT/'data/sources/index.json').read_text());requests=[];mapping={};directory=ROOT/'data/extraction';directory.mkdir(exist_ok=True)
    for source in index:
        doc=source['doc_id']
        if source['status']!='full_text_ready' or not source.get('text_file') or (directory/(doc+'.json')).exists():continue
        text=(ROOT/source['text_file']).read_text()
        if stage=='citations':
            if (directory/(doc+'.citations.response.json')).exists():continue
            params=citations_payload(source,text)
        else:
            citation_file=directory/(doc+'.citations.response.json')
            if not citation_file.exists():continue
            claims=json.loads(citation_file.read_text())
            if claims.get('stop_reason')=='max_tokens':continue
            params=payload_for(source,text,16000,claims['content'])
        # Safe conservative upper bound; tokenizer-count endpoint is unnecessary for each batch member.
        # One token per UTF-8 byte plus 2048 schema overhead exceeds ordinary English token count.
        estimate=len(json.dumps(params).encode())+2048
        n=reserve(estimate,params['max_tokens'],doc+':'+stage,batch=True)
        requests.append({'custom_id':doc,'params':params});mapping[doc]=n
        if len(requests)>=limit:break
    if not requests:return {'status':'nothing_to_submit'}
    result=api('messages/batches',{'requests':requests});result.update(stage=stage,ledger_indices=mapping);(directory/('batch-'+result['id']+'.json')).write_text(json.dumps(result,indent=2));return {'batch_id':result['id'],'stage':stage,'requests':len(requests)}

def poll_batch(batch_id):
    directory=ROOT/'data/extraction';p=directory/('batch-'+batch_id+'.json');saved=json.loads(p.read_text());status=api('messages/batches/'+batch_id)
    if status['processing_status']!='ended':return status
    req=urllib.request.Request(status['results_url'],headers={'x-api-key':secret(),'anthropic-version':'2023-06-01'})
    with urllib.request.urlopen(req,timeout=55) as response:lines=response.read().decode().splitlines()
    sources={s['doc_id']:s for s in json.loads((ROOT/'data/sources/index.json').read_text())};summary={'succeeded':0,'failed':[]}
    for line in lines:
        entry=json.loads(line);doc=entry['custom_id'];result=entry['result']
        if result['type']!='succeeded':summary['failed'].append({'doc_id':doc,'type':result['type']});continue
        message=result['message'];settle(saved['ledger_indices'][doc],message)
        if saved['stage']=='citations':(directory/(doc+'.citations.response.json')).write_text(json.dumps(message,indent=2))
        else:
            try:process_response(sources[doc],(ROOT/sources[doc]['text_file']).read_text(),message)
            except (ValueError,RuntimeError) as e:summary['failed'].append({'doc_id':doc,'reason':str(e)})
        summary['succeeded']+=1
    saved.update(status=status,results=summary,downloaded=True);p.write_text(json.dumps(saved,indent=2));combine();return summary

def main():
    global MODEL
    p=argparse.ArgumentParser();p.add_argument('--doc');p.add_argument('--max-docs',type=int,default=1);p.add_argument('--combine',action='store_true');p.add_argument('--batch-stage',choices=['citations','structure']);p.add_argument('--poll');p.add_argument('--model',default=MODEL);a=p.parse_args()
    MODEL=a.model
    if a.batch_stage:print(json.dumps(submit_batch(a.batch_stage,a.max_docs)));return
    if a.poll:print(json.dumps(poll_batch(a.poll)));return
    if a.combine:print(json.dumps({'rules':len(combine())}));return
    index=json.loads((ROOT/'data/sources/index.json').read_text());todo=[s for s in index if s['text_file'] and s['status']=='full_text_ready' and (not a.doc or s['doc_id']==a.doc) and not (ROOT/'data/extraction'/ (s['doc_id']+'.json')).exists()]
    for s in todo[:a.max_docs]:
        result=extract(s);print(json.dumps({'doc_id':s['doc_id'],'accepted':len(result['rules']),'rejected':len(result['rejected'])}),flush=True)
    combine()
if __name__=='__main__':main()
