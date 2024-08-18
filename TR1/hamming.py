import math
import random

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
    return bit_out


BS0 = [0,0,0,0,0,0,0,0]
BS1 = [1,1,1,1,1,1,1,1]
BS2 = [1,1,0,1,0,0,1]

print("message:",BS2)
encoded = cod_hamming(BS2)
print("encoded:",encoded)

index = random.randint(0,len(encoded) - 1)
print("error index:",index)
encoded[index] = encoded[index] ^ 1

print("with error:",encoded)
print("decoded:",decod_hamming(encoded))