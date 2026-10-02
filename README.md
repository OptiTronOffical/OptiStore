# OptiTron PS4 PKG Store

<a href="https://postimg.cc/LYMhyR24" target="_blank"><img src="https://i.postimg.cc/wv1JjTrN/Screenshot-2026-10-02-23-13-36.png" alt="Screenshot-2026-10-02-23-13-36"></a><br><br>
<a href="https://postimg.cc/G819Mrd9" target="_blank"><img src="https://i.postimg.cc/261vS8td/Screenshot-2026-10-02-23-13-15.png" alt="Screenshot-2026-10-02-23-13-15"></a><br><br>



**Free. No ads. No license keys. No nonsense.**  
Browse PS4 packages and install them directly to your console from your browser.

🌐 **Live Store:** [https://optistore.vercel.app](https://optistore.vercel.app)

---

## Why You'll Love It

- **100% Free** – Every feature is unlocked. No paywalls, no keys, no "premium" tiers.
- **Zero Ads** – No banners, no pop‑ups, no trackers. Just the catalog.
- **No Account Required** – Open the page and start browsing.
- **Direct PS4 Install** – Send `.pkg` files straight to your PS4 using Remote Package Installer (RPI).
- **Smart Link Handling** – Direct `.pkg` links get a **Send to PS4** button. Host pages get a **Download** button.
- **Batch Send** – Queue all direct packages for a game at once.
- **Open Source** – Self‑host it, modify it, make it yours.

---

## Support Future Projects

This store is a labor of love. If it saves you time and you'd like to see more projects like it — including a **PS5 PKG Store** — please consider donating.

**ETH / EVM Address:**  
`0x17E1D7f8A9641749A3f6A932Df09D36FE198df86`

Works on Ethereum, BSC, Polygon, and any EVM‑compatible chain.

Every donation goes toward keeping the project free and ad‑free, and toward building the next one. Thank you! 🙏

---

## How to Use

1. **Visit the store** at [https://optistore.vercel.app](https://optistore.vercel.app) or self‑host the files.
2. **Enter your PS4's IP** in the top panel and click **Save**.
3. **Click Test Connection** to verify RPI is reachable (green dot = good).
4. **Browse games** – search by title, filter by region or type.
5. **Click a game card** to see available files.
6. **Direct `.pkg` links** → click **🚀 Send to PS4**.
7. **Other links** → click **📥 Download** to open the host page.

> **⚠️ Important for remote install:** The PS4's RPI only speaks HTTP. Browsers block HTTP requests from HTTPS pages. If you're using the hosted version (which is HTTPS), the **Send to PS4** buttons may be blocked. For full functionality, run the store locally over plain HTTP (see below).

---

## Self‑Hosting (Recommended for Full PS4 Support)

To use the remote install features, serve the page over **plain HTTP** on your local network.

1. Download `index.html` and your `export_with_covers.json` catalog.
2. Put them in the same folder.
3. Start a simple HTTP server:
   - **Python 3:** `python -m http.server 8080`
   - **Node:** `npx serve`
   - **PHP:** `php -S localhost:8080`
4. Open `http://localhost:8080` in your browser.
5. Enter your PS4 IP, save, and enjoy.

---

## Catalog Format

The store reads a JSON file with a `records` array. Example:

```json
{
  "records": [
    {
      "name": "Game Title",
      "cover_image": "https://example.com/cover.jpg",
      "source": "SuperPSX",
      "title_id": "CUSA12345",
      "release_links": [
        {
          "url": "https://example.com/game.pkg",
          "kind": "pkg",
          "region": "EUR",
          "size": "10 GB",
          "source_label": "Base Game"
        },
        {
          "url": "https://mega.nz/file/abc123",
          "kind": "pkg",
          "region": "USA",
          "size": "10 GB",
          "source_label": "Mirror (Mega)"
        }
      ]
    }
  ]
}
```

- `url` ending in `.pkg` → **Send to PS4** button.
- Any other URL → **Download** button.
- `cover_image` is optional; a placeholder is shown if missing.

---

## Troubleshooting

**"Blocked by the browser" / mixed‑content error**  
You're on HTTPS. Serve the page over HTTP (see self‑hosting above).

**"Could not reach PS4"**  
- Check the PS4 IP.
- Make sure Remote Package Installer is running on port `12800`.
- Ensure both devices are on the same network.
- Temporarily disable firewalls blocking port `12800`.

**Catalog doesn't load**  
- Don't open the file as `file://` – use a web server.
- Check that `export_with_covers.json` is in the same folder.
- Look for CORS or 404 errors in the browser console.

---

## License

MIT – free to use, modify, and share.

---

## Disclaimer

This project is for educational and personal use only. You are responsible for complying with all applicable laws and the terms of service of any third‑party sites. Only use it with content you legally own or have permission to download. The authors assume no liability for misuse.

---

**Enjoy the store? Don't forget to donate to support the next project!**  
`0x17E1D7f8A9641749A3f6A932Df09D36FE198df86`
