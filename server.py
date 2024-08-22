# Funcionalidades desejadas:
# - Receber várias mensagens e enquadrá-las com contagem de caracteres, desenquadrá-las corretamente no final
# - Simular erros na sequência - colocar erros ANTES de enquadramento
# - Checar CRC e printar Resultado
import socket

# from ..conversao import *
from Enlace.enquadramento import *

# Variáveis
crc_len = 32
generator = [1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,0,1,1,1] # Representação do polinômio gerador, neste caso CRC32 IEEE 802-3

def separate_frame (byte_string: list):
    frame, characer_count, remaining_string = desenquadrar_com_contagem(byte_string)
    return (frame, characer_count, remaining_string)

def print_frame (data: list, character_count: int):
    bin_msg = bytearray(data)
    print(f"Número de caracteres: " + str(character_count))
    print(bin_msg.decode('utf8'), flush=True)
    return

def print_all_frames (data: bytearray):
    byte_string = [byte for byte in data] # Converte para uma lista de bytes no formato usado aqui
    while len(byte_string) > 0:
        frame, character_count, byte_string = separate_frame(byte_string)
        print_frame(frame, character_count) 
    return


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
    # print(data.decode('utf8'))
    print_all_frames(data)
    conn.sendall(data)
    
conn.close()