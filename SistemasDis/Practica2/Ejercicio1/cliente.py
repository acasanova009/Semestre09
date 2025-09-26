import socket
import time
import datetime

def convertirCadenaAHora(cadena):
    formato = '%Y%m%d %H:%M:%S.%f'
    horaCadena = datetime.datetime.strptime(cadena, formato)
    return horaCadena

IPServidor = "localhost"
puertoServidor = 9899   # debe coincidir con el servidor

# Apertura del socket
socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

inicio = time.time()
# Solicitar conexión con el servidor
socketCliente.connect((IPServidor, puertoServidor))

# Recibir del servidor
horaCadena = socketCliente.recv(4096).decode()
final = time.time()
tiempo = final - inicio

hora = convertirCadenaAHora(horaCadena)
print("El tiempo total de ida y vuelta fue:", tiempo)

mitadtiempo = tiempo / 2
print("Tiempo estimado de ida:", mitadtiempo)
print("Hora servidor:", horaCadena)
print("La hora exacta (ajustada):", hora + datetime.timedelta(seconds=mitadtiempo))

socketCliente.close()
