"""Core logic for Boggle Blitz."""
import random

WORDS = {
    "easy": {"cat", "dog", "sun", "run", "red", "blue", "bird", "tree", "star", "moon"},
    "normal": {"cat", "dog", "sun", "run", "red", "blue", "bird", "tree", "star", "moon", "stone", "light", "water", "green", "plane"},
    "hard": {"cat", "dog", "sun", "run", "red", "blue", "bird", "tree", "star", "moon", "stone", "light", "water", "green", "plane", "planet", "silver", "rocket", "forest", "dragon"},
}
DIFFICULTY_CONFIG = {
    "easy": {"size": 3, "rounds": 6, "bonus": 1},
    "normal": {"size": 4, "rounds": 8, "bonus": 2},
    "hard": {"size": 4, "rounds": 10, "bonus": 3},
}
VOWELS = "aeiou"
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def config(difficulty):
    return DIFFICULTY_CONFIG.get(difficulty, DIFFICULTY_CONFIG["normal"])


def word_bank(difficulty):
    return WORDS.get(difficulty, WORDS["normal"])


def make_grid(difficulty, rng=None):
    rng = rng or random
    size = config(difficulty)["size"]
    cells = []
    for idx in range(size * size):
        pool = VOWELS if idx % 5 == 0 else LETTERS
        cells.append(rng.choice(pool))
    return [cells[i:i + size] for i in range(0, len(cells), size)]


def grid_text(grid):
    return "\n".join(" ".join(row).upper() for row in grid)


def normalize_word(text):
    return "".join(ch for ch in text.strip().lower() if ch.isalpha())


def neighbors(pos, size):
    r, c = pos
    result = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size:
                result.append((nr, nc))
    return result


def can_form_word(grid, word):
    word = normalize_word(word)
    if not word:
        return False
    size = len(grid)

    def search(idx, r, c, used):
        if grid[r][c] != word[idx]:
            return False
        if idx == len(word) - 1:
            return True
        used.add((r, c))
        for nr, nc in neighbors((r, c), size):
            if (nr, nc) not in used and search(idx + 1, nr, nc, used):
                used.remove((r, c))
                return True
        used.remove((r, c))
        return False

    for r in range(size):
        for c in range(size):
            if search(0, r, c, set()):
                return True
    return False


def valid_word(grid, word, difficulty):
    word = normalize_word(word)
    return len(word) >= 3 and word in word_bank(difficulty) and can_form_word(grid, word)


def score_word(word, difficulty):
    word = normalize_word(word)
    return (len(word) * len(word)) * config(difficulty)["bonus"]


def hint_words(grid, difficulty, limit=3):
    found = [word for word in sorted(word_bank(difficulty)) if valid_word(grid, word, difficulty)]
    return found[:limit]


def final_rating(score):
    if score >= 120:
        return "master"
    if score >= 60:
        return "expert"
    if score >= 20:
        return "novice"
    return "beginner"
