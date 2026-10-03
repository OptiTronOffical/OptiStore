# OptiStore

A browser-based front end for the PS4's **Remote Package Installer (RPI)**.
Browse a catalog of `.pkg` files on your PC, then push them straight to your
console from the PS4 browser.

> [!WARNING]
> **Serve this over plain HTTP — never HTTPS.**
> Install requests go to the console's RPI at `http://<PS4-IP>:12800/api/install`.
> If the page itself is served over HTTPS, the browser blocks that request as
> mixed content, and nothing will install.

---

## Status

**The library is complete and functional as of now.** Everything documented
below works, and the catalogs are ready to use.

`ps4.html` ships with **direct Internet Archive links** for its catalog, so
games can be pulled straight from archive.org without any intermediate host.

> [!NOTE]
> Sending to RPI from the PS4 browser was an oversight on the author's part.
> Full **GoldHEN** support is being enabled, which is the intended path for
> installing on console. See [GoldHEN setup](#goldhen-setup) below.

---

## Screenshots

<a href="https://postimg.cc/VSKZJJJr" target="_blank"><img src="https://i.postimg.cc/RFBkbf9R/Screenshot-2026-10-04-00-00-44.png" alt="Screenshot-2026-10-04-00-00-44"></a><br><br>
<a href="https://postimg.cc/HJ6vrrrx" target="_blank"><img src="https://i.postimg.cc/JnLfdJmb/Screenshot-2026-10-04-00-02-25.png" alt="Screenshot-2026-10-04-00-02-25"></a><br><br>
<a href="https://postimg.cc/d75Nhhh7" target="_blank"><img src="https://i.postimg.cc/76kFQ7DN/Screenshot-2026-10-04-00-02-35.png" alt="Screenshot-2026-10-04-00-02-35"></a><br><br>
<a href="https://postimg.cc/gwgtxxxx" target="_blank"><img src="https://i.postimg.cc/Y9H5ygkz/Screenshot-2026-10-04-00-02-48.png" alt="Screenshot-2026-10-04-00-02-48"></a><br><br>
<a href="https://postimg.cc/jWM3DDDq" target="_blank"><img src="https://i.postimg.cc/SshBt8q9/Screenshot-2026-10-04-00-05-02.png" alt="Screenshot-2026-10-04-00-05-02"></a>

---

## Contents

- [Files](#files)
- [Requirements](#requirements)
- [GoldHEN setup](#goldhen-setup)
- [Quick start](#quick-start)
- [Deploying to the web](#deploying-to-the-web)
- [Using the site](#using-the-site)
- [Troubleshooting](#troubleshooting)
- [Disclaimer](#disclaimer)
- [Support](#support)

---

## Files

| File | Purpose | Open on |
| --- | --- | --- |
| `index.html` | Library browser — filter by region/kind, inspect every `.pkg` URL | PC |
| `ps4.html` | Full catalog installer with direct Internet Archive links | PS4 |
| `rpi.html` | Standalone sender for one-off `.pkg` URLs | PS4 or PC |
| `export_with_covers.json` | Catalog consumed by `index.html` | *(you provide)* |
| `games.json` | Catalog consumed by `ps4.html` | *(you provide)* |
| `README.md` | This file | — |

---

## Requirements

- **GoldHEN** running on the PS4 (see [GoldHEN setup](#goldhen-setup)).
- A way to serve static files over **HTTP** (Python 3, Node, or any web host).
- PC and PS4 on the same LAN (for local hosting).

---

## GoldHEN setup

For OptiStore to work end-to-end, enable the following in GoldHEN and the PS4
debug settings:

1. **Payload server** — enable it in GoldHEN.
2. **FTP server** — enable it in GoldHEN.
3. **Background downloads** — enable it in **Debug Settings** on the PS4.

With these three enabled, installs queue properly and can run in the background
while you keep using the console.

---

## Quick start

### 1. Serve the files

Pick whichever you have installed:

**Python 3**

```bash
cd optistore
python -m http.server 8000
```

**Node**

```bash
npx serve -p 8000
# or
npx http-server -p 8000
```

### 2. Open it on your PC

```
http://localhost:8000/
```

### 3. Open it on your PS4

Make sure GoldHEN is running with the settings above applied, then in the PS4
browser:

```
http://<PC-LAN-IP>:8000/ps4.html     # full catalog installer
http://<PC-LAN-IP>:8000/rpi.html     # single .pkg sender
```

> **Tip:** `ps4.html` uses direct Internet Archive links, so no intermediate
> host is required for catalog installs. For one-off URLs, use `rpi.html`.

---

## Deploying to the web

Because the RPI endpoint is plain HTTP, **your host must allow plain HTTP**.

| Host | Plain HTTP? | Works? |
| --- | --- | --- |
| GitHub Pages | HTTPS only | ✗ |
| Netlify | HTTPS only | ✗ |
| Vercel | HTTPS only | ✗ |
| Cloudflare Pages | HTTPS only | ✗ |
| Your own VPS | Yes | ✓ |
| LAN / home server | Yes | ✓ |
| IPFS via HTTP gateway | Yes | ✓ |
| `ngrok http <port>` | Yes | ✓ |

### Nginx example (VPS)

Put the files in `/var/www/optistore` and use:

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

## Using the site

1. **On your PC**, open `http://your-host/`.
   Browse the catalog, filter by region or kind, and click a game to see every
   `.pkg` URL it has.

2. **On your PS4**, confirm GoldHEN is running with payload server, FTP server,
   and background downloads enabled.

3. Open `http://your-host/ps4.html` in the PS4 browser.
   - Tap a game, then tap **Send to PS4**.
   - Catalog entries pull directly from the Internet Archive.

4. For a one-off `.pkg` URL, open `http://your-host/rpi.html` on the PS4,
   paste the URL, and tap **Send**.

---

## Troubleshooting

**"Timed out talking to `<ip>:12800`"**
RPI isn't running, the IP is wrong, or a firewall is blocking port 12800.
Verify from a PC:

```bash
curl http://<ip>:12800/
```

**"Request sent — no readable reply"**
Almost always means it actually worked. Check the PS4 notifications — the
download should be queued.

**Card is greyed out in `ps4.html`**
The IP field is empty. Open the settings pill and set it.

**Page loads but no games appear**
`export_with_covers.json` / `games.json` is missing or malformed. Check the
browser console for parse errors.

**Downloads don't continue in the background**
Enable **background downloads** in the PS4's Debug Settings, and confirm the
FTP and payload servers are enabled in GoldHEN.

---

## Disclaimer

**OptiStore is an index, not a source.**

The library is a browsable list of links. The author does not host, upload,
mirror, or distribute any `.pkg` file, game, or other content, and no files
are bundled with this project. Every catalog entry points to a third-party
location — in the case of `ps4.html`, directly to the **Internet Archive**.

**No copyrighted material is provided here.** The author has not supplied any
material that is not already public domain. The catalogs
(`export_with_covers.json`, `games.json`) are supplied by **you** or by third
parties; OptiStore simply reads and displays them.

**You are responsible for your library.** What you load into the catalog, what
you choose to install, and how you use the console are entirely your decisions.
It is your responsibility to ensure you have the right to access and use
anything you add, and to comply with the laws that apply where you live. The
author accepts no responsibility or liability for your use of this tool, the
content you point it at, or any consequences that follow.

**The author's only contribution is their time** — writing the code, assembling
the browser, and documenting it. If the library saved you some of yours,
consider supporting that effort:

```
ETH: 0x17E1D7f8A9641749A3f6A932Df09D36FE198df86
```

---

## Support

Donations are appreciated and go toward continued work on the tool:

```
ETH: 0x17E1D7f8A9641749A3f6A932Df09D36FE198df86
```
