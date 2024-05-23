import binascii

def string_a_binario(s):
    return ''.join(format(ord(i), '08b') for i in s)

def binario_a_string(b):
    return ''.join(chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8))

def calcular_crc(b):
    crc = 0
    for bit in b:
        crc ^= int(bit)
    return crc

def enviar(s):
    binario = string_a_binario(s)
    crc = calcular_crc(binario)
    return binario + '|' + str(crc)

def recibir(b):
    binario, crc_recibido = b.split('|')
    crc_recibido = int(crc_recibido)
    crc_calculado = calcular_crc(binario)
    if crc_recibido == crc_calculado:
        return binario_a_string(binario)
    else:
        return "Error en la transmisión de datos"

def send_message(socket_connection, message):
    if socket_connection and message:
        mensaje_binario = enviar(message)
        mensaje_string = binario_a_string(mensaje_binario.split('|')[0])  # Convertir de nuevo a string
        socket_connection.send(mensaje_string.encode('utf-8'))
        
def receive_messages(socket_connection, panel_mensajes):
    while True:
        try:
            mensaje_binario = socket_connection.recv(1024).decode('utf-8')
            message = recibir(mensaje_binario)
            if message == "Error en la transmisión de datos":
                print(message)
            else:
                panel_mensajes.insert('end', message)
        except Exception as e:
            print(f"Error al recibir mensaje: {e}")
            break