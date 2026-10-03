# Challenge package discrepancies

The supplied files remain unchanged.

- The supplied effective_date regex escapes the digit class twice. data/rule_record.corrected.schema.json corrects only that escaping; normal ISO dates otherwise fail the supplied pattern. Both validation outcomes must be reported.
- README describes rules.json as a list; the template wraps records in {"rules": [...]}. Export rules.json as a list and provide rules.wrapped.json for template consumers.
- The PDF requires penalties and a one-page method note. Preserve penalty metadata and supply the note. Extra fields are permitted by the record schema.
- Retrieval date is required in prose but absent from schema. Include retrieved_at and provenance as additional fields.
- A+B is an emergency README minimum; full goal remains A+B+C.
- Template lookup A0001 gives an NJ example although the actual address is in California; templates are examples, not reference labels.
- Corpus publisher terms and source historical validity are separate from technical retrieval success.
