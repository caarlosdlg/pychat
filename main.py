from multiprocessing import Process
from window import create_window

def main():
    # Crea dos procesos, cada uno ejecutando una instancia de la aplicación
    p1 = Process(target=create_window)
    p2 = Process(target=create_window)

    # Inicia los procesos
    p1.start()
    p2.start()

    # Espera a que ambos procesos terminen
    p1.join()
    p2.join()

if __name__ == "__main__":
    main()
    
    
    # carlos medina chupame la verga 