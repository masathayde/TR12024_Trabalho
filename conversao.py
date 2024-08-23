# Funções de auxílio

def bit2byte_string (bit_string: list) -> list:
    """Caso haja menos de 8 bits em um grupo, o algoritmo abaixo "preenche" o valor com zeros à esquerda. """
    bytecount = len(bit_string)//8 # Presume que a lista não seja vazia
    if len(bit_string) % 8 != 0:
        bytecount += 1
    byte_string = []
    i = 0
    j = 0
    while i < bytecount:
        byte_value = 0
        power = min(len(bit_string) - j - 1, 7)
        while power >= 0:
            byte_value += ((2**power) * bit_string[j])
            j += 1
            power -= 1
        byte_string.append(byte_value)
        i += 1

    return byte_string

def posInt2Bit (number: int) -> list:
    """Converte número inteiro maior ou igual a zero para sequência de bits usando divisões sucessivas por 2. """
    bit_string = []
    number_copy = number
    partial_result = [] # Lista de restos das divisões
    partial_result.append(number_copy % 2)
    number_copy = number_copy // 2
    while number_copy != 0:
        partial_result.append(number_copy % 2)
        number_copy = number_copy // 2
    i = len(partial_result) - 1
    while i >= 0:
        bit_string.append(partial_result[i])
        i -= 1

    return bit_string

def bitList2PosInt (bit_list: list) -> int:
    result = 0
    i = 0
    while i < len(bit_list):
        result += bit_list[i] * (2**(len(bit_list)-1-i))
        i += 1
    return result

def byte2bit_string (byte_string: list) -> list:
    """Converte sequência de números inteiros positivos para sequência de bits """
    result = []
    for byte in byte_string:
        partial_result = posInt2Bit(byte)
        if len(partial_result) % 8 != 0: # Adiciona padding
            padding_length = 8 - (len(partial_result) % 8)
            for _ in range(padding_length):
                partial_result.insert(0,0)
        
        result += partial_result
    
    return result


def int2ByteArray (num_list: list) -> bytearray:
    """Converte uma lista de inteiros contendo para bytearray"""
    output = bytearray()
    for num in num_list:
        output.append(num)
    return output