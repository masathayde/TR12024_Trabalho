# Correção de erros
from conversao import *

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
