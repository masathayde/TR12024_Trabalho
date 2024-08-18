def enquadrar_com_contagem (byte_string: list) -> list:
    """
        Enquadra uma sequência de bytes usando método de contagem de caracteres.
        Adiciona um cabeçalho à sequência de bytes, indicando quantos bytes a sequência inteira possui.
    """
    character_count = len(byte_string)
    frame = [character_count] + byte_string
    return frame

def desenquadrar_com_contagem (byte_string: list):
    """ Desenquadra um sequência de bytes, usando método de contagem de caracteres.
        Retorna uma tupla contendo quadro e resto da sequência de bytes. """
    character_count = byte_string[0]
    frame = []
    for i in range(character_count):
        if 1 + i < len(byte_string):
            frame += [byte_string[1 + i]]
        else:
            break
    remaining_string = []
    if 1+character_count < len(byte_string):
        remaining_string = list(byte_string[1+character_count:])

    return (frame, character_count, remaining_string)

def enquadrar_com_flag (byte_string: list) -> list:
    """
        Enquadra uma sequência de bytes usando método de inserção de flag.
        Adiciona um cabeçalho e cauda com flags. Adiciona caractere de escape para bytes na carga útil que contenham
        a flag.
        Adiciona caractere de escape antes de byte de escape também.
    """
    flag = 126 # 0x7E
    escape = 255 # 0xFF

    frame = [flag] # Coloca flag no começo
    for byte in byte_string:
        if byte == flag or byte == escape: # Caso um byte seja igual a um dos bytes especiais, colocamos escape antes.
            frame.append(escape)
        frame.append(byte)
    frame.append(flag)
    return frame

def desenquadrar_com_flag (byte_string: list):
    """
        Desenquadra uma sequência de bytes encapsuladas por um flag.
        Retorna uma tupla contendo quadro e resto da sequência de bytes.
        Se não conseguir formar um quadro, retorna tupla com quadro vazio e a sequência de bytes original.
    """
    flag = 126 # 0x7E
    escape = 255 # 0xFF

    frame = []

    i = 0
    # Primeiro, procuramos pelo primeiro byte que contenha a flag
    while i < len(byte_string):
        if byte_string[i] == flag:
            break
        i += 1
    else:
        return ([], list(byte_string)) # Não achou uma flag
    
    # Se achamos flag, o índice i conterá a posição da primeira flag
    j = i + 1
    # Percorremos o resto da sequência procurando uma segunda flag e lidando com caracteres especiais
    while j < len(byte_string):
        if byte_string[j] == flag:
            break
        elif byte_string[j] == escape: # Ignora este byte, adiciona próximo byte sem checar se é flag
            frame += [byte_string[j+1]]
            j += 2
        else:
            frame += [byte_string[j]]
            j += 1
    else:
        return ([], list(byte_string)) # Não achou uma flag
    
    remaining_string = []
    if j+1 < len(byte_string): # Checagem para evitar acesso fora da lista
        remaining_string = list(byte_string[j+1:])
    return (frame, remaining_string)