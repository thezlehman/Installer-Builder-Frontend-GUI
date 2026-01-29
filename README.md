# Installer Builder Frontend GUI

A simple GUI front-end for generating installer scripts for **Inno Setup** or **NSIS**, and optionally invoking their compilers.

## Features

- **Application metadata**
  - App name, version, publisher
  - Application directory (where your built binaries live)
  - Main EXE
  - License text file (optional)
  - Output directory for scripts/installer
- **Installer options**
  - Choose **Inno Setup** or **NSIS**
  - Create desktop shortcut
  - Create Start Menu shortcut
- **Compiler paths**
  - Configure paths to `ISCC.exe` (Inno Setup) and `makensis.exe` (NSIS)
- **Script generation**
  - Generate `.iss` script for Inno Setup
  - Generate `.nsi` script for NSIS
  - Show script in a preview/log window
- **Build installer (optional)**
  - If compiler path is valid, runs it to build the installer

## Requirements

- Windows 10/11
- Python 3.6+ (tkinter included)
- For building installers (optional):
  - [Inno Setup](https://jrsoftware.org/isinfo.php) (for ISCC.exe)
  - [NSIS](https://nsis.sourceforge.io/) (for makensis.exe)

## Running

From this folder:

```bash
python installerbuildergui.py
```

Or on Windows, double-click `run_installerbuilder.bat`.

## Notes

- This tool is **not** a full installer authoring environment; it focuses on generating basic, readable scripts suitable for small projects and demos.
- You can further customize the generated scripts manually in Inno Setup or NSIS if needed.

