import os
import sys
import webbrowser
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket
import logging

# Configure logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(console_handler)

PORT = 20260

def get_resource_path():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app
            # path into variable _MEIPASS.
            base_path = sys._MEIPASS
            logging.info(f"Running in frozen mode. _MEIPASS: {base_path}")
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            logging.info(f"Running in script mode. Base path: {base_path}")

        resource_path = os.path.join(base_path, 'app_source')
        logging.info(f"Calculated resource path: {resource_path}")
        return resource_path
    except Exception as e:
        logging.error(f"Error calculating resource path: {e}", exc_info=True)
        raise

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, directory=None):
    if directory:
        os.chdir(directory)
        logging.info(f"Changed working directory to: {directory}")

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
    print(message)
    # Try to show a message box on Windows
    if os.name == 'nt':
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, message, "Error", 0x10)
        except:
            pass

def main():
    try:
        logging.info("Starting Cotizador Launcher...")
        resource_path = get_resource_path()

        if not os.path.exists(resource_path):
            error_msg = f"Error: Directory {resource_path} not found."
            logging.error(error_msg)
            # List contents of parent dir for debugging
            parent_dir = os.path.dirname(resource_path)
            if os.path.exists(parent_dir):
                logging.info(f"Contents of {parent_dir}: {os.listdir(parent_dir)}")
            else:
                logging.error(f"Parent directory {parent_dir} does not exist either.")

            show_error(error_msg)
            input("Press Enter to exit...")
            sys.exit(1)
        else:
            logging.info(f"Resource directory exists. Contents: {os.listdir(resource_path)}")

        # Start server
        logging.info("Starting HTTP server...")
        httpd = run_server(directory=resource_path)
        port = httpd.server_port
        logging.info(f"Server started at http://127.0.0.1:{port}")

        # Run server in a separate thread
        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()

        # Open the browser
        if os.path.exists('index.html'):
            url = f'http://127.0.0.1:{port}/index.html'
        else:
            url = f'http://127.0.0.1:{port}/'
            logging.warning("index.html not found in working directory, opening root")

        logging.info(f"Opening browser at {url}")
        try:
            webbrowser.open(url)
        except Exception as e:
            logging.error(f"Could not open browser: {e}", exc_info=True)
            print(f"Could not open browser automatically. Please open: {url}")

        logging.info("Server running. Press Ctrl+C to stop.")

        # Keep the script running
        while True:
            time.sleep(1)

    except Exception as e:
        logging.critical(f"An unexpected fatal error occurred: {e}", exc_info=True)
        show_error(f"An unexpected error occurred: {e}\nCheck debug.log for details.")
        input("Press Enter to exit...")
        sys.exit(1)
    except KeyboardInterrupt:
        logging.info("Stopping server...")
        pass

if __name__ == "__main__":
    main()
