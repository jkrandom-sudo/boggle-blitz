# Boggle Blitz / 单词方阵

A bilingual console word-grid game written with the Python standard library.

一个使用 Python 标准库编写的双语控制台单词方阵小游戏。

## Features / 功能

- Generate a letter grid for each game.
- Find words by connecting adjacent letters horizontally, vertically, or diagonally.
- Built-in word banks for easy, normal, and hard modes.
- Bilingual UI: English and Chinese.
- Persistent JSON settings and top scores.
- Optional terminal bell sound with adjustable volume.
- Automated tests for core logic, persistence modules, sound, and menu gameplay.

## Requirements / 环境要求

- Python 3.9+
- No third-party dependencies.

## Run / 启动

```bash
python3 game.py
```

## Test / 测试

```bash
python3 -m py_compile game.py boggle_blitz.py i18n.py settings.py score.py sound.py
python3 tests/run_tests.py
```

## How to Play / 玩法

1. Choose Play from the main menu.
2. Look at the letter grid.
3. Type words one at a time.
4. A valid word must be at least 3 letters, in the built-in word bank, and formable by adjacent grid cells.
5. Type `hint` to show possible words.
6. Type `done` to finish early or `q` to quit the current round.

## Difficulty / 难度

| Difficulty | Grid | Guesses | Score bonus |
| --- | --- | ---: | ---: |
| easy | 3x3 | 6 | 1x |
| normal | 4x4 | 8 | 2x |
| hard | 4x4 | 10 | 3x |

## Files / 文件

- `game.py` — console UI and menus.
- `boggle_blitz.py` — core grid, word validation, hint, and scoring logic.
- `i18n.py` — bilingual strings.
- `settings.py` — JSON settings persistence.
- `score.py` — JSON score persistence.
- `sound.py` — terminal bell sound helper.
- `tests/` — automated unit tests.
