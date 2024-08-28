import math
import os


def ask_manchester(amplitude = 1.0, frequency = 1.0, bits = [1, 0], sample_num = 100):
    # Amplitude do sinal é normal caso o bit seja 1 e é nula caso o bit seja 0. Frequência considerada é o dobro do normal.
    signal = []

    for bit in bits:
        if bit == 0:
            for i in range(sample_num): # "sample_num" (padrão é 100) é o número de amostras tomadas para cada bit.
                    signal.append(0.0)
        else: # bit == 1
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * (frequency * 2) * i / sample_num))

    return signal

def ask_nrz(amplitude = 1.0, frequency = 1.0, bits = [1, -1], sample_num = 100):
    # Amplitude do sinal é normal caso o bit seja 1 e é nula caso o bit seja -1.
    signal = []

    for bit in bits:
        if bit == -1:
            for i in range(sample_num):
                    signal.append(0.0)
        else: # bit == 1
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * frequency * i / sample_num))

    return signal

def ask_bipolar(amplitude = 1.0, frequency = 1.0, bits = [1, 0, -1], sample_num = 100):
    # Amplitude do sinal é normal caso o bit seja 1, é nula caso o bit seja 0 e é metade do normal caso o bit seja -1.
    signal = []

    for bit in bits:
        if bit == -1:
            for i in range(sample_num):
                signal.append((amplitude / 2) * math.sin(2 * math.pi * frequency * i / sample_num))
        elif bit == 0:
            for i in range(sample_num):
                signal.append(0.0)
        else: # bit == 1
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * frequency * i / sample_num))

    return signal


def fsk_manchester(amplitude = 1.0, frequency_0 = 1.0, frequency_1 = 2.0, bits = [1, 0], sample_num = 100):
    # Frequência do sinal é uma caso o bit seja 1 e é outra caso o bit seja 0. Frequências consideradas são o dobro do normal.
    signal = []

    for bit in bits:
        if bit == 0:
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * (frequency_0 * 2) * i / sample_num))
        else: # bit == 1
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * (frequency_1 * 2) * i / sample_num))

    return signal

def fsk_nrz(amplitude = 1.0, frequency_0 = 1.0, frequency_1 = 2.0, bits = [1, -1], sample_num = 100):
    # Frequência do sinal é uma caso o bit seja 1 e é outra caso o bit seja -1.
    signal = []

    for bit in bits:
            if bit == -1:
                for i in range(sample_num):
                    signal.append(amplitude * math.sin(2 * math.pi * frequency_0 * i / sample_num))
            else: # bit == 1
                for i in range(sample_num):
                    signal.append(amplitude * math.sin(2 * math.pi * frequency_1 * i / sample_num))

    return signal

def fsk_bipolar(amplitude = 1.0, frequency_0 = 1.0, frequency_1 = 2.0, bits = [1, 0, -1], sample_num = 100):
    # Frequência do sinal é uma caso o bit seja 1, é outra caso o bit seja 0 e é a média das duas caso o bit seja -1.
    signal = []

    for bit in bits:
        if bit == -1:
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * ((frequency_0 + frequency_1) / 2) * i / sample_num))
        elif bit == 0:
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * frequency_0 * i / sample_num))
        else: # bit == 1
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * frequency_1 * i / sample_num))

    return signal


def eight_qam_manchester(amplitude = 1.0, frequency = 1.0, bits = [1, 0], sample_num = 100):
    # Ângulo do sinal é alterado por um valor associado a tripla de bits considerada.
    # Trabalha com bits 0 e 1. Frequência considerada é o dobro do normal.
    signal = []

    # Checar se o comprimento da palavra de bits é um múltiplo de 3. Se não for, preencher a palavra com um ou dois zeros.
    if (len(bits) % 3) == 1:
        bits = [0, 0] + bits
    elif (len(bits) % 3) == 2:
        bits = [0] + bits

    # Separar a palavra de bits em triplas.
    triple_list = [(bits[i], bits[i + 1], bits[i + 2]) for i in range(0, len(bits), 3)]

    for bit_triple in triple_list: # Usando código de Gray.
            if bit_triple == (0, 0, 0):
                for i in range(sample_num):
                    signal.append(amplitude * math.sin(2 * math.pi * (frequency * 2) * i / sample_num))
            elif bit_triple == (0, 0, 1):
                for i in range(sample_num):
                    signal.append(amplitude * math.sin((2 * math.pi * (frequency * 2) * i / sample_num) + (math.pi / 4)))
            elif bit_triple == (0, 1, 1):
                for i in range(sample_num):
                    signal.append(amplitude * math.sin((2 * math.pi * (frequency * 2) * i / sample_num) + (math.pi / 2)))
            elif bit_triple == (0, 1, 0):
                for i in range(sample_num):
                    signal.append(amplitude * math.sin((2 * math.pi * (frequency * 2) * i / sample_num) + (3 * math.pi / 4)))
            elif bit_triple == (1, 1, 0):
                for i in range(sample_num):
                    signal.append(amplitude * math.sin((2 * math.pi * (frequency * 2) * i / sample_num) + math.pi))
            elif bit_triple == (1, 1, 1):
                for i in range(sample_num):
                    signal.append(amplitude * math.sin((2 * math.pi * (frequency * 2) * i / sample_num) + (5 * math.pi / 4)))
            elif bit_triple == (1, 0, 1):
                for i in range(sample_num):
                    signal.append(amplitude * math.sin((2 * math.pi * (frequency * 2) * i / sample_num) + (3 * math.pi / 2)))
            else: # bit_triple == (1, 0, 0)
                for i in range(sample_num):
                    signal.append(amplitude * math.sin((2 * math.pi * (frequency * 2) * i / sample_num) + (7 * math.pi / 4)))

    return signal

def eight_qam_nrz(amplitude = 1.0, frequency = 1.0, bits = [1, -1], sample_num = 100):
    # Trabalha com bits -1 e 1.
    signal = []

    if (len(bits) % 3) == 1:
        bits = [0, 0] + bits
    elif (len(bits) % 3) == 2:
        bits = [0] + bits

    triple_list = [(bits[i], bits[i + 1], bits[i + 2]) for i in range(0, len(bits), 3)]

    for bit_triple in triple_list: # Usando código de Gray.
            if bit_triple == (-1, -1, -1):
                for i in range(sample_num):
                    signal.append(amplitude * math.sin(2 * math.pi * frequency * i / sample_num))
            elif bit_triple == (-1, -1, 1):
                for i in range(sample_num):
                    signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (math.pi / 4)))
            elif bit_triple == (-1, 1, 1):
                for i in range(sample_num):
                    signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (math.pi / 2)))
            elif bit_triple == (-1, 1, -1):
                for i in range(sample_num):
                    signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (3 * math.pi / 4)))
            elif bit_triple == (1, 1, -1):
                for i in range(sample_num):
                    signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + math.pi))
            elif bit_triple == (1, 1, 1):
                for i in range(sample_num):
                    signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (5 * math.pi / 4)))
            elif bit_triple == (1, -1, 1):
                for i in range(sample_num):
                    signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (3 * math.pi / 2)))
            else: # bit_triple == (1, -1, -1)
                for i in range(sample_num):
                    signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (7 * math.pi / 4)))

    return signal

def eight_qam_bipolar_amplitude(amplitude = 1.0, frequency = 1.0, bits = [1, -1], sample_num = 100):
    # Para a codificação bipolar, há pares de triplas que representam a mesma sequência binária (e.g. (1, 0, -1) = (-1, 0, 1) = 101). É
    # importante considerar essa diferença na transmissão, pois permite preservar as qualidades da codificação, como o sinal balanceado.
    # No entanto, a 8-QAM normal não é capaz de representar todas as triplas necessárias para isso (15 no total), o que leva a necessidade
    # de usar algo a mais para aumentar o número de coordenadas que podem ser utilizadas na constelação.
    # Aqui é adicionada a amplitude como parâmetro para se resolver isso, visto que aumentar o número de fases faz codificação deixar de
    # ser 8-QAM.
    # Trabalha com bits -1, 0 e 1.
    signal = []

    if (len(bits) % 3) == 1:
        bits = [0, 0] + bits
    elif (len(bits) % 3) == 2:
        bits = [0] + bits

    triple_list = [(bits[i], bits[i + 1], bits[i + 2]) for i in range(0, len(bits), 3)]

    for bit_triple in triple_list:
        if bit_triple == (0, 0, 0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * frequency * i / sample_num))
        elif bit_triple == (0, 0, 1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (math.pi / 4)))
        elif bit_triple == (0, 0, -1):
            for i in range(sample_num): # Representa a mesma sequência de bits que o anterior, mas sua amplitude é metade.
                signal.append((amplitude / 2) * math.sin((2 * math.pi * frequency * i / sample_num) + (math.pi / 4)))
        elif bit_triple == (0, 1, -1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (math.pi / 2)))
        elif bit_triple == (0, -1, 1):
            for i in range(sample_num):
                signal.append((amplitude / 2) * math.sin((2 * math.pi * frequency * i / sample_num) + (math.pi / 2)))
        elif bit_triple == (0, 1, 0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (3 * math.pi / 4)))
        elif bit_triple == (0, -1, 0):
            for i in range(sample_num):
                signal.append((amplitude / 2) * math.sin((2 * math.pi * frequency * i / sample_num) + (3 * math.pi / 4)))
        elif bit_triple == (1, -1, 0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + math.pi))
        elif bit_triple == (-1, 1, 0):
            for i in range(sample_num):
                signal.append((amplitude / 2) * math.sin((2 * math.pi * frequency * i / sample_num) + math.pi))
        elif bit_triple == (1, -1, 1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (5 * math.pi / 4)))
        elif bit_triple == (-1, 1, -1):
            for i in range(sample_num):
                signal.append((amplitude / 2) * math.sin((2 * math.pi * frequency * i / sample_num) + (5 * math.pi / 4)))
        elif bit_triple == (1, 0, -1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (3 * math.pi / 2)))
        elif bit_triple == (-1, 0, 1):
            for i in range(sample_num):
                signal.append((amplitude / 2) * math.sin((2 * math.pi * frequency * i / sample_num) + (3 * math.pi / 2)))
        elif bit_triple == (1, 0, 0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (7 * math.pi / 4)))
        else: # bit_triple == (-1, 0, 0)
            for i in range(sample_num):
                signal.append((amplitude / 2) * math.sin((2 * math.pi * frequency * i / sample_num) + (7 * math.pi / 4)))

    return signal

def eight_qam_bipolar_fase(amplitude = 1.0, frequency = 1.0, bits = [1, -1], sample_num = 100):
    # Aqui são utilizadas fases adicionais para representar todas as triplas necessárias.
    # Trabalha com bits -1, 0 e 1.
    signal = []

    if (len(bits) % 3) == 1:
        bits = [0, 0] + bits
    elif (len(bits) % 3) == 2:
        bits = [0] + bits

    triple_list = [(bits[i], bits[i + 1], bits[i + 2]) for i in range(0, len(bits), 3)]

    for bit_triple in triple_list:
        if bit_triple == (0, 0, 0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * frequency * i / sample_num))
        elif bit_triple == (0, 0, 1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (math.pi / 8)))
        elif bit_triple == (0, 0, -1):
            for i in range(sample_num): # Representa a mesma sequência de bits que o anterior, mas sua fase é diferente.
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (math.pi / 4)))
        elif bit_triple == (0, 1, -1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (3 * math.pi / 8)))
        elif bit_triple == (0, -1, 1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (math.pi / 2)))
        elif bit_triple == (0, 1, 0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (5 * math.pi / 8)))
        elif bit_triple == (0, -1, 0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (3 * math.pi / 4)))
        elif bit_triple == (1, -1, 0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (7 * math.pi / 8)))
        elif bit_triple == (-1, 1, 0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + math.pi))
        elif bit_triple == (1, -1, 1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (9 * math.pi / 8)))
        elif bit_triple == (-1, 1, -1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (5 * math.pi / 4)))
        elif bit_triple == (1, 0, -1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (11 * math.pi / 8)))
        elif bit_triple == (-1, 0, 1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (3 * math.pi / 2)))
        elif bit_triple == (1, 0, 0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (13 * math.pi / 8)))
        else: # bit_triple == (-1, 0, 0)
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (7 * math.pi / 4)))

    return signal

def eight_qam_bipolar_normal(amplitude = 1.0, frequency = 1.0, bits = [1, -1], sample_num = 100):
    # Alternativamente, se usa o 8-QAM normal sem considerar as triplas equivalentes e fica a cargo do receptor remontar a palavra de
    # bits original com base nas regras da codificação bipolar.
    # Trabalha com bits -1, 0 e 1.
    signal = []

    if (len(bits) % 3) == 1:
        bits = [0, 0] + bits
    elif (len(bits) % 3) == 2:
        bits = [0] + bits

    triple_list = [(bits[i], bits[i + 1], bits[i + 2]) for i in range(0, len(bits), 3)]
    
    for bit_triple in triple_list:
        if bit_triple == (0, 0, 0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin(2 * math.pi * frequency * i / sample_num))
        elif bit_triple == (0, 0, 1) or bit_triple == (0, 0, -1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (math.pi / 4)))
        elif bit_triple == (0, -1, 1) or bit_triple == (0, 1, -1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (math.pi / 2)))
        elif bit_triple == (0, -1, 0) or bit_triple == (0, 1, 0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (3 * math.pi / 4)))
        elif bit_triple == (1, -1, 0) or bit_triple == (-1, 1, 0):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + math.pi))
        elif bit_triple == (1, -1, 1) or bit_triple == (-1, 1, -1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (5 * math.pi / 4)))
        elif bit_triple == (1, 0, -1) or bit_triple == (-1, 0, 1):
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (3 * math.pi / 2)))
        else: # bit_triple == (1, 0, 0) or bit_triple == (-1, 0, 0)
            for i in range(sample_num):
                signal.append(amplitude * math.sin((2 * math.pi * frequency * i / sample_num) + (7 * math.pi / 4)))

    return signal


if __name__ == "__main__":
    print("-- Amplitude Shift Keying (Manchester) --\nBits => [1, 0]")
    print(ask_manchester())
    input("\nAperte ENTER\n")
    print("-- Amplitude Shift Keying (NRZ) --\nBits => [1, -1]")
    print(ask_nrz())
    input("\nAperte ENTER\n")
    print("-- Amplitude Shift Keying (Bipolar) --\nBits => [1, 0, -1]")
    print(ask_bipolar())
    input("\nAperte ENTER\n")

    os.system('cls' if os.name == 'nt' else 'clear')

    print("-- Frequency Shift Keying (Manchester) --\nBits => [1, 0]")
    print(fsk_manchester())
    input("\nAperte ENTER\n")
    print("-- Frequency Shift Keying (NRZ) --\nBits => [1, -1]")
    print(fsk_nrz())
    input("\nAperte ENTER\n")
    print("-- Frequency Shift Keying (Bipolar) --\nBits => [1, 0, -1]")
    print(fsk_bipolar())
    input("\nAperte ENTER\n")

    os.system('cls' if os.name == 'nt' else 'clear')

    print("Como o 8-QAM trabalha com triplas, adiciona-se um ou dois 0s de preenchimento caso precise.\n")
    print("-- 8-QAM (Manchester) --\nBits => [1, 0]")
    print(eight_qam_manchester())
    input("\nAperte ENTER\n")
    print("-- 8-QAM (NRZ) --\nBits => [1, -1]")
    print(eight_qam_nrz())
    input("\nAperte ENTER\n")
    print("-- 8-QAM (Bipolar - amplitude) --\nBits => [1, -1]")
    print(eight_qam_bipolar_amplitude())
    input("\nAperte ENTER\n")
    print("-- 8-QAM (Bipolar - fase) --\nBits => [1, -1]")
    print(eight_qam_bipolar_fase())
    input("\nAperte ENTER\n")
    print("-- 8-QAM (Bipolar - normal) --\nBits => [1, -1]")
    print(eight_qam_bipolar_normal())
    input("\nAperte ENTER\n")
