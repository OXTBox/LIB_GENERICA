# LIB_GENERICA

**A game's words as plain label files.** Retheme a game by editing labels, not code.

Every word a game shows (unit types, unit properties, factions, event messages, menus, buttons,
UI labels, store, credits) lives in a plain text file, one label per line. Engines and tools load
a **set** of them; a **theme** can sit on top of a base set and change only what differs.

Built from the owner's Generica stacks (2018-2026), themselves based on the Galactica Anno
Dominari source: an application template of every option and field a game developer fills in.
Analysis: `../LIB_GAD/GENERICA_TEMPLATE.md`.

| Path | What |
|---|---|
| `sets/galactica/` | the Galactica words: 49 lists, 533 labels in 37 categories (`INDEX.md`) |
| `sets/genetic_anomaly/` | DRAFT retheme for the Genetic Anomaly Detector: 7 game-state lists over galactica |
| `livecode/lib_generica.livecodescript` | loader for Vibecode3D, xt3d and any stack (`start using` it; engine-free) |
| `python/generica.py` | the same in Python (xtalk_py, tools); `python3 -I python/generica.py sets THEME [BASE]` |
| `tools/extract_from_harvest.py` | a Generica stack's XTJSON harvest -> a set (how `galactica` was made) |

## A label file

```
# list: game_events_text
# category: game_events
# about: A list of text strings displayed to the user when events occur in the game.
You took the star system % from #!
You lost the star system % when * attacked it.
```
Header lines start with `#`; then one label per line, in order (label 1 is the first line; an
empty line is an empty label). Slots, as in Galactica: `%`, `#`, `*`, `^0`, `^1`, ... filled by
`Gen.Fill` / `fill`.

## Use

```
-- LiveCode
start using stack ".../LIB_GENERICA/livecode/lib_generica.livecodescript"
Gen.Load ".../LIB_GENERICA/sets", "genetic_anomaly", "galactica"
put "Node 7" into tSlots["%"]
put "the Helix Institute" into tSlots["#"]
answer Gen.Say("game_events_text", 1, tSlots)   -- You secured the node Node 7 from the Helix Institute!
```
```python
import generica as gen
g = gen.load('~/projects/LIB_GENERICA/sets', 'genetic_anomaly', base='galactica')
g.say('game_events_text', 1, {'%': 'Node 7', '#': 'the Helix Institute'})
```
In a Sequencer `.seq` file: `{@game_events_text:1}` (the game loads the set first).

## Retheme a game

Make `sets/<theme>/`, copy only the lists you want to change from `galactica/` (same folder and
file names), edit the words. Load with `Gen.Load sets, "<theme>", "galactica"`.
