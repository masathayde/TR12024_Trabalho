# Para testes
from enquadramento import *
from correcao import *

# test = [1,1,1,1,1,1,1,0,1]
# print(bit2byte_string(test))
# print(posInt2Bit(256))

# test1 = [2,255,3,126]
# frame = enquadrar_com_flag(test1)
# # print (byte2bit_string(frame))
# print(frame)

# test2 = [1, 1, 0]
# print(add_bit_de_paridade_par(test2))

crc_len = 32
generator = [1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,0,1,1,1] # Representação do polinômio gerador, neste caso CRC32 IEEE 802-3
# generator = [1,0,1,1]

# a = [1,1,0,1,0,0,1,1,1,0,1,1,0,0]
a = [0]
b = calc_crc(a, crc_len, generator)
print(b)
c = a + b
print(check_crc(c, crc_len, generator))