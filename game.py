"""Console game for Boggle Blitz."""
import boggle_blitz as core
import score as score_mod
import settings as settings_mod
from i18n import t
from sound import Sound


class QuitGame(Exception):
    pass


def _print(text=""):
    print(text)


def show_header(settings):
    _print("=" * 32)
    _print(t(settings["lang"], "title"))
    _print("=" * 32)


def show_help(settings):
    show_header(settings)
    _print(t(settings["lang"], "help_title"))
    _print(t(settings["lang"], "help_text"))
    input(t(settings["lang"], "press_enter"))


def show_scores(settings):
    show_header(settings)
    _print(t(settings["lang"], "scores"))
    scores = score_mod.load()
    if not scores:
        _print(t(settings["lang"], "no_scores"))
    for idx, item in enumerate(scores, 1):
        _print(f"{idx}. {item.get('name', '?')} {item.get('score', 0)} ({t(settings['lang'], item.get('difficulty', '?'))})")
    input(t(settings["lang"], "press_enter"))


def settings_menu(settings):
    while True:
        show_header(settings)
        _print(t(settings["lang"], "settings"))
        _print(f"{t(settings['lang'], 'lang')}: {settings['lang']}")
        _print(f"{t(settings['lang'], 'sound')}: {t(settings['lang'], 'on' if settings['sound'] else 'off')}")
        _print(f"{t(settings['lang'], 'volume')}: {settings['volume']}")
        _print(f"{t(settings['lang'], 'difficulty')}: {t(settings['lang'], settings['difficulty'])}")
        choice = input(t(settings["lang"], "settings_menu") + "\n" + t(settings["lang"], "choice")).strip().lower()
        if choice == "1":
            settings_mod.cycle_lang(settings)
        elif choice == "2":
            settings_mod.toggle_sound(settings)
        elif choice == "3":
            settings_mod.cycle_volume(settings)
        elif choice == "4":
            settings_mod.cycle_difficulty(settings)
        elif choice == "b":
            settings_mod.save(settings)
            return
        else:
            _print(t(settings["lang"], "unknown"))


def play_round(settings):
    lang = settings["lang"]
    difficulty = settings["difficulty"]
    snd = Sound(settings["sound"], settings["volume"])
    cfg = core.config(difficulty)
    grid = core.make_grid(difficulty)
    found = set()
    total_score = 0
    guesses_left = cfg["rounds"]

    show_header(settings)
    _print(t(lang, "rounds", rounds=guesses_left))
    _print(t(lang, "grid", grid=core.grid_text(grid)))

    while guesses_left > 0:
        answer = input(t(lang, "prompt")).strip().lower()
        if answer == "q":
            raise QuitGame()
        if answer == "done":
            break
        if answer == "hint":
            hints = [word for word in core.hint_words(grid, difficulty) if word not in found]
            if hints:
                _print(t(lang, "hint", words=", ".join(hints)))
                snd.correct()
            else:
                _print(t(lang, "no_hint"))
                snd.incorrect()
            continue
        word = core.normalize_word(answer)
        if not word:
            _print(t(lang, "invalid"))
            continue
        guesses_left -= 1
        if word in found:
            _print(t(lang, "duplicate"))
            snd.incorrect()
        elif core.valid_word(grid, word, difficulty):
            points = core.score_word(word, difficulty)
            found.add(word)
            total_score += points
            _print(t(lang, "accepted", word=word, points=points))
            snd.correct()
        else:
            _print(t(lang, "invalid"))
            snd.incorrect()

    rating_key = core.final_rating(total_score)
    _print(t(lang, "finished", score=total_score, rating=t(lang, rating_key)))
    if total_score > 0:
        snd.win()
    else:
        snd.lose()
    return total_score


def main_menu():
    settings = settings_mod.load()
    while True:
        show_header(settings)
        choice = input(t(settings["lang"], "main_menu") + "\n" + t(settings["lang"], "choice")).strip().lower()
        if choice == "p":
            try:
                result = play_round(settings)
            except QuitGame:
                result = 0
            if result > 0:
                name = input(t(settings["lang"], "name_prompt")).strip()
                if name:
                    score_mod.add(name, result, settings["difficulty"])
                    _print(t(settings["lang"], "saved"))
                else:
                    _print(t(settings["lang"], "not_saved"))
            input(t(settings["lang"], "press_enter"))
        elif choice == "h":
            show_help(settings)
        elif choice == "s":
            settings_menu(settings)
        elif choice == "c":
            show_scores(settings)
        elif choice == "q":
            _print(t(settings["lang"], "bye"))
            return
        else:
            _print(t(settings["lang"], "unknown"))


if __name__ == "__main__":
    main_menu()
