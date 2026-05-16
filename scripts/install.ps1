# rnmtool Windows Installer
# Run this in PowerShell:
#   irm https://raw.githubusercontent.com/YOUR_USERNAME/rnmtool/main/scripts/install.ps1 | iex

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  rnmtool Installer for Windows"      -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Python is not installed or not on PATH." -ForegroundColor Red
    Write-Host "        Download Python from https://python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

$pyVersion = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
Write-Host "[OK] Python $pyVersion found." -ForegroundColor Green

# Install pipx if not present
if (-not (Get-Command pipx -ErrorAction SilentlyContinue)) {
    Write-Host "[INFO] pipx not found. Installing pipx..." -ForegroundColor Yellow
    python -m pip install --user pipx --quiet
    python -m pipx ensurepath
    Write-Host "[OK] pipx installed." -ForegroundColor Green
} else {
    Write-Host "[OK] pipx already installed." -ForegroundColor Green
}

# Install rnmtool
Write-Host ""
Write-Host "[INFO] Installing rnmtool via pipx..." -ForegroundColor Yellow
pipx install rnmtool

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "====================================" -ForegroundColor Green
    Write-Host "  Installation complete!" -ForegroundColor Green
    Write-Host "====================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Open a NEW terminal window and run:" -ForegroundColor White
    Write-Host "    rnmtool --help" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "[ERROR] Installation failed. Please check the output above." -ForegroundColor Red
    exit 1
}
