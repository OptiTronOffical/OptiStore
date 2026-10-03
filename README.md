[![Screenshot-2026-10-03-18-30-13.png](https://i.postimg.cc/K87XFdCx/Screenshot-2026-10-03-18-30-13.png)](https://postimg.cc/v4m2tSQN)


==========================================================
OptiStore — Deploying over HTTP
==========================================================



[![fix.png](https://i.postimg.cc/GhV3HwMg/fix.png)](https://postimg.cc/w75YGPYD)

FILES
-----
  index.html               Library browser (open on PC)
  ps4.html                 Full catalog installer (open on PS4)
  rpi.html                 Standalone .pkg sender (open on PS4 or PC)
  export_with_covers.json  Catalog for index.html (you provide)
  games.json               Catalog for ps4.html   (you provide)
  README.txt               This file

SERVE OVER PLAIN HTTP — NOT HTTPS
---------------------------------
The install request goes to the PS4's RPI at
    http://<PS4-IP>:12800/api/install
If your page is served over HTTPS, the browser will block the
request as mixed content. Use HTTP only.

EASY LOCAL SERVER (Python 3)
----------------------------
  cd optistore
  python -m http.server 8000
Then on your PC open:
    http://localhost:8000/
On your PS4's browser open:
    http://<PC-LAN-IP>:8000/ps4.html
    http://<PC-LAN-IP>:8000/rpi.html

EASY LOCAL SERVER (Node)
------------------------
  npx serve -p 8000
or
  npx http-server -p 8000

PUBLISHING TO THE WEB
---------------------
Any static host that allows plain HTTP works:
  - GitHub Pages .........  HTTPS only  ✗ (blocks RPI)
  - Netlify ..............  HTTPS only  ✗
  - Vercel ...............  HTTPS only  ✗
  - Cloudflare Pages .....  HTTPS only  ✗
  - Your own VPS .........  HTTP yes    ✓
  - LAN / home server ....  HTTP yes    ✓
  - IPFS via http gateway   HTTP yes    ✓
  - ngrok http <port> .....  HTTP yes    ✓

On a VPS with Nginx, put the files in /var/www/optistore and use:

    server {
        listen 80;
        server_name your-host.example;
        root /var/www/optistore;
        index index.html;
        location / {
            try_files $uri $uri/ =404;
        }
    }

USING THE SITE
--------------
1. On your PC, open  http://your-host/
   - Browse the catalog, filter by region / kind, click a game
     to see every .pkg URL it has.

2. On the PS4, make sure Remote Package Installer (RPI) is
   running. It listens on port 12800.

3. Open  http://your-host/ps4.html  on the PS4 browser.
   - Tap a game, then tap "Send to PS4".
   - If your PS4 is on 127.0.0.1, leave the IP as-is.
   - Otherwise tap the pill in the top-right and enter the
     console's LAN IP (e.g. 192.168.1.42).

4. For one-off .pkg URLs, open  http://your-host/rpi.html
   on the PS4, paste the URL, and tap Send.

TROUBLESHOOTING
---------------
  "Timed out talking to <ip>:12800"
      → RPI isn't running, wrong IP, or firewall is blocking
        port 12800. Verify from a PC: curl http://<ip>:12800/

  "Request sent — no readable reply"
      → Almost always means it actually worked. Look at the
        PS4 notifications — the download should be queued.

  Card is greyed out in ps4.html
      → IP field is empty; open the settings pill and set it.

  Page loads but no games
      → export_with_covers.json / games.json missing or
        malformed. Check the browser console for parse errors.
