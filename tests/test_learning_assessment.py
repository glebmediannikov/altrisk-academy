import unittest
from learning_assessment import score_assessment, learning_gain
from question_bank import QUESTIONS


class AssessmentTests(unittest.TestCase):
    def test_perfect_score(self):
        answers = {q['id']: q['answer'] for q in QUESTIONS['pre']}
        result = score_assessment('pre', answers)
        self.assertEqual(result.correct, 6)
        self.assertEqual(result.percentage, 100)

    def test_missing_answers_count_as_incorrect(self):
        result = score_assessment('pre', {})
        self.assertEqual(result.correct, 0)
        self.assertEqual(result.total, 6)

    def test_rejects_unknown_question(self):
        with self.assertRaises(ValueError):
            score_assessment('pre', {'not_a_question': 'A'})

    def test_rejects_invalid_choice(self):
        with self.assertRaises(ValueError):
            score_assessment('pre', {'pre01': 'Not an option'})

    def test_gain_is_percentage_points(self):
        pre = score_assessment('pre', {})
        post = score_assessment('post', {q['id']: q['answer'] for q in QUESTIONS['post']})
        self.assertEqual(learning_gain(pre, post), 100)

    def test_topics_have_counts(self):
        result = score_assessment('pre', {})
        self.assertEqual(result.by_topic['diversification'], (0, 2))


if __name__ == '__main__':
    unittest.main()
