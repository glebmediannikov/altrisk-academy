"""AltRisk Academy: standalone financial decision-making educational MVP."""
import io
import csv
from pathlib import Path
import streamlit as st

from climate_labs import green_investing, responsible_consumption

LOGO_PATH = Path(__file__).parent / "assets" / "logo.png"
st.set_page_config(page_title="AltRisk Academy", page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "🎓", layout="wide")

st.markdown("""<style>
.stApp {background: #f6f8fc; color: #15253c;}
.block-container {max-width: 1180px; padding-top: 2rem;}
h1,h2,h3 {color:#142747 !important;}
[data-testid="stMetric"] {background:white; border:1px solid #e2e9f3; padding:14px; border-radius:14px;}
div.stButton > button[kind="primary"] {background:#2457d6; border-radius:10px;}
.hero {background:linear-gradient(115deg,#142d59,#225fbb);color:white;padding:26px;border-radius:18px;margin-bottom:18px;}
.hero h1 {color:white !important;margin:0;}
.hero p {color:#e2edff;margin:7px 0 0;}
.small {color:#53647b;font-size:0.9rem;}
</style>""", unsafe_allow_html=True)

MODULES = [
    "Your First $1,000",
    "Life Happens",
    "Investment Risk Lab",
    "Green Investing Lab",
    "Responsible Consumption Lab",
]
if "scores" not in st.session_state:
    st.session_state.scores = {}
if "round" not in st.session_state:
    st.session_state.round = 0
if "life" not in st.session_state:
    st.session_state.life = {"cash": 500, "debt": 0, "history": []}


def save_score(name, score, lesson):
    st.session_state.scores[name] = {"score": int(max(0, min(100, score))), "lesson": lesson}


def achievements():
    scores = st.session_state.scores
    badges = []
    if scores:
        badges.append("🌱 First Steps — completed a learning lab")
    if "Your First $1,000" in scores and scores["Your First $1,000"]["score"] >= 70:
        badges.append("🛟 Safety Net — planned for emergencies")
    if "Life Happens" in scores:
        badges.append("🧭 Resilience Explorer — navigated life's surprises")
    if "Investment Risk Lab" in scores:
        badges.append("📊 Risk Detective — compared uncertainty")
    if len(scores) == len(MODULES):
        badges.append("🏆 Financial Explorer — completed all labs")
    return badges


def report_csv():
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["Module", "Score (0-100)", "Learning feedback"])
    for name in MODULES:
        if name in st.session_state.scores:
            item = st.session_state.scores[name]
            writer.writerow([name, item["score"], item["lesson"]])
    return buffer.getvalue().encode("utf-8")


GLOSSARY = {
    "Learning score": "An educational score (0–100) based on simplified rules in this activity. It does not measure financial ability or predict future performance.",
    "Emergency savings": "Money kept readily accessible for unexpected necessary expenses, such as repairs or urgent travel.",
    "Investments": "Money placed into assets that may increase or decrease in value. Unlike cash savings, investment value can fluctuate.",
    "Market return": "The percentage change in an investment's value over a period. Negative returns mean a loss.",
    "Liquidity": "How quickly and easily an asset can be converted into spendable cash without a large loss.",
    "Opportunity cost": "The benefit you give up when you choose one option instead of another.",
    "Debt": "Money owed to another party. Borrowing often adds interest or fees to the amount to repay.",
    "Volatile assets": "Assets whose prices can rise or fall sharply. They have greater price uncertainty in this simplified model.",
    "Lower-volatility assets": "Assets modeled with smaller price movements. Lower volatility does not mean risk-free.",
    "Asset allocation": "How you divide investments among different asset types, such as stocks, bonds, or cash.",
    "Downturn": "A scenario in which market prices fall.",
    "Time horizon": "How long you expect to keep money invested before you need to use it.",
    "Diversification": "Spreading investments across different assets to reduce concentration risk. It cannot eliminate all losses.",
    "Uncovered expense": "The portion of a necessary cost that remains unpaid after available savings and modeled investment proceeds are used.",
    "Achievements": "Badges unlocked by completing specific learning activities. They are motivational, not professional credentials.",
}
def term(name):
    with st.popover("❔", help=f"Definition: {name}"):
        st.markdown(f"**{name}**")
        st.write(GLOSSARY[name])

def guide(steps, takeaway):
    with st.container(border=True):
        st.markdown("#### 🧭 How to use this page")
        for i, step in enumerate(steps, 1):
            st.write(f"**{i}.** {step}")
        st.info(f"**What you'll learn:** {takeaway}")

# Support direct links from the AltRisk Academy website, for example:
# https://altrisk-academy.streamlit.app/?lab=green-investing
LAB_SLUGS = {
    "green-investing": "Green Investing Lab",
    "responsible-consumption": "Responsible Consumption Lab",
}
PAGE_TO_SLUG = {name: slug for slug, name in LAB_SLUGS.items()}
NAV_PAGES = ["Dashboard"] + MODULES


def sync_page_query():
    """Keep the URL aligned with a manual sidebar selection."""
    selected = st.session_state.academy_page
    slug = PAGE_TO_SLUG.get(selected)
    if slug:
        st.query_params["lab"] = slug
    elif "lab" in st.query_params:
        del st.query_params["lab"]


# Initialize page selection once. Query parameters take priority for new sessions.
if "academy_page" not in st.session_state:
    requested_page = LAB_SLUGS.get(st.query_params.get("lab", ""), "Dashboard")
    st.session_state.academy_page = requested_page

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=155)
    st.markdown("## AltRisk Academy")
    page = st.radio(
        "Explore", NAV_PAGES, key="academy_page",
        on_change=sync_page_query, label_visibility="collapsed",
    )
    st.divider()
    st.caption("Virtual money • Educational simulations • No account required")
    st.caption("Scores are learning prompts, not financial or psychological assessments.")

if page == "Dashboard":
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=170)
    st.markdown('<div class="hero"><h1>Financial Decision-Making Lab</h1><p>Learn. Experiment. Decide with Confidence.</p></div>', unsafe_allow_html=True)
    st.write("Explore real-life trade-offs using virtual money. Try each lab, review your decisions, and learn why uncertainty matters.")
    guide([
        "Choose a learning lab from the left sidebar.",
        "Read the scenario and adjust the interactive controls to test decisions.",
        "Finish the lab to record your educational score.",
        "Return here to review progress, badges, and download your learning report."
    ], "Understand trade-offs between spending, saving, borrowing, and investing.")
    completed = len(st.session_state.scores)
    average = round(sum(v["score"] for v in st.session_state.scores.values()) / completed) if completed else 0
    a, b, c = st.columns(3)
    a.metric("Labs completed", f"{completed}/{len(MODULES)}")
    b.metric("Average learning score", f"{average}/100" if completed else "—")
    c.metric("Achievements", len(achievements()))
    st.progress(completed / len(MODULES))
    st.markdown("**Key terms**")
    c1,c2 = st.columns(2)
    with c1:
        st.write("Learning score"); term("Learning score")
    with c2:
        st.write("Achievements"); term("Achievements")
    st.subheader("Learning pathways")
    for name, description in [
        (MODULES[0], "Balance spending, emergency savings, and investing."),
        (MODULES[1], "Navigate three unexpected financial choices."),
        (MODULES[2], "Compare different portfolio mixes and market outcomes."),
        (MODULES[3], "Build a green investment portfolio."),
        (MODULES[4], "Explore sustainable everyday decisions."),
    ]:
        with st.container(border=True):
            st.markdown(f"**{name}** {'✅' if name in st.session_state.scores else '○'}")
            st.write(description)
            if name in st.session_state.scores:
                st.caption(f"Learning score: {st.session_state.scores[name]['score']}/100")
    st.subheader("Achievements")
    if achievements():
        for badge in achievements():
            st.write(badge)
    else:
        st.info("Complete your first lab to unlock an achievement.")
    if completed:
        st.download_button("⬇ Download learning report (CSV)", report_csv(), "altrisk_academy_learning_report.csv", "text/csv")
    st.caption("Progress lasts only for this browser session. No account or cloud database is used.")

elif page == MODULES[0]:
    st.title("💵 Your First $1,000")
    st.write("You receive $1,000 in virtual money. Decide what to spend, save, and invest before unexpected events occur.")
    guide([
        "Use the first slider to choose how much to spend immediately.",
        "Use the second slider to set aside cash for emergencies; the remainder is invested automatically.",
        "Choose an unexpected expense and a hypothetical market movement.",
        "Compare the remaining savings and investments, read the explanation, then click Finish lab."
    ], "Learn why emergency reserves and liquidity can matter as much as potential returns.")
    st.markdown("#### Step 1 · Build your financial plan")
    spending = st.slider("Money for current spending ($)", 0, 1000, 200, 50,
        help="Virtual money used immediately. In this model, spending is consumed and cannot cover a later emergency.")
    saving = st.slider("Emergency savings ($)", 0, 1000-spending, min(400, 1000-spending), 50,
        help=GLOSSARY["Emergency savings"])
    st.caption("❔ Terms: Emergency savings and investments")
    a_help,b_help=st.columns(2)
    with a_help: term("Emergency savings")
    with b_help: term("Investments")
    investing = 1000-spending-saving
    x,y,z = st.columns(3)
    x.metric("Spending", f"${spending:,}")
    y.metric("Emergency savings", f"${saving:,}")
    z.metric("Investments", f"${investing:,}")
    st.divider()
    st.markdown("#### Step 2 · Test an unexpected event")
    st.write("What happens if an urgent bill arrives? The simulator uses emergency savings first.")
    event_options = {
        0: "No emergency — $0",
        300: "Laptop repair — $300",
        600: "Major unexpected expense — $600",
        120: "Bicycle tire and brake repair — $120",
        180: "Urgent dental visit — $180",
        250: "Phone replacement — $250",
        450: "Emergency trip to visit family — $450",
        800: "Unexpected housing expense — $800",
    }
    emergency = st.selectbox(
        "Unexpected event",
        list(event_options),
        format_func=lambda value: event_options[value],
        help="Choose one fictional event to test. The amounts are illustrative and are not actual cost estimates."
    )
    st.caption("Try a different event to see whether your emergency savings still cover the bill.")
    st.markdown("#### Step 3 · Explore market uncertainty")
    st.write("Move the slider to see how an investment gain or loss changes your available funds.")
    term("Market return")
    change = st.select_slider("Hypothetical market return", options=[-20,-10,0,5,10], value=-10, format_func=lambda n:f"{n:+d}%",
        help=GLOSSARY["Market return"])
    invested_after_market = investing*(1+change/100)
    savings_used = min(saving, emergency)
    shortfall = emergency-savings_used
    sold = min(invested_after_market, shortfall)
    unmet = max(0, shortfall-invested_after_market)
    remaining_savings = saving-savings_used
    remaining_investments = invested_after_market-sold
    st.subheader("Step 4 · What happened?")
    st.write("Savings remaining is the cash you still have. Investments remaining is the modeled value after any necessary sale. Uncovered expense is the bill you still cannot pay.")
    term("Uncovered expense")
    term("Liquidity")
    x,y,z = st.columns(3)
    x.metric("Savings remaining", f"${remaining_savings:,.2f}")
    y.metric("Investments remaining", f"${remaining_investments:,.2f}")
    z.metric("Uncovered expense", f"${unmet:,.2f}")
    st.caption("Assumption: the emergency is paid from savings first, then by selling investments after the selected market move. Spending is treated as consumed. No fees or taxes.")
    score = round(max(0, min(100, 35 + 45*(min(saving,emergency)/max(1,emergency)) + 20*(1 if unmet==0 else 0) - (10 if investing>0 and sold>0 and change<0 else 0)))) if emergency else round(60+min(40,saving/10))
    if unmet > 0:
        lesson = "This plan could not cover the full emergency. Consider a larger accessible cash reserve."
    elif sold > 0:
        lesson = "The emergency required selling investments. Liquidity matters when markets fluctuate."
    else:
        lesson = "Emergency savings protected your investments. Balance liquidity with other goals."
    st.info(lesson)
    if st.button("Finish lab & save learning score", type="primary"):
        save_score(MODULES[0], score, lesson)
        st.success(f"Lab complete! Learning score: {score}/100. Return to Dashboard to see your achievement.")

elif page == MODULES[1]:
    st.title("🌦️ Life Happens")
    st.write("Navigate three financial events. Your starting emergency cash is $500. Debt carries a simplified 10% fee each round; this is a teaching assumption, not a loan quote.")
    guide([
        "Read each event carefully and consider whether the cost is essential or optional.",
        "Choose an action. If you decide to pay, select cash or borrowing.",
        "Confirm the decision to move to the next round. Cash and debt carry over.",
        "After three rounds, review your choices and finish the lab to save your score."
    ], "Practice weighing liquidity, borrowing costs, and opportunity costs.")
    st.markdown("**Terms to know**")
    g1,g2,g3=st.columns(3)
    with g1: term("Debt")
    with g2: term("Liquidity")
    with g3: term("Opportunity cost")
    st.warning("Teaching simplification: a 10% fee is added to the outstanding debt after every round. This is not an actual lending rate.")
    events = [
        ("Your phone needs a $200 repair.", 200, "Repair now", "Delay the repair"),
        ("You are offered a $150 training course.", 150, "Pay for the course", "Skip the course"),
        ("An urgent $350 travel expense appears.", 350, "Cover the travel expense", "Ask for a payment plan"),
    ]
    round_index = st.session_state.round
    life = st.session_state.life
    st.progress(round_index/3)
    a,b = st.columns(2)
    a.metric("Cash", f"${life['cash']:.2f}")
    b.metric("Outstanding debt", f"${life['debt']:.2f}")
    if round_index < 3:
        title, amount, option_a, option_b = events[round_index]
        st.subheader(f"Round {round_index+1}: {title}")
        st.caption("Think about urgency, the cash you need later, and the cost of borrowing before confirming.")
        choice = st.radio("Choose your response", [option_a, option_b], key=f"life_choice_{round_index}")
        if choice == option_a:
            funding = st.radio("How would you fund it?", ["Use available cash first", "Borrow the full amount"], key=f"funding_{round_index}")
        else:
            funding = None
        if st.button("Confirm decision", type="primary"):
            if choice == option_a:
                cash_used = min(life["cash"], amount) if funding == "Use available cash first" else 0
                life["cash"] -= cash_used
                life["debt"] += amount-cash_used
                feedback = f"You chose to pay ${amount}. Cash used: ${cash_used}; new borrowing: ${amount-cash_used}."
                decision_points = 20 if funding == "Use available cash first" else 10
            elif round_index == 0:
                feedback = "Delaying repairs preserves cash but may cause inconvenience."
                decision_points = 12
            elif round_index == 1:
                feedback = "Skipping training saves money but sacrifices a potential learning opportunity."
                decision_points = 14
            else:
                life["debt"] += 175
                life["cash"] -= min(175, life["cash"])
                feedback = "Illustrative payment plan: $175 paid now and $175 deferred as debt."
                decision_points = 16
            life["debt"] = round(life["debt"]*1.10, 2)
            life["history"].append((feedback, decision_points))
            st.session_state.round += 1
            st.rerun()
    else:
        st.success("All three events completed!")
        for i,(message,_) in enumerate(life["history"],1):
            st.write(f"**Round {i}:** {message}")
        score = min(100, max(0, 30+sum(points for _,points in life["history"]) + min(15,life["cash"]/35) - min(25,life["debt"]/20)))
        lesson = "You explored liquidity, borrowing costs, and opportunity costs. A different choice can be reasonable under different circumstances."
        if st.button("Finish lab & save learning score", type="primary"):
            save_score(MODULES[1],score,lesson)
            st.success(f"Lab complete! Learning score: {round(score)}/100")
    if st.button("↺ Restart Life Happens"):
        st.session_state.round=0
        st.session_state.life={"cash":500,"debt":0,"history":[]}
        st.rerun()


elif page == MODULES[2]:
    st.title("📈 Investment Risk Lab")
    st.write("Compare simplified hypothetical portfolios. These are fictional assets, not recommendations or forecasts.")
    guide([
        "Enter the virtual amount you want to invest.",
        "Move the allocation slider to divide it between lower- and higher-volatility assets.",
        "Compare the portfolio values across downturn, flat, and growth scenarios.",
        "Answer the reflection question and choose a time horizon before finishing."
    ], "See how asset allocation changes sensitivity to market movements; scenarios are not forecasts.")
    st.markdown("#### Step 1 · Set up your portfolio")
    st.write("The investment amount is fictional. Changing the allocation changes how strongly the portfolio reacts to each scenario.")
    a1,a2,a3=st.columns(3)
    with a1: term("Asset allocation")
    with a2: term("Volatile assets")
    with a3: term("Lower-volatility assets")
    amount = st.number_input("Virtual starting investment ($)", 100, 100000, 1000, 100,
        help="The fictional starting amount used for each market scenario.")
    risk_share = st.slider("Allocation to volatile assets (%)", 0, 100, 50, 10,
        help=GLOSSARY["Volatile assets"] + " A higher percentage increases the portfolio's sensitivity to market movements in this model.")
    stable_share = 100-risk_share
    st.write(f"**Portfolio:** {stable_share}% lower-volatility assets + {risk_share}% higher-volatility assets")
    st.markdown("#### Step 2 · Compare possible outcomes")
    st.write("Each bar shows the ending portfolio value under one invented market scenario. Compare both gains and potential losses.")
    term("Downturn")
    scenarios = {"Downturn": (0.01,-0.30), "Flat market":(0.02,0.0), "Growth":(0.03,0.18)}
    outcomes = {}
    for name,(stable_return,volatile_return) in scenarios.items():
        blended = stable_share/100*stable_return + risk_share/100*volatile_return
        outcomes[name] = round(amount*(1+blended),2)
    st.markdown("**Portfolio ending value by scenario (USD)**")
    # Text labels are rendered directly on bars; a table below provides exact values.
    try:
        import plotly.graph_objects as go
        names = list(outcomes)
        values = [outcomes[name] for name in names]
        fig = go.Figure(go.Bar(
            x=values,
            y=names,
            orientation="h",
            text=[f"${v:,.2f}" for v in values],
            textposition="auto",
            marker_color=["#DC6C6C", "#7397C7", "#36A795"],
            hovertemplate="%{y}: $%{x:,.2f}<extra></extra>",
        ))
        fig.update_layout(
            xaxis_title="Ending portfolio value ($)",
            yaxis_title=None,
            yaxis=dict(autorange="reversed"),
            height=320,
            margin=dict(l=10,r=35,t=10,b=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
    except ImportError:
        st.bar_chart(outcomes, horizontal=True)
        st.caption("Exact values are listed in the table below.")
    st.dataframe([{"Scenario":k,"End value ($)":v,"Gain/loss ($)":round(v-amount,2)} for k,v in outcomes.items()], hide_index=True, use_container_width=True)
    st.caption("One-period deterministic teaching scenarios. Returns are invented for illustration; no probabilities, diversification correlations, fees, inflation, or taxes are modeled.")
    downside = amount-outcomes["Downturn"]
    st.metric("Downturn loss in this model",f"${max(0,downside):,.2f}")
    st.markdown("#### Step 3 · Check your understanding")
    st.write("Use what you learned from the chart. The goal is understanding uncertainty, not maximizing a simulated gain.")
    answer = st.radio("What does a higher share of volatile assets usually change in this model?", ["It guarantees higher returns", "It increases sensitivity to market changes", "It removes all risk"], index=None)
    st.write("Choose a risk allocation based on your hypothetical goal. No single allocation is universally best.")
    term("Time horizon")
    horizon = st.selectbox("Hypothetical time horizon", ["Less than 1 year", "1–5 years", "More than 5 years"],
        help=GLOSSARY["Time horizon"])
    if st.button("Finish lab & save learning score", type="primary"):
        if answer is None:
            st.warning("Answer the reflection question before finishing.")
        else:
            correct = answer == "It increases sensitivity to market changes"
            score = 85 if correct else 45
            score += 15 if (horizon=="Less than 1 year" and risk_share<=30) or (horizon=="More than 5 years" and risk_share<=80) or horizon=="1–5 years" else 0
            lesson = "A portfolio's risk depends on allocation and goals; these simple outcomes are scenarios, not predictions."
            save_score(MODULES[2],score,lesson)
            st.success(f"Lab complete! Learning score: {score}/100. {'Correct: volatility increases sensitivity.' if correct else 'Review: volatility increases sensitivity; it does not guarantee returns.'}")
elif page == "Green Investing Lab":
    green_investing(save_score)

elif page == "Responsible Consumption Lab":
    responsible_consumption(save_score)
st.divider()
with st.container(border=True):
    st.markdown("### 🎓 Want a Certificate of Completion?")
    st.write(
        "Complete all five learning labs, then email the AltRisk Academy team "
        "to request a Certificate of Completion. Please include your preferred "
        "name for the certificate and a copy of your downloaded learning report. "
        "Certificates are issued after manual review and are not academic credentials."
    )
    st.info("Contact email: **[ADD CONTACT EMAIL]** — replace this placeholder with the official AltRisk Academy email before sharing the app.")
st.caption("AltRisk Academy · Independent educational prototype · Not investment, tax, or financial advice. No real transactions.")
