import socket
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# log server from: https://github.com/Gezine/Y2JB/blob/main/log.py
class LogHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default HTTP logging
    
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        log_msg = self.rfile.read(length).decode('utf-8')
        print(log_msg, flush=True)
        
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def start_logger(port=8080):
    """Start HTTP logger server in background thread"""
    server = HTTPServer(('0.0.0.0', port), LogHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"[+] Logger started on port {port}")
    return server

def send_js_payload(host, port, js_file_path):
    """
    Send JavaScript payload to the remote loader server.
    
    Args:
        host: Target IP address
        port: Target port number
        js_file_path: Path to JavaScript file to send
    """
    try:
        # Read the JavaScript file
        with open(js_file_path, 'r', encoding='utf-8') as f:
            js_code = f.read()
        
        print(f"[*] Read {len(js_code)} bytes from {js_file_path}")
        
        # Create socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        
        print(f"[*] Connecting to {host}:{port}...")
        sock.connect((host, port))
        print("[+] Connected!")
        
        # Send the payload
        print("[*] Sending payload...")
        sock.sendall(js_code.encode('utf-8'))
        print("[+] Payload sent successfully!")
        
        # Close connection
        sock.close()
        print("[+] Connection closed")
        
    except FileNotFoundError:
        print(f"[-] Error: File '{js_file_path}' not found")
        sys.exit(1)
    except ConnectionRefusedError:
        print(f"[-] Error: Connection refused to {host}:{port}")
        sys.exit(1)
    except socket.timeout:
        print(f"[-] Error: Connection timeout")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python send.py <host> <port> <js_file>")
        print("Example: python send.py 192.168.1.100 9999 payload.js")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    js_file = sys.argv[3]
    
    # Start logger first
    logger_server = start_logger(8080)
    print("[*] Logger is ready to receive logs\n")
    
    # Send payload
    send_js_payload(host, port, js_file)
    
    # Keep logger running
    print("\n[*] Waiting for logs... (Press Ctrl+C to exit)")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
        logger_server.shutdown()
