
"""Learning Assessment interface for AltRisk Academy."""
import plotly.graph_objects as go
import streamlit as st

from learning_assessment import learning_gain, score_assessment
from question_bank import QUESTIONS


PRACTICE_GUIDANCE = {
    "diversification": (
        "Spread investments across different assets to reduce reliance on one "
        "investment; diversification cannot eliminate all losses. Try the Investment Risk Lab."
    ),
    "liquidity": (
        "Liquidity is how readily money can be used when needed. Explore emergency "
        "expenses in Your First $1,000 or Life Happens."
    ),
    "budgeting": (
        "Compare income with expenses and plan savings for unexpected costs. "
        "Practice in Your First $1,000 and Life Happens."
    ),
    "risk": (
        "Consider possible losses as well as potential returns; higher risk does "
        "not guarantee a higher return. Explore the Investment Risk Lab."
    ),
}


def restart_assessment():
    st.session_state.assessment_results = {}
    for form in ("pre", "post"):
        for question in QUESTIONS[form]:
            st.session_state.pop(f"assessment_{question['id']}", None)


def render_assessment():
    st.title("Learning Assessment")
    st.write(
        "Check what you know before exploring the learning labs, "
        "then return to see how your answers change."
    )
    st.info(
        "This is a prototype learning check, not a validated exam. "
        "Results are stored only in your current app session."
    )

    if "assessment_results" not in st.session_state:
        st.session_state.assessment_results = {}

    results = st.session_state.assessment_results

    for form, heading in [
        ("pre", "Step 1 — Pre-test"),
        ("post", "Step 3 — Post-test"),
    ]:
        if form == "post":
            st.subheader("Step 2 — Learning experience")
            st.write(
                "Choose the educational labs from the Explore sidebar and complete "
                "them before returning to Learning Assessment for the post-test. "
                "Your completed assessment results stay in this session as you navigate."
            )
        st.subheader(heading)

        if form == "post" and "pre" not in results:
            st.warning("Complete the pre-test first.")
            continue

        if form in results:
            result = results[form]
            st.success(
                f"Completed: {result.correct}/{result.total} "
                f"({result.percentage:.1f}%)"
            )
            continue

        with st.form(f"assessment_{form}"):
            answers = {}
            for question in QUESTIONS[form]:
                answers[question["id"]] = st.radio(
                    question["prompt"],
                    question["options"],
                    index=None,
                    key=f"assessment_{question['id']}",
                )

            submitted = st.form_submit_button(
                f"Submit {form}-test", type="primary"
            )

        if submitted:
            if any(answer is None for answer in answers.values()):
                st.warning("Please answer all six questions.")
            else:
                results[form] = score_assessment(form, answers)
                st.rerun()

    if "pre" in results and "post" in results:
        st.divider()
        st.subheader("Step 4 — Learning results")

        pre = results["pre"]
        post = results["post"]
        gain = learning_gain(pre, post)

        a, b, c = st.columns(3)
        a.metric("Pre-test", f"{pre.correct}/{pre.total} ({pre.percentage:.2f}%)")
        b.metric("Post-test", f"{post.correct}/{post.total} ({post.percentage:.2f}%)")
        c.metric("Change", f"{gain:+.2f} percentage points")

        fig = go.Figure(go.Bar(
            x=["Pre-test", "Post-test"],
            y=[pre.percentage, post.percentage],
            marker_color=["#7397C7", "#2457d6"],
            text=[f"{pre.percentage:.2f}%", f"{post.percentage:.2f}%"],
            textposition="auto",
        ))
        fig.update_layout(
            yaxis=dict(title="Score (%)", range=[0, 100]),
            height=300,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
        )
        st.plotly_chart(fig)

        st.write("**Performance by topic**")
        for topic, (post_correct, post_total) in post.by_topic.items():
            pre_correct, pre_total = pre.by_topic[topic]
            st.write(
                f"**{topic.title()}** — Pre-test: {pre_correct}/{pre_total}; "
                f"post-test: {post_correct}/{post_total}."
            )
            if post_correct < post_total:
                st.info(f"More practice: {PRACTICE_GUIDANCE[topic]}")

        st.caption(
            "These prototype questions have not been educationally validated. "
            "A score change does not prove that the labs caused learning or "
            "establish educational effectiveness."
        )

    st.button("Restart assessment", on_click=restart_assessment)
