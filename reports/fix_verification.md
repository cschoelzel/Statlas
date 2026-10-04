# Fresh independent interpreter verification

2026-10-03. Frozen engine SHA256 at first verification: `b4d84511f18a48d4e71c752b883411c77a568ee90c5a95cc2778baa18e251bba`. Scope: deterministic logic only. No legal gold labels, no source or reference accuracy certification. The provided objective file ends at §5.2; no §§7–12 were present. Used architecture, conservative decisions, targeted questions, reproducible evidence, and independent-review requirements actually provided, plus challenge README §§7–9.

Phase 1 formed without implementation explanations or earlier review reports. `python3 -m unittest tests.test_engine -q`: 38 existing tests passed (the combined earlier command with redteam ran 44 tests, one failure). Independent test file: `python3 -m unittest tests.test_fix_independent -q`: 9 methods, 6 pass / 3 fail; nested truth-table method exercises 27 combinations, counted as one method. Runtime 0.002s. No output result is a legal answer verification.

## Confirmed findings

1. **P1 / conflict safety:** `navigator/engine.py:evaluate_rules`. Two initially applicable rules A and B with evidenced A→B and B→A supersedes edges both become `superseded`; neither conflict flag nor review is set. Minimum input is `test_supersession_cycle_requires_review` in the independent file. Expected: unresolved cycle retained and marked for review, not simultaneous suppression of every operative candidate. Actual: both suppressed. Source of expected behavior: explicit requirement to flag conflicts and avoid invented operative conclusions; a cycle provides no consistent precedence. Permanent regression: same named test, plus 3-cycle and acyclic attached rule.

2. **P1 / malformed logic conservative evaluation:** `evaluate_condition({'all': [], 'any': [False]}, {})` gives `(True, set())`, because first matching operator wins. Expected unknown with source review: conflicting multiple top-level operators have no unambiguous executable meaning. This can create an affirmative application from malformed extraction. Permanent regression: `test_ambiguous_condition_fails_closed`, additionally all+not and fact+all combinations. Confirmed interpreter defect; exposure in current rule corpus not established.

3. **P2 / typed date operator consistency:** date `ne` comparison with actual `2026-10-02` and expected `2026-10-01` gives `(None, {'date'})`. Expected True from non-overlapping exact dates; numeric `ne` exists. For partial overlapping dates expected unknown. Permanent regression: `test_exact_date_not_equal`. Confirmed incomplete supported comparison rather than false affirmative application.

## Reverified fixed behaviors

Missing translation and malformed logic objects return unknown. Nested all/any truth tables drop irrelevant questions. Month precision strictly before exact cutoff is true; overlapping year is unknown. Operative/effective disagreement is conservatively unknown and marked review. Nonfinite, oversized numeric literals, malformed formula args return diagnostics. Acyclic supersession is order independent. These are synthetic behavioral checks only.

## Phase 2: previous failing tests

Then read `tests/test_redteam.py`. The prior operative-date test expects `not_yet_effective` for distinct effective and operative dates. Current engine returns unknown with a source conflict review. This is an acceptable conservative interpretation of an ambiguous generic input, not proof that the effective date alias failed. The fresh test explicitly locks that conservative behavior. The six earlier redteam methods otherwise pass; initial combined command reports 44 methods and one failure. Do not relabel that suite as green without updating the expectation or defining operative-date precedence in the input contract.

Critical residual conflict-cycle and malformed-expression findings prevent a clean interpreter release until fixed and independently rerun. Geography, actual legal source completeness, extraction correctness, and change-test gold expectations are outside this verification.
