import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8888))
client_message = 'koliko je sati' #koliko je sati? kako se zoves? koji je datum?
s.send(client_message.encode("utf8"))
server_response = s.recv(4096).decode("utf8")
print("server kaze: {}".format(server_response))
