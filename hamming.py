import math
def calcular_bit_parity(data):
    # Calcula el bit de paridad para cada posición en los datos
    # y devuelve una lista de bits de paridad
    parity_bits = []
    for i in range(len(data)):
        parity_bit = 0
        for j in range(len(data)):
            if (i+1) & (1 << j):
                parity_bit ^= int(data[j])
        parity_bits.append(parity_bit)
    return parity_bits

def agregar_bits_parity(data, parity_bits):
    # Agrega los bits de paridad a los datos
    encoded_data = []
    data_index = 0
    for i in range(len(data) + len(parity_bits)):
        if i+1 in [2**j for j in range(len(parity_bits))]:
            encoded_data.append(parity_bits[data_index])
            data_index += 1
        else:
            encoded_data.append(int(data[i-data_index]))
    return encoded_data

def verificar_error(encoded_data):
    # Verifica si hay errores en los datos codificados
    error_positions = []
    for i in range(len(encoded_data)):
        if i+1 in [2**j for j in range(int(math.log2(len(encoded_data)))+1)]:
            parity_bit = 0
            for j in range(len(encoded_data)):
                if (i+1) & (1 << j):
                    parity_bit ^= int(encoded_data[j])
            if parity_bit != 0:
                error_positions.append(i)
    return error_positions

def corregir_error(encoded_data, error_positions):
    # Corrige los errores en los datos codificados
    for position in error_positions:
        encoded_data[position] ^= 1
    return encoded_data
