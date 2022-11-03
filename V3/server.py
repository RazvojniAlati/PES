import socket
from threading import Thread

def accept_incoming_client():
    while True:
        conn, addr = s.accept()
        Thread(target=handle_client, args=(conn,)).start()

def handle_client(client):
    data = client.recv(1024).decode("utf8")
    print(data)
    if data == 'koliko je sati':
        client.sendall(b'8:24')
    elif data == 'kako se zoves':
        client.sendall(b"lenka")
    else:
        client.sendall(b'3.11.2022.')

    #client.sendall(b'response')
    client.close()

if __name__ == "__main__":
    s = socket.socket()
    s.bind(('127.0.0.1', 8888))
    print("cekam na portu 8888")
    s.listen(10)
    accept_thread = Thread(target = accept_incoming_client)
    accept_thread.start()
    accept_thread.join()
    s.close()



