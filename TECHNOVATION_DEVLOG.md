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

## November 7, 2026 — Adaptive Feedback Engine (V2.0.2)
- Added deterministic topic recommendations with explanations, hypothetical numerical examples, and links to existing labs. Topics with wrong answers are ordered by lowest fraction correct, then alphabetically. The pre-test path is replaced by the post-test path; students need not complete all labs.
- Chose explicit rules for transparency and reproducibility. The answer-level engine identifies wrong and unanswered questions separately, excludes unanswered items from topic percentages, and rejects invalid choices. The UI derives recommendations from existing completed topic scores, with no additional answer storage.
- Motivation: the reported 50-student needs survey found low financial confidence in 25/50 (50%), low diversification understanding in 27/50 (54%), low confidence comparing risk in 27/50 (54%), a lack of practical examples as the main obstacle for 19/50 (38%), and strong interest in a simulator in 30/50 (60%). These descriptive findings do not establish educational effectiveness or represent all high school students.
- Files added: `adaptive_feedback.py`, `tests/test_adaptive_feedback.py`. Files modified: `app.py`, `assessment_ui.py`, `tests/test_assessment_ui.py`, `README.md`, and `TECHNOVATION_DEVLOG.md`.
- Tests: `.\.venv\Scripts\python.exe -m pytest tests/ -v` — 51 passed. `.\.venv\Scripts\python.exe -m compileall -q app.py assessment_ui.py adaptive_feedback.py learning_assessment.py question_bank.py` — passed. A local Streamlit agent-API smoke test submitted a pre-test and navigated to a recommended lab; AppTest covers all four final topic-to-lab routes. The existing Investment Risk Lab emitted Streamlit `use_container_width` deprecation warnings during the smoke test.
- Privacy: no identifiers, database, analytics, external API, or persistent assessment storage added. Recommendations are derived in memory from session results.
- Limitations: the questions and recommendations are not educationally validated; examples are hypothetical, not forecasts or financial advice. Score changes do not prove learning or causation. The sample is not evidence of population representativeness. No student testing of the new feature is claimed.
- GitHub Copilot assisted with implementation, tests, and documentation.

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
