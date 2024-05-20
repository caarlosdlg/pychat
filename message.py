def send_message(socket_connection, message):
    if socket_connection and message:
        socket_connection.send(message.encode('utf-8'))

def receive_messages(socket_connection, panel_mensajes):
    while True:
        try:
            message = socket_connection.recv(1024).decode('utf-8')
            panel_mensajes.insert('end', message)
        except Exception as e:
            print(f"Error al recibir mensaje: {e}")
            break