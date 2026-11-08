"""Deterministic educational recommendations; no user data is stored."""
from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence, TypedDict


class Question(TypedDict):
    id: str
    topic: str
    prompt: str
    options: tuple[str, ...]
    answer: str


@dataclass(frozen=True)
class Recommendation:
    topic: str
    correct: int
    total: int
    explanation: str
    example: str
    lab: str
    reason: str


@dataclass(frozen=True)
class Feedback:
    recommendations: tuple[Recommendation, ...]
    incorrect_ids: tuple[str, ...]
    unanswered_ids: tuple[str, ...]


# The question bank's "risk" topic is displayed as financial risk in the UI.
TOPIC_CONTENT = {
    "diversification": (
        "Diversification spreads exposure across investments, reducing dependence "
        "on one company. It cannot eliminate market risk or guarantee returns.",
        "Hypothetical example: $1,000 in one company could fall to $600 if that "
        "company loses 40% of its value. Spreading investments can reduce "
        "concentration risk, but a market downturn could still affect the mix.",
        "Green Investing Lab",
    ),
    "liquidity": (
        "Liquidity describes how readily an asset can be used to pay a bill. "
        "Accessible savings can be more suitable for an emergency than an "
        "asset that is difficult to sell quickly.",
        "Hypothetical example: a $500 emergency bill could be paid from $500 "
        "in accessible savings; selling a house or a locked investment may "
        "take time or involve costs.",
        "Your First $1,000",
    ),
    "budgeting": (
        "A budget compares income with expenses and helps plan for needs and "
        "unexpected costs.",
        "Hypothetical example: $1,200 monthly income minus $1,350 in expenses "
        "leaves a $150 deficit. Consider reducing optional expenses or finding "
        "additional income to close the gap.",
        "Your First $1,000",
    ),
    "risk": (
        "Potential return and downside exposure are different: a possible "
        "gain is not guaranteed, and an investment may lose value.",
        "Hypothetical example: two $1,000 investments each have a possible "
        "$100 gain. In one downside scenario, A falls to $900 (a $100 loss) "
        "and B falls to $700 (a $300 loss). B has greater downside exposure "
        "in these scenarios; they are not forecasts.",
        "Investment Risk Lab",
    ),
}


def recommendations_for_scores(
    scores: Mapping[str, tuple[int, int]],
) -> tuple[Recommendation, ...]:
    """Recommend imperfect topics, ordered by lowest fraction correct then topic."""
    for topic, (correct, total) in scores.items():
        if topic not in TOPIC_CONTENT:
            raise ValueError(f"Unsupported topic: {topic}")
        if total < 0 or correct < 0 or correct > total:
            raise ValueError(f"Invalid topic score for {topic}")

    ranked = sorted(
        ((topic, correct, total) for topic, (correct, total) in scores.items()
         if total > 0 and correct < total),
        key=lambda item: (Fraction(item[1], item[2]), item[0]),
    )
    recommendations = []
    for topic, correct, total in ranked:
        explanation, example, lab = TOPIC_CONTENT[topic]
        recommendations.append(Recommendation(
            topic=topic,
            correct=correct,
            total=total,
            explanation=explanation,
            example=example,
            lab=lab,
            reason=f"You answered {correct} of {total} questions correctly on this topic.",
        ))
    return tuple(recommendations)


def generate_feedback(
    answers: Mapping[str, str | None],
    questions: Sequence[Question],
) -> Feedback:
    """Analyze provided choices; unanswered questions are reported, not scored.

    Invalid choices, unknown IDs, duplicate question IDs, and unsupported topics
    raise ValueError. No input or output is written to persistent storage.
    """
    ids = [question["id"] for question in questions]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate question IDs")
    if set(answers) - set(ids):
        raise ValueError("Answers contain unknown question IDs")
    scores: dict[str, tuple[int, int]] = {}
    incorrect = []
    unanswered = []
    for question in questions:
        topic = question["topic"]
        if topic not in TOPIC_CONTENT:
            raise ValueError(f"Unsupported topic: {topic}")
        answer = answers.get(question["id"])
        if answer is None:
            unanswered.append(question["id"])
            continue
        if answer not in question["options"]:
            raise ValueError(f"Invalid option for {question['id']}")
        correct, total = scores.get(topic, (0, 0))
        if answer == question["answer"]:
            correct += 1
        else:
            incorrect.append(question["id"])
        scores[topic] = (correct, total + 1)
    return Feedback(recommendations_for_scores(scores), tuple(incorrect), tuple(unanswered))
