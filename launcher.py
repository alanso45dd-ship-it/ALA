import os
import sys
import webbrowser
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket
import logging

# Basic logging even for production
logging.basicConfig(filename='cotizador.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

PORT = 20260

def get_resource_path():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, 'app_source')

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, directory=None):
    if directory:
        os.chdir(directory)

    # Try the fixed port first
    port_to_use = PORT
    if is_port_in_use(port_to_use):
        logging.warning(f"Port {port_to_use} is in use. Trying random port...")
        port_to_use = 0 # Let OS pick a random port if default is taken

    server_address = ('127.0.0.1', port_to_use)
    httpd = server_class(server_address, handler_class)
    return httpd

def show_error(message):
    logging.error(message)
    # Try to show a message box on Windows
    if os.name == 'nt':
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, message, "Error", 0x10)
        except:
            pass

def main():
    try:
        resource_path = get_resource_path()
        logging.info(f"Resource path: {resource_path}")

        if not os.path.exists(resource_path):
            show_error(f"Error: Directory {resource_path} not found.")
            sys.exit(1)

        # Start server
        httpd = run_server(directory=resource_path)
        port = httpd.server_port
        logging.info(f"Server started on port {port}")

        # Run server in a separate thread
        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()

        # Open the browser
        if os.path.exists('index.html'):
            url = f'http://127.0.0.1:{port}/index.html'
        else:
            url = f'http://127.0.0.1:{port}/'

        try:
            webbrowser.open(url)
        except Exception as e:
            logging.error(f"Could not open browser: {e}")

        # Keep running
        while True:
            time.sleep(1)

    except Exception as e:
        show_error(f"An unexpected error occurred: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
