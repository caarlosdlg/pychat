import binascii
import random

def string_a_bytes(s):
    return s.encode('utf-8')

def bytes_a_string(b):
    return b.decode('utf-8')

def calcular_crc(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc



def enviar(s):
    data = string_a_bytes(s)
    crc = calcular_crc(data)
    # Simular un error en el CRC con una probabilidad del 10%
    if random.random() < 0.4:
        crc += 0x0001  # Añadir 1 al CRC para generar un error
    return data + b'|' + str(crc).encode('utf-8')

def recibir(b):
    data, crc_recibido = b.split(b'|')
    crc_recibido = int(crc_recibido)
    crc_calculado = calcular_crc(data)
    if crc_recibido == crc_calculado:
        return bytes_a_string(data), crc_recibido
    else:
        return "Error en la transmisión de datos", None

def send_message(socket_connection, message):
    if socket_connection and message:
        mensaje_binario = enviar(message)
        socket_connection.send(mensaje_binario)

def receive_messages(socket_connection, panel_mensajes):
    while True:
        try:
            mensaje_binario = socket_connection.recv(1024)
            message, crc = recibir(mensaje_binario)
            if message == "Error en la transmisión de datos":
                print(message)
            else:
                panel_mensajes.insert('end', f"Mensaje: {message}, CRC: {crc}")
                
        except Exception as e:
            print(f"Error al recibir mensaje: {e}")
            panel_mensajes.insert('end', f"Mensaje: {message}, Corregido con Hamming: {decodificar_hamming(message)}")    
            break

def calcular_hamming(data):
    data = list(map(int, str(data)))
    n = len(data)
    r = 1
    while(2**r < r + n + 1):
        r += 1
    arr = ['0'] * (r + n)
    j = 0
    for i in range(1, len(arr) + 1):
        if(i == 2**j):
            j += 1
        else:
            arr[i - 1] = str(data[-1])
            data.pop()
    arr.reverse()
    j = 0
    for i in range(1, len(arr) + 1):
        if(i == 2**j):
            parity = 0
            for k in range(i, len(arr) + 1, i*2):
                parity ^= int(arr[-k])
            arr[-i] = str(parity)
            j += 1
    arr.reverse()
    return ''.join(arr)

def decodificar_hamming(data):
    data = list(map(int, str(data)))
    data.reverse()
    n = len(data)
    r = 1
    while(2**r <= n):
        r += 1
    for i in range(r):
        val = 0
        for j in range(1, n + 1):
            if(j & (2**i) == (2**i)):
                val = val ^ int(data[-1 * j])
        data[-1 * (2**i)] = val
    data.reverse()
    power_vals = [2**i for i in range(r)]
    error_loc = sum([data[-1 * i - 1] * i for i in power_vals])
    if(error_loc >= 1):
        data[-1 * error_loc - 1] = 1 - data[-1 * error_loc - 1]
        print('Error is at position', error_loc)
    data = [data[-1 * i - 1] for i in range(1, n + 1) if i not in power_vals]
    return ''.join(map(str, data))