# CFFFL Hall of Fame

Live at https://nomaadco.github.io/hall-of-fame/

## Weekly updates

`.github/workflows/weekly-update.yml` runs every Wednesday at 15:00 UTC. It pulls the
current season from the Sleeper API (`build/pull_sleeper.py`), rebuilds `index.html`
(`build/build_hof.py`), and commits only when something changed. GitHub Pages then
republishes the site. To run it right away: **Actions → Weekly Sleeper update → Run workflow**.

When a new Sleeper season's league is created, the pull script follows it automatically
through `previous_league_id`.

## Building by hand

```
cd build
pip install openpyxl
python build_hof.py                               # rebuild from build/sleeper.json
python build_hof.py --merge sleeper_current.json  # merge a fresh pull first
```

`build/hof_template.html` holds the page layout; all UI changes go there.
