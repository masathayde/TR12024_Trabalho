import socket

host = "127.0.0.1"
port = 6969

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((host, port))
tcp_server.listen()
conn, addr = tcp_server.accept()

while 1:
    data = conn.recv(1024)
    if not data:
        break
    print(data.decode('utf8'))
    conn.sendall(data)
conn.close()