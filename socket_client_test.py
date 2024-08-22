import socket

host = "127.0.0.1"
port = 6969

tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    tcp_client.connect((host, port))
except socket.error as msg:
    raise socket.error(f"Failed to connect: {msg}")

msg = "Hello world"
bin_msg = bytearray(msg, 'utf8')
status = tcp_client.send(bin_msg)

if status > 0:
    data = tcp_client.recv(1024)
    print('Got', repr(data))
tcp_client.close()