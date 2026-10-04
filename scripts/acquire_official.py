"""Single targeted official-source retrieval; never infer historical validity."""
import sys, urllib.request
from datetime import datetime,timezone
from html.parser import HTMLParser
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from navigator.sources import retain_acquisition,build_inventory
class Parser(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.skip=0
    def handle_starttag(self,t,a):
        if t in ('script','style'):self.skip+=1
    def handle_endtag(self,t):
        if t in ('script','style'):self.skip=max(0,self.skip-1)
        if t in ('p','div','br','li'):self.parts.append('\n')
    def handle_data(self,d):
        if not self.skip:self.parts.append(d)
if __name__=='__main__':
    doc_id,url=sys.argv[1:]
    if not any(url.startswith(x) for x in ['https://leginfo.legislature.ca.gov/','https://malegislature.gov/','https://www.njleg.state.nj.us/']):
        raise SystemExit('Only approved official LegInfo endpoint supported')
    b=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=4).read()
    p=Parser();p.feed(b.decode())
    t='\n'.join(x.strip() for x in ''.join(p.parts).splitlines() if x.strip())
    r=retain_acquisition(doc_id,b,url,datetime.now(timezone.utc).isoformat(),t,'stdlib-htmlparser-v1')
    build_inventory()
    print(doc_id,'retained',len(t),'text characters')
