import socket
import threading

def connect_to_server(host, port, panel_mensajes):
    obj = socket.socket()
    obj.connect((host, port))
    panel_mensajes.insert('end', "Conectado al servidor\n")

    def receive_messages():
        while True:
            recibido = obj.recv(1024).decode('utf-8')
            if not recibido:
                break
            panel_mensajes.insert('end', f"{recibido}\n")
        obj.close()
        panel_mensajes.insert('end', "Conexión cerrada\n")

    thread = threading.Thread(target=receive_messages)
    thread.start()

    return obj