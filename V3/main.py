
import socket
s=socket.socket()
host=socket.gethostbyname('www.google.com')
port=80
s.connect((host,port))
s.sendall(b"GET /\r\n")
val = s.recv(1188).decode("utf8")
# Split off the HTTP headers
val = val.split('\r\n\r\n',1)[1]
file = open("goo.html", "w")
file.write("{}".format(val))
file.close()
print(val)