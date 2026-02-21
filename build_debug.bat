@echo off
echo Building DEBUG executable (console mode)...
pyinstaller --noconfirm --onefile --console --name "Cotizador_DEBUG" --add-data "app_source;app_source" launcher_debug.py

echo Build complete. The DEBUG executable is in the dist folder.
pause
