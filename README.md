# Cotizador Protemax 2026 - Guía de Instalación

Este proyecto contiene el código fuente del Cotizador Protemax 2026 y las herramientas necesarias para convertirlo en un archivo ejecutable (.exe) para Windows.

## Requisitos Previos

1. **Python**: Necesitas tener Python instalado en tu computadora. Puedes descargarlo gratis desde [python.org](https://www.python.org/downloads/). Asegúrate de marcar la casilla "Add Python to PATH" durante la instalación.

## Instrucciones para Crear el Ejecutable (.exe)

Sigue estos pasos sencillos para generar el archivo `CotizadorProtemax2026.exe`:

1. **Descarga y extrae los archivos**: Descarga todos los archivos de este proyecto en una carpeta de tu computadora (por ejemplo, en el Escritorio).
2. **Ejecuta el script de construcción**:
   - Busca el archivo llamado `build.bat` en la carpeta.
   - Haz doble clic sobre él.
   - Se abrirá una ventana negra (consola) que instalará las herramientas necesarias y creará el ejecutable.
   - Espera a que termine. Verás un mensaje que dice "Build complete".
3. **Encuentra tu ejecutable**:
   - Una vez finalizado, verás una nueva carpeta llamada `dist`.
   - Dentro de esa carpeta encontrarás el archivo `CotizadorProtemax2026.exe`.
   - ¡Listo! Ya puedes copiar ese archivo y usarlo donde quieras.

## Solución de Problemas

- Si `build.bat` se cierra inmediatamente, intenta abrirlo desde una consola de comandos (CMD) para ver el error.
- Asegúrate de tener conexión a internet la primera vez para que pueda descargar `pyinstaller`.

---
Generado por tu Asistente de Ingeniería de Software.
