# CFFFL Hall of Fame

Live at https://carversfinest.com (the old https://nomaadco.github.io/hall-of-fame/ address forwards there).

## Custom domain

`CNAME` holds `carversfinest.com`, and `deploy.yml` copies it into the published site. Because Pages
publishes from GitHub Actions, the domain itself is set in **Settings → Pages → Custom domain**; the
file is a record of it. DNS at the registrar: four `A` records for `@` (185.199.108.153, 185.199.109.153,
185.199.110.153, 185.199.111.153), four `AAAA` records for `@` (2606:50c0:8000::153, 2606:50c0:8001::153,
2606:50c0:8002::153, 2606:50c0:8003::153) and a `CNAME` for `www` pointing to `nomaadco.github.io`.

## Weekly updates

`.github/workflows/weekly-update.yml` runs every Wednesday at 15:00 UTC. It pulls the
current season from the Sleeper API (`build/pull_sleeper.py`), rebuilds `index.html`
(`build/build_hof.py`), and commits only when something changed. GitHub Pages then
republishes the site (see below). To run it right away: **Actions → Weekly Sleeper update → Run workflow**.

When a new Sleeper season's league is created, the pull script follows it automatically
through `previous_league_id`.

## League password

The live site is locked with one shared league password.
`.github/workflows/deploy.yml` encrypts `index.html` with [StatiCrypt](https://github.com/robinmoisson/staticrypt)
and publishes it to GitHub Pages. The password lives only in the repo secret `SITE_PASSWORD`
(**Settings → Secrets and variables → Actions**), never in the code. To change it, update the
secret and run **Actions → Publish site (password protected) → Run workflow**. Everyone will
need the new password.

Pages must be set to **Settings → Pages → Source: GitHub Actions**.

Note: this repo is public, so the source files (including `index.html` and `build/*.json`)
can still be read on GitHub. The password only locks the website.

## Building by hand

```
cd build
pip install openpyxl
python build_hof.py                               # rebuild from build/sleeper.json
python build_hof.py --merge sleeper_current.json  # merge a fresh pull first
```

`build/hof_template.html` holds the page layout; all UI changes go there.
