
# OptiStore

A browser-based front end for browsing PS4 and PS5 package libraries, with direct download links for every base game, update, DLC, and theme.

Now combined both repos, enjoy

## Screenshots
<a href="https://postimg.cc/5Yg9sWvK" target="_blank"><img src="https://i.postimg.cc/8cQFP1CG/Screenshot-2026-10-07-00-57-29.png" alt="Screenshot-2026-10-07-00-57-29"></a><br><br>
<a href="https://postimg.cc/7G9PKr7s" target="_blank"><img src="https://i.postimg.cc/Bb98Qqv0/Screenshot-2026-10-07-00-57-41.png" alt="Screenshot-2026-10-07-00-57-41"></a><br><br>
<a href="https://postimg.cc/vgh80w93" target="_blank"><img src="https://i.postimg.cc/x8DkT0dD/Screenshot-2026-10-07-00-57-52.png" alt="Screenshot-2026-10-07-00-57-52"></a><br><br>
<a href="https://postimg.cc/q6dsc2cB" target="_blank"><img src="https://i.postimg.cc/sxMTrcvW/ps4.png" alt="ps4"></a><br><br>
<a href="https://postimg.cc/5Yz5Fsz6" target="_blank"><img src="https://i.postimg.cc/j5gMm9dQ/ps4pkg.png" alt="ps4pkg"></a><br><br>


---

## Status

The library is complete and functional. Two standalone pages ship with this project:

- **`index.html`** — PS4 package library. Drop `export_with_covers.json` (or `games.json`) next to it and browse every title, update, and DLC, with direct `.pkg` links and one-tap copy for external tools.
- **`ps5.html`** — PS5 package library. Loads three independent catalogs (`dlps.json`, `pippo.json`, `pfs.json`) via in-page tabs, with category filters, region filtering, Pippo link-lock detection, and archive-password help built in.

The PS4 page links to `ps5.html` from its topbar; both pages are self-contained and share no runtime dependencies.

---

## Contents

- [Files](#files)
- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Run as a local app](#run-as-a-local-app)
- [Deploying to the web](#deploying-to-the-web)
- [Using the PS4 library](#using-the-ps4-library)
- [Using the PS5 library](#using-the-ps5-library)
- [Catalog formats](#catalog-formats)
- [Passwords & link-locks](#passwords--link-locks)
- [Troubleshooting](#troubleshooting)
- [Disclaimer](#disclaimer)
- [Support](#support)

---

## Files

| File | Purpose | Open on |
| --- | --- | --- |
| `index.html` | PS4 library browser — filter by region / kind / size, inspect every `.pkg` URL 
| `ps5.html` | PS5 library browser — three catalogs (DLPSGAME, .exfat, PFS), category filters, password help
| `export_with_covers.json` | Primary PS4 catalog consumed by `index.html` | *(you provide)* |
| `games.json` | Fallback PS4 catalog for `index.html` | *(you provide)* |
| `dlps.json` | DLPSGAME catalog for `ps5.html` | *(you provide)* |
| `pippo.json` | `.exfat` catalog for `ps5.html` | *(you provide)* |
| `pfs.json` | PFS catalog for `ps5.html` (bundled per title ID) | *(you provide)* |
| `server.py` | Local app launcher — serves the pages and fetches the latest catalogs on start | PC |
| `build.py`, `build-windows.bat`, `build-linux.sh` | Build a standalone executable with PyInstaller | PC |
| `.github/workflows/build.yml` | GitHub Actions workflow that builds the executables | — |
| `README.md` | This file | — |

---

## Requirements

- A modern desktop or console browser (the pages use `content-visibility`, `aspect-ratio`, and ES2015+).

---


---

## Quick start

### 1. Serve the folder

**OptiStore launcher** (recommended — fetches the latest catalogs, see [Run as a local app](#run-as-a-local-app))

```bash
python server.py
```

**Python 3**

```bash
cd optistore
python3 -m http.server 8000
```

**Node**

```bash
npx serve -p 8000
# or
npx http-server -p 8000
```

### 2. Open it

```
http://localhost:8000/           # PS4 library
http://localhost:8000/ps5.html   # PS5 library
```

From another device on the LAN (e.g. your PS4 browser):

```
http://<PC-LAN-IP>:8000/
http://<PC-LAN-IP>:8000/ps5.html
```

### 3. Drop in your catalogs

Place `export_with_covers.json` (or `games.json`) next to `index.html`, and `dlps.json` / `pippo.json` / `pfs.json` next to `ps5.html`. The pages handle missing files gracefully — each will show a diagnostic panel with a **Choose JSON file** button so you can load a catalog straight from disk without restarting the server.

---

## Run as a local app

`server.py` is a small launcher that serves OptiStore on your computer, opens it
in your browser, and prints a LAN address so other devices (e.g. your PS4
browser) on the same network can use it.

### Run from source

Python 3.10 or newer is required. From the project folder:

```bash
python server.py
```

| Option | Effect |
| --- | --- |
| `--port 8080` | Starting port (default `8000`; the next free port is used if it's busy) |
| `--no-browser` | Don't open the browser automatically |
| `--offline` | Don't fetch catalogs; use the local copies only |
| `--catalog-source <url>` | Base URL to fetch catalogs from (default: this repo's `main` branch) |

Keep the window open while you use the app; press **Ctrl+C** to stop it. If
Windows Firewall asks, allow access on your private network.

### Always-fresh catalogs

Every time the launcher starts, it downloads the latest catalogs
(`export_with_covers.json`, `games.json`, `dlps.json`, `pippo.json`, `pfs.json`)
from the raw files in this repository:

```
https://raw.githubusercontent.com/OptiTronOffical/OptiStore/main/<file>.json
```

So updating a JSON in the repo is all it takes — nobody has to rebuild,
redeploy, or replace files by hand. Downloads are validated as JSON and cached
in a per-user folder (`%LOCALAPPDATA%\OptiStore\catalogs` on Windows,
`~/Library/Caches/OptiStore/catalogs` on macOS, `~/.cache/OptiStore/catalogs`
on Linux); unchanged files are skipped via ETag. If the network is unavailable,
the last cached copy is used, then the copy shipped with the app.

### Build an executable yourself

No prebuilt executables are published. You can build one in either of two ways.

**With GitHub Actions (no local Python needed).** The
[`Build executables`](.github/workflows/build.yml) workflow builds OptiStore for
Windows, Linux, and macOS with PyInstaller. Fork the repo, open the **Actions**
tab, pick **Build executables**, and click **Run workflow**. When it finishes,
download `OptiStore-windows`, `OptiStore-linux`, or `OptiStore-macos` from the
run's **Artifacts** section. The workflow also runs on pushes and pull requests
that change the launcher.

**Locally.** With Python 3.10+ installed:

- **Windows:** double-click `build-windows.bat` → `dist\OptiStore.exe`
- **Linux / macOS:** `./build-linux.sh` → `dist/OptiStore`

Both scripts install PyInstaller and run `build.py`, which bundles `index.html`,
`ps5.html`, and the catalogs into a single file. An executable only runs on the
OS (and CPU architecture) it was built on.

---

## Deploying to the web

Both pages are fully static, so any plain-HTTP host works. If you also add an RPI sender, **your host must allow plain HTTP** — HTTPS pages cannot talk to `http://<PS4-IP>:12800/`.

| Host | Plain HTTP? | Works? |
| --- | --- | --- |
| GitHub Pages | HTTPS only | ✗ (browsing only if HTTPS is acceptable) |
| Netlify | HTTPS only | ✗ |
| Vercel | HTTPS only | ✓ (browsing) |
| Cloudflare Pages | HTTPS only | ✗ |
| Your own VPS | Yes | ✓ |
| LAN / home server | Yes | ✓ |
| `ngrok http <port>` | Yes | ✓ |

### Nginx example (VPS)

```nginx
server {
    listen 80;
    server_name your-host.example;
    root /var/www/optistore;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

---

## Using the PS4 library

1. Open `index.html` in a browser.
2. **Search** by title or title ID, or use the **Region** dropdown and the **Kind** chips (Base, Update, DLC, Theme, Avatar, Demo, App, PKG) to narrow the list.
3. Sort by name, package count, or total size.
4. Click any card to open the detail modal:
   - Every `.pkg` is listed with its kind, direct/external status, size, version, region, minimum firmware, and host.
   - Files are sorted so **Base → Update → DLC** appear in install order.
   - **Copy all URLs** copies every link separated by newlines — handy for feeding an external downloader.
   - Each row has a 📋 button for one-off copies.
5. Hero stats show total titles, total packages, total size, and USA / EUR counts.

**Keyboard shortcuts**

| Key | Action |
| --- | --- |
| `/` | Focus the search box |
| `Enter` / `Space` | Open the focused card |
| `Esc` | Close the open modal |

---

## Using the PS5 library

`ps5.html` is a self-contained viewer with its own topbar, catalogs, filters, and modals.

### Catalogs

Three tabs, each loading its own file:

| Tab | File | Notes |
| --- | --- | --- |
| **DLPSGAME** | `dlps.json` | The default view on first load. |
| **.exfat** | `pippo.json` | Titles served from `.exfat`. Some links route through a Pippo link-lock page. |
| **PFS** | `pfs.json` | Entries are **grouped by title ID** — every version, category, and link for a title appears on a single card. |

The active tab is remembered in `localStorage`, so reloading lands you where you left off.

### Filtering & sorting

- **Search** matches against title and title ID.
- **Category chips** at the top of the grid are single-select quick filters (Game, DLC, Update, App, Theme, Demo).
- The **Filter** popover adds:
  - Multi-select category chips
  - Region dropdown (only regions present in the active catalog)
  - Toggles: *Has download links*, *Has Pippo link-lock*, *Contains an update*, *Contains DLC*, *Bundled releases only*
- The **Sort** popover offers Name A–Z / Z–A, Category, Most links, Title ID, and Recently updated.
- The active filter count appears as a badge on the Filter button.

### Freshness banner

Each catalog shows a banner with its last-modified timestamp (read from the JSON's `lastUpdated` field, the `Last-Modified` HTTP header, or the newest per-item `updatedAt`). A **Refresh** button reloads the active catalog without touching the other two.

### Update check

The green **Update** button in the topbar refetches **all three** catalogs and reports per-catalog deltas (`+N new`, `-N removed`, or `no changes`) as a rich toast. The baseline is stored in `localStorage` so the first run reports "baseline" instead of noise.

### Detail modal

Click any card to see:

- Category, region, version, and bundle count as chips.
- **Included in this release** — for PFS grouped items, a per-category breakdown (Game, DLC, Update, …) with each entry's version, link count, and size.
- **Release details** — parsed from the description field (Region, Firmware, Genre, Size, Versions, Password, Contributor, Release note, Updated) plus any extra `Key: Value` lines.
- **Download links** — with favicon, host, category tag, version tag, and per-link **Open** / **📋 Copy** buttons.

A pink callout appears automatically whenever any link goes through a Pippo host.

### Other features

- **Passwords** button (topbar, footer, and every detail modal) opens a modal listing archive passwords and the Pippo link-lock password.
- **Drag & drop** a `.json` file anywhere on the page to load it as the active catalog — no server round-trip.
- **Keyboard shortcuts**:

  | Key | Action |
  | --- | --- |
  | `/` | Focus search |
  | `Alt` + `1` / `2` / `3` | Switch to DLPSGAME / .exfat / PFS |
  | `U` | Trigger Update check |
  | `Esc` | Close popovers and modals |

---

## Catalog formats

The pages are tolerant of several JSON shapes. If you're generating a catalog, the simplest structures are below.

### PS4 (`export_with_covers.json`, `games.json`)

Either an array of records:

```json
{
  "lastUpdated": "2025-09-01T12:00:00Z",
  "records": [
    {
      "name": "Example Game",
      "title_id": "CUSA00000",
      "region": "USA",
      "cover_image": "https://…/cover.jpg",
      "release_links": [
        { "url": "https://…/base.pkg",   "kind": "base",   "size": "12.4 GB", "version": "1.00" },
        { "url": "https://…/patch.pkg",  "kind": "update", "size": "1.2 GB",  "version": "1.05" },
        { "url": "https://…/dlc01.pkg",  "kind": "dlc",    "size": "400 MB" }
      ]
    }
  ]
}
```

…or a `DATA` map of URL → metadata:

```json
{
  "DATA": {
    "https://…/game.pkg": {
      "name": "Example Game",
      "title_id": "CUSA00000",
      "region": "EUR",
      "cover_url": "https://…/cover.jpg",
      "size": "12.4 GB"
    }
  }
}
```

Recognised `kind` values (aliases accepted): `base`, `update` / `patch`, `dlc` / `addon`, `theme`, `avatar`, `demo`, `app`, and anything else falls back to `pkg`.

### PS5 (`dlps.json`, `pippo.json`, `pfs.json`)

```json
{
  "lastUpdated": "2025-09-01T12:00:00Z",
  "packages": [
    {
      "title": "Example PS5 Game",
      "titleId": "PPSA00000",
      "category": "game",
      "version": "1.00",
      "posterUrl": "https://…/poster.jpg",
      "sizeBytes": 45000000000,
      "description": "Region: USA\nFirmware: 4.50\nPassword: DLPSGAME.COM",
      "downloadLinks": [
        { "name": "Part 1", "url": "https://…/part1.pkg", "group": "Base", "version": "1.00" },
        { "name": "Part 2", "url": "https://…/part2.pkg", "group": "Base", "version": "1.00" }
      ]
    }
  ]
}
```

The parser also accepts:

- A bare array of objects (no `packages` wrapper).
- A `packages` map (object keyed by anything).
- A `DATA` map (object keyed by URL).
- `downloadLinks` as an array of objects or an array of plain URL strings.
- `files` in place of `downloadLinks`.

`category` values recognised: `game`, `dlc`, `update`, `app`, `theme`, `demo`. Anything else is grouped as "Other".

### Descriptions

In PS5 catalogs, the `description` string is parsed line-by-line. Any line in `Key: Value` form is lifted into a release-detail spec. Recognised keys:

- `Region`
- `Firmware`
- `Genre`
- `Password`
- `Contributor`
- `Release note` (or `Note`)
- `Updated` (or `Release date`)

Unknown `Key: Value` lines are shown verbatim under *Release details*.

---

## Passwords & link-locks

Two independent password systems are documented by the pages:

### DLPSGAME archive passwords

Shown in both the **Passwords** modal and the **Archive passwords** notice that opens on first visit. Current list is defined in `ps5.html` under `PASSWORDS_ARCHIVE`:

```js
var PASSWORDS_ARCHIVE = ['DLPSGAME.COM','downloadgameps3.com','hako','[DLPSGAME.COM]'];
```

To add or remove one, edit that array — the notice, the standalone modal, and the "Copy all passwords" button all read from it.

### Pippo link-lock password

Any URL whose host contains `pippo` (see `PIPPO_HOSTS` in `ps5.html`) is flagged as a link-lock. Those pages use the password:

```
pippo
```

**All lowercase** — `Pippo` and `PIPPO` are rejected by the lock. Cards and detail rows that contain a Pippo link show a pink hint, and the standalone Passwords modal repeats the warning.

To extend the host list, edit:

```js
var PIPPO_HOSTS = ['pippo','pippolink','pippo.link','pippo.onl', …];
```

---

## Troubleshooting

**"No PS4 catalog found" / "No PS5 catalog found"**

The JSON is missing or malformed. Check the browser console for a parse error, or click **Choose JSON file** in the diagnostic panel to load it from disk. If you're opening the HTML via `file://`, switch to an HTTP server — browsers block local JSON fetches from `file://`.

**PS5 tab shows "unavailable"**

That specific catalog file isn't next to `ps5.html`. The other tabs will still work — only the missing one shows the diagnostic view. Drop the file in and hit **Refresh**, or reload the page.

**Cards are blank / posters don't load**

Cover images are loaded lazily. If your JSON points at a host that blocks hotlinking, the image is removed silently and the placeholder letter stays visible. That's cosmetic — the download links still work.

**Search finds nothing**

The PS4 search matches title and title ID only. The PS5 search matches title and title ID. If you're pasting a package URL, that won't match — use the detail modal's 📋 button instead.

**The update toast shows "baseline"**

First run for that browser. The counts are now stored; the next Update click will show real deltas.

**Drag & drop isn't loading my file**

Only `.json` and `.txt` are accepted, and the file must be parseable JSON. Check the console — a parse error will also raise a red toast.

---

## Disclaimer

**OptiStore is an index, not a source.**

The library is a browsable list of links. The author does not host, upload, mirror, or distribute any `.pkg` file, game, or other content, and no files are bundled with this project. Every catalog entry points to a third-party location — including, in some catalogs, the Internet Archive.

**No copyrighted material is provided here.** The catalogs (`export_with_covers.json`, `games.json`, `dlps.json`, `pippo.json`, `pfs.json`) are supplied by public scrapes or third parties; OptiStore simply reads and displays them.

**You are responsible for your library.** What you load into the catalogs, what you choose to install, and how you use your console are entirely your decisions. It is your responsibility to ensure you have the right to access and use anything you add, and to comply with the laws that apply where you live. The author accepts no responsibility or liability for your use of this tool, the content you point it at, or any consequences that follow.

**The author's only contribution is their time** — writing the code, assembling the browser, and documenting it. If the library saved you some of yours, consider supporting that effort:

```
ETH: 0x17E1D7f8A9641749A3f6A932Df09D36FE198df86
```


## Support

- **Telegram:** [@OptiTronOffical](https://t.me/OptiTronOffical) — issues, questions, or custom project requests.
- **Coffee:** the Ethereum address above, or the **Donate me a coffee** button in the topbar of either page.
```
