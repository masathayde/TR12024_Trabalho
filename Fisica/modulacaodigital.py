def mod_NRZpolar(bit_stream):
    bit_out = []
    for i in range(len(bit_stream)):
        bit = bit_stream[i]
        if bit == 0:
            bit = 255
        bit_out.append(bit)
    return bit_out

def demod_NRZpolar(bit_stream):
    bit_out = []
    for i in range(len(bit_stream)):
        bit = bit_stream[i]
        if bit == -1:
            bit = 0
        bit_out.append(bit)
    return bit_out
        

def mod_Manchester(bit_stream, f):
    length = len(bit_stream)
    clock = []
    for i in range(length):
        clock.append(0)
        clock.append(1)
    bit_out = []
    for bit in bit_stream:  # Duplicando o bit stream para fazer operações diretas
        bit_out.append(bit)
        bit_out.append(bit)
    for i in range(len(bit_out)):   # Fazendo o XOR bit a bit
        bit_out[i] = bit_out[i] ^ clock[i]
    return bit_out,2*f

def demod_Manchester(bit_stream):
    bit_out = []
    consider = 1
    for bit in bit_stream:  # Duplicando o bit stream para fazer operações diretas
        if consider == 1:
            bit_out.append(bit)
        consider = consider * -1
    return bit_out

def mod_Bipolar(bit_stream):
    bit_out = []
    crntpeak = 1
    for i in range(len(bit_stream)):
        bit = bit_stream[i]
        if bit == 1:
            bit = crntpeak
            crntpeak = - crntpeak
        bit_out.append(bit)
    return bit_out

def demod_Bipolar(bit_stream):
    bit_out = []
    for bit in bit_stream:
        if bit != 0:
            bit = 1
        else:
            bit = 0
        bit_out.append(bit)
    return bit_out

# Precisamos usar sockets para transmitir dados, os quais devem estar em um bytearray.
# No entanto, bytearrays não conseguem representar número negativos como -1
# Daí, convertemos os valores iguais a -1 para 255, o que seria -1 em complemento de 2, com um byte de capacidade de armazenamento
def makeByteArrayFriendly (bit_stream):
    bit_out = []
    for bit in bit_stream:
        if bit == -1:
            bit_out.append(255)
        else:
            bit_out.append(bit)
    return bit_out

# Inverso da função anterior
def reverseMakeByteArrayFriendly (bit_stream):
    bit_out = []
    for bit in bit_stream:
        if bit == 255:
            bit_out.append(-1)
        else:
            bit_out.append(bit)
    return bit_out


# BS0 = [0,0,0,0,0,0,0,0]
# BS1 = [1,1,1,1,1,1,1,1]
# BS2 = [0,1,0,1,0,1,0,1]
# BS3 = [0,0,1,0,1,1,1,0]

# print(BS0)
# print(BS1)
# print(BS2)
# print(BS3)

# print("")

# print(mod_NRZpolar(BS0))
# print(mod_NRZpolar(BS1))
# print(mod_NRZpolar(BS2))
# print(mod_NRZpolar(BS3))

# print("")

# print(mod_Manchester(BS0,1)[0])
# print(mod_Manchester(BS1,1)[0])
# print(mod_Manchester(BS2,1)[0])
# print(mod_Manchester(BS3,1)[0])

# print("")

# print(mod_Bipolar(BS0))
# print(mod_Bipolar(BS1))
# print(mod_Bipolar(BS2))
# print(mod_Bipolar(BS3))

# print("")

# print(demod_NRZpolar(mod_NRZpolar(BS0)))
# print(demod_NRZpolar(mod_NRZpolar(BS1)))
# print(demod_NRZpolar(mod_NRZpolar(BS2)))
# print(demod_NRZpolar(mod_NRZpolar(BS3)))

# print("")

# print(demod_Manchester(mod_Manchester(BS0,1)[0]))
# print(demod_Manchester(mod_Manchester(BS1,1)[0]))
# print(demod_Manchester(mod_Manchester(BS2,1)[0]))
# print(demod_Manchester(mod_Manchester(BS3,1)[0]))

# print("")

# print(demod_Bipolar(mod_Bipolar(BS0)))
# print(demod_Bipolar(mod_Bipolar(BS1)))
# print(demod_Bipolar(mod_Bipolar(BS2)))
# print(demod_Bipolar(mod_Bipolar(BS3)))
