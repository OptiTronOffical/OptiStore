# OptiStore

OptiStore is a locally hosted web app for browsing the included PS4 and PS5
catalogs. Its launcher starts a small HTTP server on your computer, opens the
app in your browser, and shows the local network address so another device on
the same Wi-Fi/LAN can access it.

## Screenshots

<a href="https://postimg.cc/5QMB5852" target="_blank"><img src="https://i.postimg.cc/0jzVsfbD/ps5.png" alt="PS5 library"></a><br><br>
<a href="https://postimg.cc/BLF51mF3" target="_blank"><img src="https://i.postimg.cc/xCx6h7TX/ps5pkg.png" alt="PS5 packages"></a><br><br>
<a href="https://postimg.cc/q6dsc2cB" target="_blank"><img src="https://i.postimg.cc/sxMTrcvW/ps4.png" alt="PS4 library"></a><br><br>
<a href="https://postimg.cc/5Yz5Fsz6" target="_blank"><img src="https://i.postimg.cc/j5gMm9dQ/ps4pkg.png" alt="PS4 packages"></a>

## Run on Windows

Build `OptiStore.exe` using the steps below, then double-click it. The app
opens at `http://localhost:8000/`. Keep the console
window open while using the app; close it or press **Ctrl+C** to stop the server.

If port 8000 is already in use, OptiStore tries the next available port and
prints the address it selected. To use the app from another device, open the
**local network** address printed in that window. If Windows Firewall asks,
allow access on your private network.

The executable contains the app and catalog files, so Python is not required on
the computer that runs it. It is built for Windows; use the source instructions
below on other operating systems.

## Build the Windows executable

On a Windows machine with Python 3.10 or newer installed:

1. Put the project files in one folder.
2. Double-click `build-windows.bat`.
3. Find the standalone executable at `dist\OptiStore.exe`.

The build script installs PyInstaller and packages `index.html` and all three
catalogs into a single-file executable. Copy that executable to another
Windows machine and run it there.

## Run from source

Python 3.10 or newer is required. From the project folder, run:

```bash
python server.py
```

Then open the URL printed by the launcher. You can choose a starting port or
skip opening the browser automatically:

```bash
python server.py --port 8080 --no-browser
```

## Build and run on Linux

On Linux, build a native executable with:

```bash
./build-linux.sh
```

This creates `dist/OptiStore`. Run it with:

```bash
./dist/OptiStore
```

The build script installs PyInstaller in a local `.venv-build` folder. The
result is for the Linux architecture and system used to build it; build
separately on Windows for `OptiStore.exe`.

## Catalog files

- `export_with_covers.json` and `games.json` provide the PS4 library data.
- `ps5-catalog.json` provides the PS5 library data.

The launcher bundles the included versions. For a source run, replace these
files next to `server.py` with your own catalog data before starting it.

## Network use

The server listens on all network interfaces so devices on the same local
network can reach it. The address printed as `On this computer` is for the
computer running OptiStore; `On your local network` is for other devices.
The server is plain HTTP and is intended for trusted local networks.

## Disclaimer

OptiStore is an index, not a source. It displays links to third-party locations
and does not host or distribute package files. You are responsible for the
catalog data you use and for complying with the laws that apply where you live.
