import unittest
from scoring import ALL_ITEMS, calculate_scale_scores, cronbach_alpha, score_response


class ScoringTests(unittest.TestCase):
    def test_forward_scoring(self):
        self.assertEqual(score_response(1, False), 1)
        self.assertEqual(score_response(5, False), 5)

    def test_reverse_scoring(self):
        self.assertEqual(score_response(1, True), 5)
        self.assertEqual(score_response(2, True), 4)
        self.assertEqual(score_response(3, True), 3)
        self.assertEqual(score_response(4, True), 2)
        self.assertEqual(score_response(5, True), 1)

    def test_all_neutral_scores_three(self):
        answers = {item_id: 3 for item_id, *_ in ALL_ITEMS}
        scores = calculate_scale_scores(answers)
        self.assertTrue(all(score == 3.0 for score in scores.values()))

    def test_keying_is_applied(self):
        # On reverse-keyed items, raw=1 becomes scored=5; on positive items raw=5 stays 5.
        answers = {}
        for item_id, _, _, reverse in ALL_ITEMS:
            answers[item_id] = 1 if reverse else 5
        scores = calculate_scale_scores(answers)
        self.assertTrue(all(score == 5.0 for score in scores.values()))

    def test_incomplete_scale_rejected(self):
        answers = {item_id: 3 for item_id, *_ in ALL_ITEMS}
        answers.pop("P01")
        with self.assertRaises(ValueError):
            calculate_scale_scores(answers)

    def test_alpha_perfect_consistency(self):
        rows = [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4], [5, 5, 5]]
        self.assertEqual(cronbach_alpha(rows), 1.0)


if __name__ == "__main__":
    unittest.main()
