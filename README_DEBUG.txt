# Cotizador Protemax 2026 - Guía de Depuración (Solución de Problemas)

Si el ejecutable principal no funciona, sigue estos pasos para identificar el problema:

1. Ejecuta el archivo `build_debug.bat`.
   - Esto creará un nuevo ejecutable en la carpeta `dist` llamado `Cotizador_DEBUG.exe`.

2. Abre la carpeta `dist` y ejecuta `Cotizador_DEBUG.exe`.
   - Verás una ventana negra (consola) con información detallada sobre lo que está sucediendo.
   - Si ocurre un error, la ventana permanecerá abierta para que puedas leer el mensaje.

3. Revisa el archivo `debug.log`.
   - Se creará un archivo llamado `debug.log` en la misma carpeta donde ejecutes el programa.
   - Este archivo contiene información técnica que puedes enviar al desarrollador para solucionar el problema.

## Errores Comunes

- **Directory not found**: Significa que los archivos de la aplicación no se copiaron correctamente dentro del ejecutable.
- **Port in use**: El puerto 20260 está ocupado por otra aplicación. El sistema intentará usar otro puerto automáticamente.
- **Browser error**: No se pudo abrir el navegador web predeterminado. Intenta abrir la dirección URL (http://127.0.0.1:20260) manualmente.
