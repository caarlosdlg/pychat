import socket
import threading
from message import recibir

def start_server(host, panel_mensajes, send_message_event, port=8050):
    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ser.bind((host, port))
    ser.listen(1)
    clients = []

    def handle_client(cli, addr):
        while True:
            recibido = cli.recv(1024)
            message, crc = recibir(recibido)
            if message == "Error en la transmisión de datos":
                print(message)
            else:
                panel_mensajes.insert('end', f"Mensaje: {message}, CRC: {crc} se usó hamming\n")

        cli.close()
        

        
        
    def accept_connections():
        while True:
            cli, addr = ser.accept()
            clients.append(cli)
            panel_mensajes.insert('end', f"Recibo conexion de la IP: {addr[0]} Puerto: {addr[1]}\n")
            thread = threading.Thread(target=handle_client, args=(cli, addr))
            thread.start()

    def send_messages(message):
        for cli in clients:
            send_message_event(cli, message)

    thread = threading.Thread(target=accept_connections)
    thread.start()
