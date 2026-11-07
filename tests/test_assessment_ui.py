import json
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from question_bank import QUESTIONS


APP = str(Path(__file__).parent.parent / "app.py")


def assessment_app():
    app = AppTest.from_file(APP, default_timeout=30)
    app.query_params["lab"] = "learning-assessment"
    return app.run()


def answer_form(app, form, correct_count=6):
    for index, question in enumerate(QUESTIONS[form]):
        answer = question["answer"]
        if index >= correct_count:
            answer = next(option for option in question["options"] if option != answer)
        app.radio(key=f"assessment_{question['id']}").set_value(answer)
    app.button(key=f"FormSubmitter:assessment_{form}-Submit {form}-test").click().run()
    assert not app.exception


def test_render_and_post_test_access_restriction():
    app = assessment_app()
    assert not app.exception
    assert app.title[0].value == "Learning Assessment"
    assert len([r for r in app.radio if r.key and r.key.startswith("assessment_pre")]) == 6
    assert not [r for r in app.radio if r.key and r.key.startswith("assessment_post")]
    assert any("Complete the pre-test first" in warning.value for warning in app.warning)
    assert any("prototype" in info.value for info in app.info)


@pytest.mark.parametrize("answered", [0, 5])
def test_unanswered_pre_test_is_not_submitted(answered):
    app = assessment_app()
    for question in QUESTIONS["pre"][:answered]:
        app.radio(key=f"assessment_{question['id']}").set_value(question["answer"])
    app.button(key="FormSubmitter:assessment_pre-Submit pre-test").click().run()
    assert not app.exception
    assert any("answer all six" in warning.value for warning in app.warning)
    assert "pre" not in app.session_state["assessment_results"]
    assert not [r for r in app.radio if r.key and r.key.startswith("assessment_post")]


def test_pre_test_submission_and_no_resubmission():
    app = assessment_app()
    answer_form(app, "pre", correct_count=4)
    pre = app.session_state["assessment_results"]["pre"]
    assert (pre.correct, pre.total, pre.percentage) == (4, 6, 66.67)
    assert any("4/6 (66.7%)" in item.value for item in app.success)
    assert not [r for r in app.radio if r.key and r.key.startswith("assessment_pre")]
    assert len([r for r in app.radio if r.key and r.key.startswith("assessment_post")]) == 6
    assert not [b for b in app.button if b.label == "Submit pre-test"]


def test_unanswered_post_test_is_not_submitted():
    app = assessment_app()
    answer_form(app, "pre")
    app.button(key="FormSubmitter:assessment_post-Submit post-test").click().run()
    assert not app.exception
    assert any("answer all six" in warning.value for warning in app.warning)
    assert "post" not in app.session_state["assessment_results"]


@pytest.mark.parametrize(
    "pre_correct,post_correct,expected_gain",
    [(3, 5, "+33.33 percentage points"), (6, 0, "-100.00 percentage points")],
)
def test_results_scores_gain_topics_and_chart(pre_correct, post_correct, expected_gain):
    app = assessment_app()
    answer_form(app, "pre", pre_correct)
    answer_form(app, "post", post_correct)
    results = app.session_state["assessment_results"]
    assert results["pre"].correct == pre_correct
    assert results["post"].correct == post_correct
    assert app.metric[0].value == f"{pre_correct}/6 ({results['pre'].percentage:.2f}%)"
    assert app.metric[1].value == f"{post_correct}/6 ({results['post'].percentage:.2f}%)"
    assert app.metric[2].value == expected_gain
    charts = app.get("plotly_chart")
    assert len(charts) == 1
    chart = json.loads(charts[0].proto.spec)
    assert chart["data"][0]["x"] == ["Pre-test", "Post-test"]
    assert chart["data"][0]["y"] == [results["pre"].percentage, results["post"].percentage]
    assert any("Budgeting" in item.value and "post-test" in item.value for item in app.markdown)
    assert any("More practice:" in item.value for item in app.info)
    assert any("does not prove" in item.value for item in app.caption)
    assert not [b for b in app.button if b.label == "Submit post-test"]


def test_results_persist_across_labs_and_dashboard():
    app = assessment_app()
    answer_form(app, "pre", 4)
    answer_form(app, "post", 5)
    results = dict(app.session_state["assessment_results"])
    for page in [
        "Your First $1,000", "Life Happens", "Investment Risk Lab",
        "Green Investing Lab", "Responsible Consumption Lab", "Dashboard",
        "Learning Assessment",
    ]:
        app.sidebar.radio[0].set_value(page).run()
        assert not app.exception
        assert app.session_state["assessment_results"] == results
    assert app.metric[0].value == "4/6 (66.67%)"
    assert app.metric[1].value == "5/6 (83.33%)"


def test_restart_clears_results_answers_and_leaves_lab_scores_alone():
    app = assessment_app()
    answer_form(app, "pre")
    answer_form(app, "post")
    app.session_state["scores"] = {"Life Happens": {"score": 80, "lesson": "Example"}}
    next(button for button in app.button if button.label == "Restart assessment").click().run()
    assert not app.exception
    assert app.session_state["assessment_results"] == {}
    assert app.session_state["scores"]["Life Happens"]["score"] == 80
    assert all(app.radio(key=f"assessment_{q['id']}").value is None for q in QUESTIONS["pre"])
    assert not [r for r in app.radio if r.key and r.key.startswith("assessment_post")]
    answer_form(app, "pre")
    assert all(app.radio(key=f"assessment_{q['id']}").value is None for q in QUESTIONS["post"])


def test_restart_during_unfinished_post_test():
    app = assessment_app()
    answer_form(app, "pre")
    first = QUESTIONS["post"][0]
    app.radio(key=f"assessment_{first['id']}").set_value(first["answer"])
    app.button(key="FormSubmitter:assessment_post-Submit post-test").click().run()
    next(button for button in app.button if button.label == "Restart assessment").click().run()
    assert not app.exception
    assert app.session_state["assessment_results"] == {}
    answer_form(app, "pre")
    assert app.radio(key=f"assessment_{first['id']}").value is None


def test_personalized_path_updates_after_post_test():
    app = assessment_app()
    answer_form(app, "pre", 4)
    assert any("Your Personalized Learning Path" in item.value for item in app.subheader)
    assert any("Based on your pre-test" in item.value for item in app.caption)
    assert app.button(key="assessment_path_diversification")
    assert app.button(key="assessment_path_budgeting")
    assert any("Hypothetical example" in item.value for item in app.markdown)
    answer_form(app, "post", 5)
    assert any("Based on your post-test" in item.value for item in app.caption)
    assert [button.key for button in app.button if button.key and button.key.startswith("assessment_path_")] == [
        "assessment_path_budgeting"
    ]
    assert app.metric[0].value == "4/6 (66.67%)"
    assert app.metric[1].value == "5/6 (83.33%)"


@pytest.mark.parametrize("topic,lab,slug", [
    ("diversification", "Green Investing Lab", "green-investing"),
    ("risk", "Investment Risk Lab", "investment-risk"),
    ("budgeting", "Your First $1,000", "first-1000"),
    ("liquidity", "Your First $1,000", "first-1000"),
])
def test_recommended_lab_navigation_and_return(topic, lab, slug):
    app = assessment_app()
    answer_form(app, "pre", 0)
    pre = app.session_state["assessment_results"]["pre"]
    app.button(key=f"assessment_path_{topic}").click().run()
    assert not app.exception
    assert app.sidebar.radio[0].value == lab
    assert app.query_params["lab"] == slug
    assert app.session_state["assessment_results"]["pre"] == pre
    app.sidebar.radio[0].set_value("Learning Assessment").run()
    assert not app.exception
    assert app.query_params["lab"] == "learning-assessment"
    assert app.button(key=f"assessment_path_{topic}")
    assert app.session_state["assessment_results"]["pre"] == pre


def test_perfect_pre_and_restart_clear_learning_path():
    app = assessment_app()
    answer_form(app, "pre", 6)
    assert any("all questions correctly" in item.value for item in app.success)
    assert not [button for button in app.button if button.key and button.key.startswith("assessment_path_")]
    answer_form(app, "post", 0)
    assert app.button(key="assessment_path_risk")
    next(button for button in app.button if button.label == "Restart assessment").click().run()
    assert not app.exception
    assert app.session_state["assessment_results"] == {}
    assert not any("Your Personalized Learning Path" in item.value for item in app.subheader)
    assert not [button for button in app.button if button.key and button.key.startswith("assessment_path_")]
