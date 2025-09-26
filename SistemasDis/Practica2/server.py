import socket
import datetime

direcServidor = "localhost"
puertoServidor = 9899

# Abrimos el Socket
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Avisar al SO de creación de socket y asociar el prog al socket
socketServidor.bind((direcServidor, puertoServidor))

# Escuchar la conexión y atenderla
socketServidor.listen(5)
print(f"Servidor escuchando en {direcServidor}:{puertoServidor}")

while True:
    # Aceptar conexiones de clientes
    socketConexion, addr = socketServidor.accept()
    print("Conectado con cliente", addr)

    # Se calcula la hora después de la petición
    hora = datetime.datetime.now()

    # Convirtiendo a cadena (YYYYMMDD HH:MM:SS.microseconds)
    horaCadena = hora.strftime('%Y%m%d %H:%M:%S.%f')

    # Notificación de la hora y la fecha
    print("Envio la hora al cliente", addr)
    print(hora)

    socketConexion.send(horaCadena.encode())
    socketConexion.close()
