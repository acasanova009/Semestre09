import socket

host = "192.168.1.169"   # target IP
ports = [22, 80, 443, 9899]  # list of ports to check

for port in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((host, port))
        print(f"Port {port} is OPEN")
    except:
        print(f"Port {port} is CLOSED")
    finally:
        s.close()
