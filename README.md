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
2. Upload `app.py`, `requirements.txt`, and this `README.md` to the repository root.
3. Sign in at https://share.streamlit.io/ with GitHub.
4. Choose **Create app**, select the repository and branch, set main file path to `app.py`, and deploy.
5. Open the resulting URL and test all three scenarios on desktop and mobile.

No secrets or external APIs required. Progress is stored in Streamlit session state and resets if the session ends; no personal data is collected or persisted.

## Modules
- **Your First $1,000**: budget allocation, emergency event and market scenario.
- **Life Happens**: decisions over three rounds, with liquidity and debt trade-offs.
- **Investment Risk Lab**: compare portfolio mixes across hypothetical market conditions.
- **Dashboard**: lesson progress, achievements, score breakdown, and CSV learning report.

## Scoring
Scores reward reasoning and preparedness, not maximizing investment returns. Each module awards 0–100 points according to explicit rules in the code. These are illustrative learning heuristics, not validated assessments or personalized financial advice.

## Before competition submission
Maria should review, test, and understand all code and calculations; verify competition eligibility and disclosure requirements; document her own changes and user testing. This is a newly authored educational MVP; the original AltRisk code is not reused.
