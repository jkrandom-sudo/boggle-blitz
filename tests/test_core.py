import unittest

import boggle_blitz as core


class FixedRng:
    def __init__(self, values):
        self.values = list(values)

    def choice(self, seq):
        return self.values.pop(0)


class TestCore(unittest.TestCase):
    def test_config_and_word_bank_fallback(self):
        self.assertEqual(core.config("bad"), core.config("normal"))
        self.assertEqual(core.word_bank("bad"), core.word_bank("normal"))

    def test_make_grid(self):
        rng = FixedRng(list("abcdefghi"))
        grid = core.make_grid("easy", rng)
        self.assertEqual(len(grid), 3)
        self.assertEqual(grid[0], ["a", "b", "c"])

    def test_grid_text(self):
        self.assertEqual(core.grid_text([["a", "b"], ["c", "d"]]), "A B\nC D")

    def test_normalize_word(self):
        self.assertEqual(core.normalize_word(" Cat! "), "cat")

    def test_neighbors(self):
        self.assertEqual(sorted(core.neighbors((0, 0), 3)), [(0, 1), (1, 0), (1, 1)])
        self.assertEqual(len(core.neighbors((1, 1), 3)), 8)

    def test_can_form_word(self):
        grid = [["c", "a", "t"], ["d", "o", "g"], ["s", "u", "n"]]
        self.assertTrue(core.can_form_word(grid, "cat"))
        self.assertTrue(core.can_form_word(grid, "dog"))
        self.assertFalse(core.can_form_word(grid, "cats"))

    def test_valid_word(self):
        grid = [["c", "a", "t"], ["d", "o", "g"], ["s", "u", "n"]]
        self.assertTrue(core.valid_word(grid, "cat", "easy"))
        self.assertFalse(core.valid_word(grid, "ca", "easy"))
        self.assertFalse(core.valid_word(grid, "zzz", "easy"))

    def test_score_word(self):
        self.assertEqual(core.score_word("cat", "easy"), 9)
        self.assertEqual(core.score_word("cat", "normal"), 18)

    def test_hint_words(self):
        grid = [["c", "a", "t"], ["d", "o", "g"], ["s", "u", "n"]]
        self.assertEqual(core.hint_words(grid, "easy", 2), ["cat", "dog"])

    def test_final_rating(self):
        self.assertEqual(core.final_rating(120), "master")
        self.assertEqual(core.final_rating(60), "expert")
        self.assertEqual(core.final_rating(20), "novice")
        self.assertEqual(core.final_rating(0), "beginner")


if __name__ == "__main__":
    unittest.main()
