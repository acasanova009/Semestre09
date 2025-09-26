import socket
import datetime
import threading

def atender_cliente(socketConexion, addr):
    print("Conectado con cliente", addr)
    hora = datetime.datetime.now()
    horaCadena = hora.strftime('%Y%m%d %H:%M:%S.%f')
    socketConexion.send(horaCadena.encode())
    socketConexion.close()

def main():
    direcServidor = "0.0.0.0"   # acepta conexiones desde cualquier IP
    puertoServidor = 9899

    socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketServidor.bind((direcServidor, puertoServidor))
    socketServidor.listen(5)

    print(f"Servidor escuchando en {direcServidor}:{puertoServidor}")

    while True:
        socketConexion, addr = socketServidor.accept()
        hilo = threading.Thread(target=atender_cliente, args=(socketConexion, addr))
        hilo.start()

if __name__ == "__main__":
    main()
