# Correção de erros
import math
import random

def add_bit_de_paridade_par (bit_string: list) -> list:
    """Conta o número de bits na sequência e adiciona um bit a mais no fim,
    para que o número de bits iguais a 1 na sequência seja par."""
    new_bit_string = []
    total = 0
    for bit in bit_string:
        total += bit
    
    last_bit = total % 2 # Se o total não for par, o bit de paridade deve ser 1
    new_bit_string = bit_string + [last_bit]

    return new_bit_string

def checar_bit_de_paridade_par (bit_string: list) -> bool:
    """Retorna True se o número de bits na sequência de entrada for par """
    # Somamos todos os bits, se o resultado for par, retorna verdadeiro
    result = 0
    for bit in bit_string:
         result += bit
    return not bool(result % 2)

def calc_crc (bit_string: list, crc_len: int, generator: list) -> list:
    """Calcula bits para correção de erro usando CRC. """

    dividend = list(bit_string) # Cópia (rasa) da lista original, para que possa ser modificada. Também conterá o resultado final
    dividend += [0] * crc_len # Adicionando preenchimento

    while len(dividend) > crc_len:
        if dividend[0] != 0: # Se o bit mais significativo for 0, pulamos o cálculo a seguir e vamos para a próxima repetição do laço
            for i in range(crc_len + 1):
                    dividend[i] = int(bool(dividend[i]) ^ bool(generator[i]))

        dividend.pop(0) # Remove bit mais significativo e reduz comprimento da sequência
    
    # Ao final, a lista deve conter o resto da divisão, a sequência de redudância desejada
    return dividend

def check_crc (bit_string: list, crc_len: int, generator: list) -> bool:
    """Checa se há erro na sequência de bits usando CRC. Retorna True se não houver erros.
    Presume que os bits de redudância já estejam na sequência de entrada. """

    dividend = list(bit_string)
    is_correct = True

    while len(dividend) > crc_len:
        if dividend[0] != 0: # Se o bit mais significativo for 0, pulamos o cálculo a seguir e vamos para a próxima repetição do laço
            for i in range(crc_len + 1):
                    dividend[i] = int(bool(dividend[i]) ^ bool(generator[i]))

        dividend.pop(0) # Remove bit mais significativo e reduz comprimento da sequência
    
    for bit in dividend:
        if bit != 0:
            is_correct = False
            break
    
    return is_correct

def add_crc (bit_string: list, crc_len: int, generator: list) -> list:
     """Faz cálculo de CRC e adiciona os bits no final da mensagem"""
     bit_string_with_crc = list(bit_string)
     crc = calc_crc(bit_string, crc_len, generator)
     bit_string_with_crc += crc
     return bit_string_with_crc

def cod_hamming(bit_stream):
    bit_out = []
    powpos = []
    length = len(bit_stream)
    i = 0
    n = 1
    while i < length:
        if ((n) & n-1 == 0) and n != 0: # Checando se é potência de 2
            bit_out.append(0)
            powpos.append(i)    # Guardando a posição para depois fazer a paridade
            n = n + 1
        else:
            bit_out.append(bit_stream[i])
            i = i + 1
            n = n + 1
    for i in range(len(powpos)):
        inter = 2**i
        bit_out[inter - 1] = ham_parity(bit_out,inter)
    return bit_out
        

def ham_parity(bit_stream,interval):
    count = interval - 1
    valid = -1   # Se deve ou contar o bit atual
    parity = 0
    for i in range(len(bit_stream)):
        if count == 0: 
            count = interval
            valid = - valid
        if valid > 0:
            parity = parity ^ bit_stream[i]
        count = count - 1
    return parity

def decod_hamming(bit_stream):
    bit_out = []
    length = len(bit_stream)
    i = 0
    power = math.floor(math.sqrt(len(bit_stream)))
    parities = []
    check = False
    for i in range(power+1):
        par = ham_parity(bit_stream,2**i)
        parities.append(par)
        if par == 1:
            check = True
    if check:   # Se teve erro
        count = 0
        for i in range(len(parities)):
            count += parities[i] * (2**i)
        bit_stream[count-1] = bit_stream[count-1] ^ 1
    i = 1
    for bit in bit_stream:
        if ((i) & (i-1) != 0):
            bit_out.append(bit)
        i += 1
    return bit_out, check


# BS0 = [0,0,0,0,0,0,0,0]
# BS1 = [1,1,1,1,1,1,1,1]
# BS2 = [1,1,0,1,0,0,1]

# print("message:",BS2)
# encoded = cod_hamming(BS2)
# print("encoded:",encoded)

# index = random.randint(0,len(encoded) - 1)
# print("error index:",index)
# encoded[index] = encoded[index] ^ 1

# print("with error:",encoded)
# print("decoded:",decod_hamming(encoded))
