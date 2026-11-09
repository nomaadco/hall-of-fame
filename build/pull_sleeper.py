"""pull_sleeper.py - fetch the current CFFFL Sleeper season and save it as sleeper_current.json.

Python port of pull_sleeper_season.js, run by the weekly GitHub workflow (GitHub's
runners can reach api.sleeper.app; Claude's cloud container can't).

The league is found automatically: it starts from the newest league in sleeper.json and,
when Sleeper's NFL season has moved on, follows previous_league_id to the new year's league
by looking through the commissioner's leagues for that year.
"""
import json, time, urllib.request

API = 'https://api.sleeper.app/v1'
COMMISH_USER = '446054268240130048'   # Patrick Tighe's Sleeper user id


def j(path):
    for attempt in range(4):
        try:
            req = urllib.request.Request(API + path, headers={'User-Agent': 'cfffl-hall-of-fame'})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:
            if attempt == 3:
                raise
            print('retry', path, e)
            time.sleep(2 ** attempt)


def find_league(state):
    S = json.load(open('sleeper.json', encoding='utf-8'))
    newest = max(S['seasons'], key=lambda s: int(s['season']))
    league = newest['id']
    for year in range(int(newest['season']) + 1, int(state['league_season']) + 1):
        nxt = [l for l in (j(f'/user/{COMMISH_USER}/leagues/nfl/{year}') or [])
               if l.get('previous_league_id') == league]
        if not nxt:
            break            # new season's league not created yet; keep the last one
        league = nxt[0]['league_id']
        print('following league into', year, league)
    return league


def main():
    state = j('/state/nfl')
    league = find_league(state)
    L = j(f'/league/{league}')
    users = [[u['user_id'], u.get('display_name') or '', (u.get('metadata') or {}).get('team_name') or '']
             for u in j(f'/league/{league}/users')]
    rosters = []
    for r in j(f'/league/{league}/rosters'):
        s = r['settings']
        rosters.append([r['roster_id'], r['owner_id'], s.get('wins', 0), s.get('losses', 0), s.get('ties', 0),
                        round(s.get('fpts', 0) + (s.get('fpts_decimal') or 0) / 100, 2),
                        round(s.get('fpts_against', 0) + (s.get('fpts_against_decimal') or 0) / 100, 2)])
    done = L['status'] == 'complete'
    if done:
        lw = 17
    elif L['status'] in ('pre_draft', 'drafting'):
        lw = 0
    else:
        lw = max(0, (state['week'] if state['season'] == L['season'] else 18) - 1)
    weeks = {}
    for w in range(1, (17 if done else lw + 1) + 1):
        ms = j(f'/league/{league}/matchups/{w}')
        if ms:
            weeks[str(w)] = [[m['roster_id'], m.get('matchup_id'), m.get('points')] for m in ms]

    def br(a):
        return [[b.get('r'), b.get('m'), b.get('t1'), b.get('t2'), b.get('w'), b.get('l'), b.get('p')] for b in (a or [])]

    S = L['settings']
    season = {'season': L['season'], 'id': league, 'name': L['name'], 'status': L['status'],
              'total_rosters': L['total_rosters'], 'pws': S['playoff_week_start'],
              'prt': S.get('playoff_round_type'), 'pt': S.get('playoff_teams'), 'lw': lw,
              'users': users, 'rosters': rosters,
              'wb': br(j(f'/league/{league}/winners_bracket')), 'lb': br(j(f'/league/{league}/losers_bracket')),
              'weeks': weeks}
    if lw == 0 and not done:
        print('season', L['season'], 'has not started; nothing to merge')
        return
    json.dump(season, open('sleeper_current.json', 'w', encoding='utf-8'))
    print('saved season', L['season'], L['status'], 'last week', lw)


if __name__ == '__main__':
    main()
