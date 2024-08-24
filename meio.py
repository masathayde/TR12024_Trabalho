import socket
import random
import sys
import os

from Enlace.enquadramento import *
from Fisica.modulacaodigital import *

class Meio ():

    def __init__(self, err_prob = 0.1, max_err = 1, err_only_in_frame = True):
        self.error_probability = float(err_prob)
        self.max_errors = int(max_err)
        self.error_only_inside_frame = bool(err_only_in_frame)
        self.framing_type = 0
        self.encoding_type = 0

    def routine (self):
        msgs = ""
        host_in = "127.0.0.1"
        port_in = 7777
        host_out = "127.0.0.1"
        port_out = 7778

        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.bind((host_in, port_in))
        tcp_server.listen()
        while 1:
            conn, addr = tcp_server.accept()
            data = conn.recv(2048)
            if data:
                conn.sendall(data)
                bit_list = self.decode(data)
                processed_steam = self.process_stream(bit_list)
                encoded_stream = bytearray(self.encode(processed_steam))

                # Conectar ao server gui
                tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_client.connect((host_out, port_out))
                status = tcp_client.send(encoded_stream)
                if status > 0:
                    data = tcp_client.recv(2048)
                    # print('Got', repr(data))
                tcp_client.close()

            conn.close()

# Decodifica, para que possa adicionar erros somente ao conteúdo dos quadros (sem alterar cabeçalhos e trelissas)
    def decode (self, data: bytearray) -> list:

        # Informação sobre código e enquadramento usado devem estar nos primeiros 2 bytes
        self.encoding_type = data[0]
        self.framing_type = data[1]

        bit_stream = [bit for bit in data[2:]]
        bit_stream = reverseMakeByteArrayFriendly(bit_stream)
        
        match self.encoding_type:

            case 0: # Sem código
                pass

            case 1: # NRZ Polar
                bit_stream = demod_NRZpolar(bit_stream)
                pass
            
            case 2: # Manchester
                bit_stream = demod_Manchester(bit_stream)
                pass

            case 3: # Bipolar
                bit_stream = demod_Bipolar(bit_stream)
                pass

            case _:
                pass

        return bit_stream
    
    def encode (self, bit_string: list) -> list:

        encoded_bit_stream = list(bit_string)

        match self.encoding_type:

            case 0: # Sem código
                pass

            case 1: # NRZ Polar
                encoded_bit_stream = mod_NRZpolar(encoded_bit_stream)
                pass
            
            case 2: # Manchester
                encoded_bit_stream, _ = mod_Manchester(encoded_bit_stream, 1)
                pass

            case 3: # Bipolar
                encoded_bit_stream = mod_Bipolar(encoded_bit_stream)
                pass

            case _:
                pass

        encoded_bit_stream = makeByteArrayFriendly(encoded_bit_stream)
        return encoded_bit_stream
    

    def separate_frame (self, bit_string: list):
        frame = []
        remaining_string = []

        match self.framing_type:

            case 0: # Contagem de caracteres
                frame, _, remaining_string = desenquadrar_com_contagem(bit_string)
            
            case 1: # Inserção de byte de flag
                frame, remaining_string = desenquadrar_com_flag(bit_string)
            
            case _:
                pass

        return (frame, remaining_string)
    
    def create_frame (self, bit_list) -> list:
        frame = []
        match self.framing_type:

            case 0: # Contagem de caracteres
                frame = list(enquadrar_com_contagem(bit_list))
            
            case 1: # Inserção de byte de flag
                frame = list(enquadrar_com_flag(bit_list))
            
            case _:
                frame = list(bit_list)
        return frame
    
    # Coloca erros em uma sequência
    def insert_errors_in_sequence (self, sequence: list):
        errors = 0
        out_sequence = list(sequence)
        i = 0
        for i in range(len(out_sequence)):
            if errors >= self.max_errors:
                break
            random_num = random.uniform(0.0001, 1)
            result = self.error_probability - random_num
            if result >= 0:
                print("error added")
                out_sequence[i] = int(bool(out_sequence[i]) ^ 1)
                errors += 1
            i += 1
        return out_sequence
    

    def process_stream (self, bit_list: list):
        
        out_stream = []

        if self.error_only_inside_frame == False:
            out_stream = self.insert_errors_in_sequence(bit_list)
        else:
            # Aqui, precisa-se desenquadrar cada quadro para adicionar erros individualmente
            bit_list_copy = list(bit_list)
            while len(bit_list_copy) > 0:
                frame, bit_list_copy = self.separate_frame(bit_list_copy)
                if frame == []: # Não conseguimos criar uma frame por erro na sequência de bits
                    # Nesse caso, inserem-se erros na sequência toda
                    # Se o programa cliente estiver funcionando corretamente, isto nunca deve acontecer. Mas caso aconteça, o programa não falhará aqui.
                    out_stream = self.insert_errors_in_sequence(bit_list)
                    break
                frame = self.insert_errors_in_sequence(frame)
                # Reenquadrar
                frame = self.create_frame(frame)
                out_stream += frame
        return out_stream



# Programa
try:
    if len(sys.argv) == 4:
        meio = Meio(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        meio = Meio()
    meio.routine()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)