#!/usr/bin/env python3
"""generica.py - a game's words as plain label files (LIB_GENERICA), the Python twin of
livecode/lib_generica.livecodescript: same files, same names.

    import generica as gen
    g = gen.load('~/projects/LIB_GENERICA/sets', 'genetic_anomaly', base='galactica')
    g.label('game_unit_types', 1)          -> 'agent'
    g.say('game_events_text', 1, {'%': 'Node 7', '#': 'the Helix'})

    python3 -I python/generica.py SETS THEME [BASE]    print a summary (lists, labels, overlays)
"""
import os
import sys


class Generica:
    def __init__(self):
        self.labels, self.about, self.theme, self.source = {}, {}, None, {}

    def load_theme(self, folder, theme):
        root = os.path.join(os.path.expanduser(folder), theme)
        if not os.path.isdir(root):
            raise FileNotFoundError(root)
        for cat in sorted(os.listdir(root)):
            cdir = os.path.join(root, cat)
            if not os.path.isdir(cdir):
                continue
            for f in sorted(os.listdir(cdir)):
                if not f.endswith('.txt'):
                    continue
                lines = open(os.path.join(cdir, f), encoding='utf-8').read().replace('\r', '').split('\n')
                about = ''
                while lines and lines[0].startswith('#'):
                    if lines[0].startswith('# about:'):
                        about = lines[0][len('# about:'):].strip()
                    lines.pop(0)
                if lines and lines[-1] == '':
                    lines.pop()
                name = f[:-4]
                self.labels[name], self.about[name], self.source[name] = lines, about, theme

    def label(self, name, n):
        items = self.labels.get(name, [])
        return items[n - 1] if 1 <= n <= len(items) else ''

    def list(self, name):
        return list(self.labels.get(name, []))

    def count(self, name):
        return len(self.labels.get(name, []))

    def lists(self):
        return sorted(self.labels)

    @staticmethod
    def fill(text, slots):
        for key in sorted(slots, key=len, reverse=True):     # ^10 before ^1
            text = text.replace(key, str(slots[key]))
        return text

    def say(self, name, n, slots=None):
        return self.fill(self.label(name, n), slots or {})


def load(folder, theme, base=None):
    g = Generica()
    if base and base != theme:
        g.load_theme(folder, base)
    g.load_theme(folder, theme)
    g.theme = theme
    return g


if __name__ == '__main__':
    if len(sys.argv) < 3 or sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0)
    g = load(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    own = [n for n in g.lists() if g.source[n] == g.theme]
    print('%s: %d lists, %d labels; %d lists from the theme itself%s' % (
        g.theme, len(g.lists()), sum(map(g.count, g.lists())), len(own),
        (', the rest from ' + sys.argv[3]) if len(sys.argv) > 3 else ''))
    for n in own:
        print('  %-30s %3d  %s' % (n, g.count(n), g.label(n, 1)))
