import math
import os


def amplitude_sk(amplitude = 1.0, frequency = 1.0, bits = 10, sample_num = 100):
    # Amplitude do sinal se torna 0 se o bit for 0.
    signal = []

    # Torna o número binário em uma lista de bits.
    bit_list = [int(i) for i in str(bits)]

    for bit in bit_list:
        if bit == 0:
            for i in range(sample_num): # "sample_num" (padrão = 100) é o número de amostras tomadas para cada bit.
                signal.append(0.0)
        else: # bit == 1
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * frequency * (i + 1) / sample_num))

    return f"List of bits => {bit_list}\n" \
           f"Signal => {signal}"

def frequency_sk(amplitude = 1.0, frequency_0 = 1.0, frequency_1 = 2.0, bits = 10, sample_num = 100):
    # Sinal possui uma frequência se o bit for 0, e outra se o bit for 1.
    signal = []

    bit_list = [int(i) for i in str(bits)]

    for bit in bit_list:
        if bit == 0:
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * frequency_0 * (i + 1) / sample_num))
        else: # bit == 1
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * frequency_1 * (i + 1) / sample_num))

    return f"List of bits => {bit_list}\n" \
           f"Signal => {signal}"

def eight_qam(amplitude = 1.0, frequency = 1.0, bits = 1010, sample_num = 100):
    # Ângulo do sinal é alterado por um valor associado a tripla de bits considerada.
    signal = []

    # Checar se o comprimento da palavra de bits é um múltiplo de 3. Se não for, preencher a palavra com um ou dois zeros.
    aux = str(bits)

    if (len(aux) % 3) == 1:
        aux = "00" + aux
    elif (len(aux) % 3) == 2:
        aux = "0" + aux

    # Separar a palavra de bits em triplas.
    aux.split()
    bit_list = [(int(aux[i]), int(aux[i + 1]), int(aux[i + 2])) for i in range(0, len(aux), 3)]

    for bit_triple in bit_list: # Usando código de Gray.
        if bit_triple == (0,0,0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * frequency * (i + 1) / sample_num))
        elif bit_triple == (0,0,1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * (i + 1) / sample_num) + (math.pi / 8)))
        elif bit_triple == (0,1,1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * (i + 1) / sample_num) + (math.pi / 4)))
        elif bit_triple == (0,1,0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * (i + 1) / sample_num) + (3 * math.pi / 8)))
        elif bit_triple == (1,1,0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * (i + 1) / sample_num) + (math.pi / 2)))
        elif bit_triple == (1,1,1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * (i + 1) / sample_num) + (5 * math.pi / 8)))
        elif bit_triple == (1,0,1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * (i + 1) / sample_num) + (3 * math.pi / 4)))
        else: # bit_triple == (1,0,0)
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * (i + 1) / sample_num) + (7 * math.pi / 8)))

    return f"String of bits => {aux}\n" \
           f"List of bits => {bit_list}\n" \
           f"Signal => {signal}"

if __name__ == "__main__":
    print("-- Amplitude Shift Keying --\n" + amplitude_sk())
    input()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("-- Frequency Shift Keying --\n" + frequency_sk())
    input()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("-- 8-QAM --\n" + eight_qam())
    input()
