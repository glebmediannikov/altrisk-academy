# AltRisk Academy — Financial Decision-Making Lab

Independent educational FinTech MVP built with Python and Streamlit. All scenarios are hypothetical, educational, and use virtual money.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Create a **new** GitHub repository named `altrisk-academy` (do not overwrite the existing AltRisk project).
2. Upload the complete application repository, including its Python modules and assets.
3. Sign in at https://share.streamlit.io/ with GitHub.
4. Choose **Create app**, select the repository and branch, set main file path to `app.py`, and deploy.
5. Open the resulting URL and test the labs and assessment on desktop and mobile.

No secrets or external APIs required. Progress is stored in Streamlit session state and resets if the session ends; no personal data is collected or persisted.

## Modules
- **Your First $1,000**: budget allocation, emergency event and market scenario.
- **Life Happens**: decisions over three rounds, with liquidity and debt trade-offs.
- **Investment Risk Lab**: compare portfolio mixes across hypothetical market conditions.
- **Green Investing Lab** and **Responsible Consumption Lab**: explore environmental decisions.
- **Learning Assessment**: take a six-question pre-test and post-test, then compare scores and topic feedback. This prototype is not a validated educational instrument; score changes do not demonstrate educational effectiveness. Results remain in the current Streamlit session only.
- **Dashboard**: lesson progress, achievements, score breakdown, and CSV learning report.

## Personalized learning path
After each completed assessment, the app recommends practice for topics with incorrect answers, ordered by the lowest proportion correct; ties are alphabetical. Each recommendation includes an explanation, a hypothetical example, and a button to an existing lab. The post-test replaces the pre-test recommendations with its own; completing all labs is not required.

The deterministic rules were chosen to make recommendations transparent and reproducible, without an AI service or machine-learning model. The answer-level engine reports unanswered items separately and excludes them from topic percentages; invalid choices are rejected. The assessment UI requires every answer before submitting. Only assessment results in the current session are used; no identifiers or persistent assessment records are collected.

The feature was motivated by a reported needs-assessment survey of 50 high school students: 25/50 (50%) reported low financial confidence, 27/50 (54%) low understanding of diversification, 27/50 (54%) low confidence comparing risks, 19/50 (38%) cited lack of practical examples as the main obstacle, and 30/50 (60%) expressed strong interest in an interactive simulator. These descriptive findings do not establish effectiveness or represent all high school students. The questions, recommendations, and examples are prototypes, not validated measures or financial advice; score changes do not establish causation or educational impact.

On November 7, 2026, the automated suite passed 51 tests and the requested Python compile check passed. GitHub Copilot assisted with the adaptive feedback implementation, tests, and documentation; no student testing of this feature is claimed.

## Scoring
Scores reward reasoning and preparedness, not maximizing investment returns. Each module awards 0–100 points according to explicit rules in the code. These are illustrative learning heuristics, not validated assessments or personalized financial advice.

## Before competition submission
Maria should review, test, and understand all code and calculations; verify competition eligibility and disclosure requirements; document her own changes and user testing. This is a newly authored educational MVP; the original AltRisk code is not reused.
