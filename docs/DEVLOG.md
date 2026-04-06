# Development Log

## 2026-04-06 — README Refresh & Project Status

**What was done:**
- Installed `hypothesis` — all 444 tests passing (331 unit + 113 property), 61% coverage
- Created `TODO.md` tracking known issues and coverage goals
- Rewrote `README.md` (842 → 125 lines) for portfolio/LinkedIn readiness
- Extracted full API reference to `docs/API.md`
- Merged and pushed to `main` on `fishbits/wa-leg-mcp`
- LinkedIn post published

**Where to pick up next:**

1. **Bug — Roll call vote values missing for older bills**
   - `roll_call_tools.py` — API not returning individual vote values for older bienniums
   - Need to compare raw API responses (old vs. recent bill) to determine if it's upstream WSLWS or a parsing issue
   - Tracked in `TODO.md`

2. **Coverage gaps** (currently 61%, goal 80%+)
   - `governor_action_tools.py` — 0%
   - `session_law_tools.py` — 0%
   - `committee_action_tools.py` — 0%
   - `enhanced_committee_tools.py` — 64%
   - `sponsor_tools.py` — 73%
   - `passage_tools.py` — 77%
   - All tracked in `TODO.md`

3. **Branch cleanup** — `initial-local-changes` is fully superseded by `main` (keeping for now, safe to delete later)
