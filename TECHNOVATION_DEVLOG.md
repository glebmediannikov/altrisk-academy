# Technovation 2027 — Development Log

## Baseline
- Repository: `glebmediannikov/altrisk-academy`
- Development branch: `technovation-2027`
- Baseline: record the exact `main` commit SHA and date before merging any new changes.
- Production deployment: unchanged.

## Proposed change 01 — Assessment prototype (not yet integrated)
- Goal: compare student knowledge before and after a financial-risk lesson.
- Files: `question_bank.py`, `learning_assessment.py`, `tests/test_learning_assessment.py`.
- Status: AI-assisted prototype prepared for Maria's review; not a validated research instrument.
- Limitations: six paired questions per form; equivalence and educational validity not established; no participant tracking; no causal claims.
- Privacy: no names, emails, identifiers, network calls, or persistent data collection in these files.
- Next: Maria reviews each question, explains and edits the scoring logic, educator checks content, then conducts an approved pilot.

## November 7, 2026 — Learning Assessment integration
- Integrated an optional six-question pre-test and post-test into the existing sidebar and deep-link navigation, using the existing scoring and percentage-point change helpers.
- Files modified: `app.py`, `assessment_ui.py` (pre-existing untracked interface extended for integration), `tests/test_navigation.py`, `README.md`, and `TECHNOVATION_DEVLOG.md`. Added `tests/test_assessment_ui.py`. The question bank and scoring helpers were not modified.
- Tests: `.\.venv\Scripts\python.exe -m pytest tests/ -v` — 33 passed. `.\.venv\Scripts\python.exe -m compileall -q app.py assessment_ui.py learning_assessment.py question_bank.py` — passed.
- Privacy: assessment results are held in Streamlit session state only; no student identifiers, database, analytics, or external API calls were added.
- Limitations: the prototype questions have not been educationally validated or tested for equivalent difficulty. A score change cannot establish educational effectiveness or causation. Lab completion is encouraged but not enforced; the post-test requires a completed pre-test. Assessment results are lost when the session ends.
- GitHub Copilot assisted with implementation, automated tests, and documentation. No student or educator validation is claimed.

## Entry template for future work
- Date:
- Author / contributor:
- Problem observed (include evidence):
- Change implemented:
- Tests run and results:
- Student/educator feedback:
- AI tools used and exactly how:
- Maria's independent decisions and modifications:
- Commit / PR link:

## Competition integrity
Document AI assistance accurately and follow the current Technovation Honor Code. Do not represent AI-generated code as independently authored or claim student research results before they exist.
