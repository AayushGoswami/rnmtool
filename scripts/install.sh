#!/usr/bin/env bash
# rnmtool Installer for Linux and macOS
# Run this in your terminal:
#   curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/rnmtool/main/scripts/install.sh | bash

set -e

echo ""
echo "===================================="
echo "  rnmtool Installer for Linux/macOS"
echo "===================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed."
    echo "        Install it from https://python.org/downloads/ or via your package manager."
    exit 1
fi

PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "[OK] Python $PY_VERSION found."

# Install pipx if not present
if ! command -v pipx &> /dev/null; then
    echo "[INFO] pipx not found. Installing pipx..."
    python3 -m pip install --user pipx --quiet
    python3 -m pipx ensurepath
    echo "[OK] pipx installed."
else
    echo "[OK] pipx already installed."
fi

# Install rnmtool
echo ""
echo "[INFO] Installing rnmtool via pipx..."
pipx install rnmtool

echo ""
echo "===================================="
echo "  Installation complete!"
echo "===================================="
echo ""
echo "  Restart your terminal (or run: source ~/.bashrc)"
echo "  Then try: rnmtool --help"
echo ""
