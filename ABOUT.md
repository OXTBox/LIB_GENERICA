Friday, November 13, 2026
**LIB_GENERICA**: Generica, a game's words

**What it is built to do:** keep every word a game shows (units, factions, events, menus, buttons,
labels) in plain text files, so one game engine can become many games by editing words, and
every engine (Vibecode3D, xt3d, Python tools, the Sequencer) reads the same files.

**How:**
- Open any file under `sets/galactica/` in a text editor: one label per line.
- To make a new theme: copy the lists you want to change into `sets/<your theme>/`, same names.
- LiveCode: `start using` `livecode/lib_generica.livecodescript`, then `Gen.Load`, `Gen.Label`, `Gen.Say`.
- Python: `python3 -I python/generica.py sets genetic_anomaly galactica` prints what a theme changes.

**How to report:** a theme works when a game shows its words instead of Galactica's. Tell
Claude which label looked wrong (file and line); the label files are the only thing to fix.
