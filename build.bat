@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo Building executable...
pyinstaller --noconfirm --onefile --windowed --name "CotizadorProtemax2026" --add-data "packing_list_generator;packing_list_generator" launcher.py

echo Build complete. The executable is in the dist folder.
pause
