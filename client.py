import socket

# from ..conversao import *
from Enlace.enquadramento import *


# def print_frame (data: list, character_count: int):
#     bin_msg = bytearray(data)
#     print(f"Número de caracteres: ".encode('utf-8') + str(character_count).encode('utf-8'))
#     print(bin_msg.decode('utf8'), flush=True)
#     return

def create_frame (msg:str) -> list:
    bin_msg = bytearray(msg, 'utf8')
    msg_byte_list = [byte for byte in bin_msg]
    frame = enquadrar_com_contagem(msg_byte_list)
    return frame

def read_input (max_len:int = 10, max_msgs:int = 10):
    msg_num = int(input("Number of messages? (Maximum = " + str(max_msgs) + "): "))
    if msg_num < 0 or msg_num > max_msgs:
        msg_num = 1
    
    print("Number of messages chosen: " + str(msg_num))

    byte_string = []
    for i in range(msg_num):
        message = input("Insert message (maximum length = " + str(max_len) + "): ")
        message = message[0:max_len]
        byte_string += create_frame(message)

    byte_stream = bytearray(byte_string)
    return byte_stream


host = "127.0.0.1"
port = 6969

tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    tcp_client.connect((host, port))
except socket.error as msg:
    raise socket.error(f"Failed to connect: {msg}")

# msg = "Hello world"
# bin_msg = bytearray(msg, 'utf8')
# status = tcp_client.send(bin_msg)

byte_stream = read_input()
status = tcp_client.send(byte_stream)

if status > 0:
    data = tcp_client.recv(1024)
    print('Got', repr(data))
tcp_client.close()