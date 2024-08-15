# Funcionalidades desejadas:
# - Receber várias mensagens e enquadrá-las com contagem de caracteres, desenquadrá-las corretamente no final
# - Simular erros na sequência - colocar erros ANTES de enquadramento
# - Checar CRC e printar Resultado

# Variáveis

crc_len = 32
generator = [1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,0,1,1,1] # Representação do polinômio gerador, neste caso CRC32 IEEE 802-3



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