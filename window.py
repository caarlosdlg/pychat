import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
from server import start_server
from client import connect_to_server
from message import send_message, receive_messages

# Variable global para almacenar la conexión del socket
socket_connection = None

def create_window():
    global socket_connection

    window = tk.Tk()  # Crea una nueva ventana
    window.title("Aplicación de Mensajes")  # Establece el título de la ventana

    # Define una fuente atractiva
    nice_font = ("Helvetica", 14)

    panel_mensajes = scrolledtext.ScrolledText(window, bg='black', fg='white', font=nice_font)
    textbox = tk.Entry(window, bg='black', fg='white', font=nice_font)

    marco_computadoras = tk.Frame(window, bg='black')
    panel_computadoras = tk.Listbox(marco_computadoras, bg='black', fg='white', font=nice_font)

    # Función para manejar el evento del botón de envío
    def send_message_event(event=None):  # se agrega el parámetro event
        message = textbox.get()
        textbox.delete(0, 'end')
        send_message(socket_connection, message)

    boton_enviar = tk.Button(window, text="Enviar", command=send_message_event, font=nice_font, bg='grey', fg='white')

    # Vincula el evento de presionar Enter al widget de entrada de texto
    textbox.bind('<Return>', send_message_event)

    # Función para manejar el evento del botón "Cliente"
    def connect_to_server_event():
        global socket_connection
        socket_connection = connect_to_server('localhost', 8050, panel_mensajes)
        Thread(target=receive_messages, args=(socket_connection, panel_mensajes)).start()
        boton_cliente.config(bg='green')

    # Función para manejar el evento del botón "Servidor"
    def start_server_event():
        start_server('localhost', panel_mensajes, 8050)
        boton_servidor.config(bg='blue')
        textbox.config(state='disabled')

    boton_cliente = tk.Button(marco_computadoras, text="Cliente", bg='grey', fg='white', relief='groove', bd=10, command=connect_to_server_event, font=nice_font)
    boton_servidor = tk.Button(marco_computadoras, text="Servidor", bg='grey', fg='white', relief='groove', bd=10, command=start_server_event, font=nice_font)

    panel_mensajes.grid(row=0, column=0, sticky='nsew')
    marco_computadoras.grid(row=0, column=1, sticky='ns')
    panel_computadoras.pack(fill='both', expand=True)
    boton_cliente.pack(side='bottom', fill='x')
    boton_servidor.pack(side='bottom', fill='x')
    textbox.grid(row=1, column=0, sticky='ew')
    boton_enviar.grid(row=1, column=1, sticky='ew')

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    window.mainloop()  # Inicia el bucle principal de la ventana

if __name__ == "__main__":
    create_window()