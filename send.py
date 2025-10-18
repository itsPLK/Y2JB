import socket
import sys

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
    
    send_js_payload(host, port, js_file)
