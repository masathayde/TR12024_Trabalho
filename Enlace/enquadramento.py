def enquadrar_com_contagem (byte_string: list) -> list:
    """
        Enquadra uma sequência de bytes usando método de contagem de caracteres.
        Adiciona um cabeçalho à sequência de bytes, indicando quantos bytes a sequência inteira possui.
    """
    character_count = len(byte_string)
    frame = [character_count] + byte_string
    return frame

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

