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