# Para testes
from enquadramento import *
from correcao import *
from conversao import *

# test = [1,1,1,1,1,1,1,0,1]
# print(bit2byte_string(test))
# print(posInt2Bit(256))

# test1 = [2,255,3,126]
# frame = enquadrar_com_flag(test1)
# # print (byte2bit_string(frame))
# print(frame)

# test2 = [1, 1, 0]
# print(add_bit_de_paridade_par(test2))

# crc_len = 32
# generator = [1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,0,1,1,1] # Representação do polinômio gerador, neste caso CRC32 IEEE 802-3
# # generator = [1,0,1,1]
# # a = [1,1,0,1,0,0,1,1,1,0,1,1,0,0]
# a = [0]
# b = calc_crc(a, crc_len, generator)
# print(b)
# c = a + b
# print(check_crc(c, crc_len, generator))

# a = [1,1,1,1,0,0,0,0,1]
# a = bit2byte_string(a)
# b = bytearray(a)
# c = [x for x in b]
# print(a)
# print(b)
# print(c)

# a = [3,1,2,3,4,5,6]
# b = desenquadrar_com_contagem(a)
# print(b[0])
# print(b[1])


a = [1,2,255,3,4,126,5,6]
x = [2,2,2]
t = [126, 1, 2]
a_ = enquadrar_com_flag(a)
b = desenquadrar_com_flag(a_ + x)
c = desenquadrar_com_flag(t)
print(a)
print(a_)
print(b[0])
print(b[1])
print(c[0])
print(c[1])
