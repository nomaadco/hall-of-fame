"""build_hof.py - rebuild the CFFFL Hall of Fame site page (../index.html).

Run from this build/ folder:
  python build_hof.py                              # rebuild from sleeper.json as it is
  python build_hof.py --merge sleeper_current.json # first replace that season in sleeper.json
Also writes cfffl-hall-of-fame.html (the same page without the outer HTML skeleton),
which is what gets published to the Claude artifact.
"""
import json, os, subprocess, sys

args = sys.argv[1:]
if '--merge' in args:
    path = args[args.index('--merge') + 1]
    if os.path.exists(path):
        new = json.load(open(path, encoding='utf-8'))
        S = json.load(open('sleeper.json', encoding='utf-8'))
        S['seasons'] = [new] + [s for s in S['seasons'] if s['season'] != new['season']]
        S['seasons'].sort(key=lambda s: -int(s['season']))
        S['state'] = {'season': new['season'], 'week': new['lw'] + 1,
                      'season_type': 'post' if new['status'] == 'complete' else 'regular'}
        json.dump(S, open('sleeper.json', 'w', encoding='utf-8'))
        print('merged season', new['season'], new['status'], 'lw', new['lw'])
    else:
        print('no', path, '- building from sleeper.json as it is')

subprocess.run([sys.executable, 'gen_data.py'], check=True)   # ESPN/Yahoo + Sleeper -> hof_data.json
t = open('hof_template.html', encoding='utf-8').read()
page = (t.replace('__DATA__', open('hof_data.json', encoding='utf-8').read())
         .replace('__EXTRA__', open('extra_data.json', encoding='utf-8').read())
         .replace('__DG__', json.dumps({'2026': json.load(open('dg2026.json', encoding='utf-8'))})))
open('cfffl-hall-of-fame.html', 'w', encoding='utf-8').write(page)

# Standalone page for GitHub Pages: first line of the build is <title>, which goes in <head>.
title, rest = page.split('\n', 1)
site = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        + title + '\n</head>\n<body>\n' + rest + '\n</body>\n</html>\n')
open(os.path.join('..', 'index.html'), 'w', encoding='utf-8').write(site)
d = json.load(open('hof_data.json', encoding='utf-8'))
print('built index.html:', len(d['games']), 'games; in progress:', d['inprogress'])
