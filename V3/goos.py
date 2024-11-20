import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)  
host = socket.gethostbyname('www.google.com')
port = 80
try:
    s.connect((host, port))
    print(f"Konektovao sam se na: {host} ({s.getsockname()})")
except socket.timeout:
    print("Konektovanje je predugo trajalo.")
    s.close()
    exit(1)
request = b"GET / HTTP/1.1\r\nHost: www.google.com\r\nConnection: close\r\n\r\n"
s.sendall(request)
chunks = []
while True:
    try:
        chunk = s.recv(4096) 
        if not chunk: 
            break
        chunks.append(chunk)
    except socket.timeout:
        print("Prijem podataka je predugo trajao")
        break
print("Svi podaci su primljeni")
val = b''.join(chunks).decode("utf8")
print("Header:")
print(val[:500])
try:
    header, body = val.split('\r\n\r\n', 1)
    with open("goo.html", "w") as file:
        file.write(body)
    print("\nBody:")
    print(body[:500]) 
except ValueError:
    print("Odgovor hosta nije u ocekivanom formatu (headre, body)")
    s.close()
    exit(1)
s.close()
