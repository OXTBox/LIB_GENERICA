#!/usr/bin/env python3
"""extract_from_harvest.py - a Generica stack's labels (XTJSON harvest) -> plain label files.

    python3 -I tools/extract_from_harvest.py HARVEST_FOLDER THEME
    e.g. ~/projects/XTJSON/batch/GenericaProperties_02042024A/GenericaProperties_03182026a galactica

Writes sets/<THEME>/<category>/<list>.txt: a '#' header (list, category, description), then one
label per line in order (an empty line is an empty label), and sets/<THEME>/INDEX.md.
In the stack each list is a custom property array (keys 001, 002 ... and 'description') in a
custom property set (= category) on any card; values look like '12.[label text]'.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Game_UI_Properties is the stack's scratch state (stray single entries under real list names)
SKIP_SETS = {'Game_UI_Properties'}
LABEL = re.compile(r'^\s*\d+\.\[(.*)\]\s*$', re.S)


def lists_of(harvest):
    st = json.load(open(glob.glob(os.path.join(harvest, 'stack_*.json'))[0], encoding='utf-8'))
    found = {}
    for card in st.get('cards', []):
        for category, body in card.get('custom', {}).get('$sets', {}).items():
            if category in SKIP_SETS:
                continue
            for name, arr in body.items():
                if not isinstance(arr, dict):
                    continue
                keys = sorted(k for k in arr if k != 'description')
                if not keys or not all(k.isdigit() for k in keys):
                    continue            # not a label list (e.g. the Game_UI_Properties scratch set)
                labels = []
                for k in keys:
                    v = str(arr[k])
                    m = LABEL.match(v)
                    labels.append((m.group(1) if m else v).replace('\r', '').replace('\n', ' '))
                found[(category, name)] = (str(arr.get('description', '')).strip(), labels)
    return found


def main():
    if len(sys.argv) != 3 or sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        return
    harvest, theme = sys.argv[1], sys.argv[2]
    out = os.path.join(HERE, 'sets', theme)
    found = lists_of(harvest)
    rows = []
    for (category, name), (desc, labels) in sorted(found.items()):
        folder = os.path.join(out, category)
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, name + '.txt'), 'w', encoding='utf-8') as f:
            f.write('# list: %s\n# category: %s\n# about: %s\n' % (name, category, desc.replace('\n', ' ')))
            f.write('\n'.join(labels) + '\n')
        rows.append('| %s | %s | %d | %s |' % (category, name, len(labels), desc.replace('\n', ' ').replace('|', '/')[:110]))
    with open(os.path.join(out, 'INDEX.md'), 'w', encoding='utf-8') as f:
        f.write('# Generica set: %s\n\nExtracted from `%s` by tools/extract_from_harvest.py.\n'
                '%d lists, %d labels.\n\n| category | list | labels | about |\n|---|---|---|---|\n'
                % (theme, os.path.basename(os.path.normpath(harvest)), len(rows), sum(len(l) for _, l in found.values())))
        f.write('\n'.join(rows) + '\n')
    print('%d lists, %d labels -> %s' % (len(rows), sum(len(l) for _, l in found.values()), out))


if __name__ == '__main__':
    main()
