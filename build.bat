@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo Building executable...
pyinstaller --noconfirm --onefile --windowed --name "CotizadorProtemax2026" --add-data "app_source;app_source" launcher.py

echo Build complete. The executable is in the dist folder.
pause
