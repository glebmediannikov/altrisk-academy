import builtins
import socket

import pytest

from adaptive_feedback import generate_feedback, recommendations_for_scores
from learning_assessment import score_assessment
from question_bank import QUESTIONS


def correct_answers(form="pre"):
    return {question["id"]: question["answer"] for question in QUESTIONS[form]}


def wrong_answer(question):
    return next(option for option in question["options"] if option != question["answer"])


def test_identifies_incorrect_answers_and_topics():
    questions = QUESTIONS["pre"]
    answers = correct_answers()
    for index in (0, 1, 2, 3):
        answers[questions[index]["id"]] = wrong_answer(questions[index])
    feedback = generate_feedback(answers, questions)
    assert feedback.incorrect_ids == ("pre01", "pre02", "pre03", "pre04")
    assert not feedback.unanswered_ids
    by_topic = {item.topic: item for item in feedback.recommendations}
    assert set(by_topic) == {"diversification", "liquidity", "budgeting", "risk"}
    assert (by_topic["diversification"].correct, by_topic["diversification"].total) == (1, 2)
    assert (by_topic["liquidity"].correct, by_topic["liquidity"].total) == (0, 1)
    assert feedback.recommendations == recommendations_for_scores(
        score_assessment("pre", answers).by_topic
    )


def test_priority_is_fraction_correct_then_alphabetical():
    scores = {
        "diversification": (1, 2), "risk": (0, 1),
        "liquidity": (0, 1), "budgeting": (2, 2),
    }
    assert [r.topic for r in recommendations_for_scores(scores)] == [
        "liquidity", "risk", "diversification",
    ]


def test_consistency_and_no_input_mutation():
    questions = QUESTIONS["post"]
    answers = {q["id"]: wrong_answer(q) for q in questions}
    original = dict(answers)
    first = generate_feedback(answers, questions)
    assert first == generate_feedback(dict(reversed(list(answers.items()))), questions)
    assert answers == original


def test_hypothetical_examples_and_labs():
    content = {r.topic: r for r in recommendations_for_scores({
        "diversification": (0, 1), "liquidity": (0, 1),
        "budgeting": (0, 1), "risk": (0, 1),
    })}
    assert 1000 * (1 - 0.40) == 600
    assert all(s in content["diversification"].example for s in ("$1,000", "$600", "40%"))
    assert all(s in content["liquidity"].example for s in ("$500", "savings"))
    assert 1350 - 1200 == 150
    assert all(s in content["budgeting"].example for s in ("$1,200", "$1,350", "$150 deficit"))
    assert 1000 - 900 == 100 and 1000 - 700 == 300
    assert all(s in content["risk"].example for s in ("$1,000", "$900", "$100 loss", "$700", "$300 loss"))
    assert all("Hypothetical" in item.example for item in content.values())
    assert "cannot eliminate market risk or guarantee returns" in content["diversification"].explanation
    assert content["risk"].lab == "Investment Risk Lab"
    assert content["diversification"].lab == "Green Investing Lab"
    assert content["liquidity"].lab == content["budgeting"].lab == "Your First $1,000"


@pytest.mark.parametrize("form", ["pre", "post"])
def test_all_correct_has_no_recommendations(form):
    feedback = generate_feedback(correct_answers(form), QUESTIONS[form])
    assert feedback.recommendations == ()
    assert feedback.incorrect_ids == ()
    assert feedback.unanswered_ids == ()


def test_incomplete_answers_are_reported_not_treated_as_wrong():
    questions = QUESTIONS["pre"]
    answers = {"pre01": wrong_answer(questions[0]), "pre05": None}
    feedback = generate_feedback(answers, questions)
    assert feedback.incorrect_ids == ("pre01",)
    assert feedback.unanswered_ids == ("pre02", "pre03", "pre04", "pre05", "pre06")
    assert [(r.topic, r.correct, r.total) for r in feedback.recommendations] == [
        ("diversification", 0, 1)
    ]
    assert generate_feedback({}, questions).recommendations == ()


@pytest.mark.parametrize("answers", [
    {"pre01": "Not an option"}, {"unknown": "answer"}, {"pre01": ""},
])
def test_invalid_answers_raise(answers):
    with pytest.raises(ValueError):
        generate_feedback(answers, QUESTIONS["pre"])


def test_invalid_metadata_and_scores_raise():
    question = QUESTIONS["pre"][0]
    with pytest.raises(ValueError, match="Duplicate"):
        generate_feedback({}, [question, question])
    with pytest.raises(ValueError, match="Unsupported"):
        generate_feedback({}, [{**question, "topic": "unsupported"}])
    with pytest.raises(ValueError, match="Invalid topic score"):
        recommendations_for_scores({"risk": (2, 1)})


def test_engine_does_not_store_data_or_use_network(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Unexpected file or network access")

    monkeypatch.setattr(builtins, "open", forbidden)
    monkeypatch.setattr(socket, "socket", forbidden)
    answers = {"pre01": wrong_answer(QUESTIONS["pre"][0])}
    feedback = generate_feedback(answers, QUESTIONS["pre"])
    assert feedback.incorrect_ids == ("pre01",)
    assert answers == {"pre01": wrong_answer(QUESTIONS["pre"][0])}
