"""Pure assessment helpers for the AltRisk Academy Technovation pilot.

No user identifiers, network requests, or persistent storage.
"""
from dataclasses import dataclass
from typing import Mapping

from question_bank import QUESTIONS


@dataclass(frozen=True)
class AssessmentResult:
    correct: int
    total: int
    percentage: float
    by_topic: dict[str, tuple[int, int]]


def score_assessment(form: str, answers: Mapping[str, str]) -> AssessmentResult:
    """Score a completed form. Missing answers are counted as incorrect.

    Raises ValueError for an unknown form, unexpected question IDs, or invalid choices.
    """
    if form not in QUESTIONS:
        raise ValueError(f"Unknown assessment form: {form}")
    questions = QUESTIONS[form]
    known = {q['id'] for q in questions}
    if set(answers) - known:
        raise ValueError('Answers contain unknown question IDs')
    topic_counts: dict[str, list[int]] = {}
    correct = 0
    for q in questions:
        answer = answers.get(q['id'])
        if answer is not None and answer not in q['options']:
            raise ValueError(f"Invalid option for {q['id']}")
        hit = int(answer == q['answer'])
        correct += hit
        topic_counts.setdefault(q['topic'], [0, 0])
        topic_counts[q['topic']][0] += hit
        topic_counts[q['topic']][1] += 1
    return AssessmentResult(correct, len(questions), round(100 * correct / len(questions), 2),
                            {topic: tuple(values) for topic, values in topic_counts.items()})


def learning_gain(pre: AssessmentResult, post: AssessmentResult) -> float:
    """Return the percentage-point change, not a causal effect estimate."""
    if pre.total != post.total:
        raise ValueError('Forms must have the same number of questions')
    return round(post.percentage - pre.percentage, 2)
