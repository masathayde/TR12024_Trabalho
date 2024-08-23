from conversao import *

def enquadrar_com_contagem (bit_string: list) -> list:
    """
        Enquadra uma sequência de bits usando método de contagem de caracteres.
        Adiciona um cabeçalho à sequência de bits, indicando quantos bits a sequência inteira possui.
        Usa os dois primeiros bytes como cabeçalho. Assim, o número máximo de bits na sequência é 65535.
    """
    character_count = len(bit_string)
    if character_count > 65535:
        character_count = 65535 # Trunca sequência
    hi_part = int(character_count / 256)
    hi_part = posInt2Bit(hi_part)
    if len(hi_part) < 8:
        padding_length = 8 - (len(hi_part) % 8)
        for _ in range(padding_length):
            hi_part.insert(0,0)

    lo_part = character_count % 256
    lo_part = posInt2Bit(lo_part)
    if len(lo_part) < 8:
        padding_length = 8 - (len(lo_part) % 8)
        for _ in range(padding_length):
            lo_part.insert(0,0)
    
    frame = hi_part + lo_part + bit_string
    return frame

def desenquadrar_com_contagem (bit_string: list):
    """ Desenquadra um sequência de bits, usando método de contagem de caracteres.
        Retorna uma tupla contendo quadro e resto da sequência de bits. """
    character_count = bitList2PosInt(bit_string[:16])

    frame = []
    for i in range(character_count):
        if 16 + i < len(bit_string):
            frame += [bit_string[16 + i]]
        else:
            break
    remaining_string = []
    if 16+character_count < len(bit_string):
        remaining_string = list(bit_string[16+character_count:])

    return (frame, character_count, remaining_string)

def enquadrar_com_flag (bit_string: list) -> list:
    """
        Enquadra uma sequência usando método de inserção de flag.
        Adiciona um cabeçalho e cauda com flags. Insere bit nulo após sequência de 5 bits iguais a 1.
    """

    print(bit_string)
    flag = [0,1,1,1,1,1,1,0] # 0x7E
    frame = []
    frame += flag # Coloca flag no começo
    ones_count = 0
    i = 0
    while i < len(bit_string):
        if ones_count == 5:
            frame.append(0)
            ones_count = 0
        
        if bit_string[i] == 1:
            ones_count += 1
        elif bit_string[i] == 0:
            ones_count = 0

        frame.append(bit_string[i])
        i += 1

    frame += flag
    return frame

def desenquadrar_com_flag (bit_string: list):
    """
        Desenquadra uma sequência de bits encapsuladas por um flag.
        Retorna uma tupla contendo quadro e resto da sequência de bits.
        Se não conseguir formar um quadro, retorna tupla com quadro vazio e a sequência de bits original.
    """
    flag = [0,1,1,1,1,1,1,0] # 0x7E

    i = 0
    # Primeiro, procuramos pela flag
    while i + 8 <= len(bit_string):
        if bit_string[i:i+8] == flag:
            break
        i += 1
    else:
        return ([], list(bit_string)) # Não achou uma flag
    
    # Se achamos flag, o índice i + 8 conterá a posição da primeira flag
    first_msg_bit_idx = i + 8
    j = first_msg_bit_idx
    if (j+8 > len(bit_string)): # Se a partir de j (índice do primeiro bit depois da flag), não houver pelo menos 8 bits, não haverá uma segunda flag, necessariamente
        return ([], list(bit_string)) # Não achou uma flag

    # Percorremos o resto da sequência procurando uma segunda flag
    while j+8 <= len(bit_string):
        potential_flag = bit_string[j:j+8]
        if potential_flag == flag:
            break
        j += 1
    else:
        return ([], list(bit_string)) # Não achou uma flag
    
    # Agora sabemos que j:j+8 contém a segunda flag. Precisamos descartar os bits adicionais colocados no enquadramento.
    frame = []
    ones_in_a_row = 0
    for bit in bit_string[first_msg_bit_idx:j]:
        if ones_in_a_row == 5: # Bit extra, ignoramos.
            ones_in_a_row = 0
        else:
            if bit == 1:
                ones_in_a_row += 1
            elif bit == 0:
                ones_in_a_row = 0
            else: # This shouldn't happen
                print("Something went wrong.")
                pass
            frame.append(bit)
    
    remaining_string = []
    # Lembrando que j+8 agora é o primeiro índice depois da segunda flag
    if j+8 < len(bit_string): # Checagem para evitar acesso fora da lista
        remaining_string = list(bit_string[j+8:])
    return (frame, remaining_string)