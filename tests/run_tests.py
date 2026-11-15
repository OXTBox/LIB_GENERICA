#!/usr/bin/env python3
"""LIB_GENERICA's check that runs without LiveCode (A-50): a base theme and a theme over it, made
in a temporary folder, load the way generica.load() promises (the theme's labels win, the base fills
the rest, ^ slots are filled longest first).

    python3 -I tests/run_tests.py
"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'python'))
import tempfile
import generica                               # noqa: E402

CHECKS, FAILS = [0], []


def check(name, ok, got=None):
    CHECKS[0] += 1
    if not ok:
        FAILS.append(name)
        print("FAIL  %s%s" % (name, "" if got is None else "  (got %r)" % (got,)))
    else:
        print("ok    %s" % name)


def done():
    print("\n%d of %d passed" % (CHECKS[0] - len(FAILS), CHECKS[0]))
    return 1 if FAILS else 0


def main():
    with tempfile.TemporaryDirectory() as root:
        for theme, files in {'base': {'Ships/names.txt': '# about: ship names\nScout\nRaider\n',
                                      'Words/greet.txt': 'Hello ^1, you have ^10 credits\n'},
                             'space': {'Ships/names.txt': 'Starling\nComet\nNova\n'}}.items():
            for rel, text in files.items():
                os.makedirs(os.path.join(root, theme, os.path.dirname(rel)), exist_ok=True)
                open(os.path.join(root, theme, rel), 'w', encoding='utf-8').write(text)
        g = generica.load(root, 'space', base='base')
        check('the theme wins over the base', g.list('names') == ['Starling', 'Comet', 'Nova'], g.list('names'))
        check('the base fills what the theme lacks', g.label('greet', 1).startswith('Hello'))
        check('label numbers start at 1; out of range is empty', g.label('names', 1) == 'Starling' and g.label('names', 9) == '')
        check('slots: ^10 is filled before ^1', g.say('greet', 1, {'^1': 'Bill', '^10': 7}) == 'Hello Bill, you have 7 credits',
              g.say('greet', 1, {'^1': 'Bill', '^10': 7}))
        check('count and lists', g.count('names') == 3 and g.lists() == ['greet', 'names'], g.lists())
        missing = False
        try:
            generica.load(root, 'nope')
        except FileNotFoundError:
            missing = True
        check('a missing theme is an error, not an empty game', missing)
    return done()


if __name__ == '__main__':
    sys.exit(main())
