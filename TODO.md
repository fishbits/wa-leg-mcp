# TODO

## Bugs

- [ ] Roll call API not returning individual vote values for older bills (pre-?? biennium). Need to investigate which bienniums are affected and whether this is an upstream WSLWS API limitation or a parsing issue in `roll_call_tools.py`.

## Coverage

- [ ] `governor_action_tools.py` — 0% unit test coverage
- [ ] `session_law_tools.py` — 0% unit test coverage
- [ ] `committee_action_tools.py` — 0% unit test coverage
- [ ] `enhanced_committee_tools.py` — 64% coverage (property tests help, but unit tests missing for several code paths)
- [ ] Overall goal: push from 61% toward 80%+
