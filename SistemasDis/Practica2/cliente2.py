import socket
import time
import datetime

def convertirCadenaAHora(cadena):
    formato = '%Y%m%d %H:%M:%S.%f'
    horaCadena = datetime.datetime.strptime(cadena, formato)
    return horaCadena

IPServidor = "localhost"
puertoServidor = 9899

socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

inicio = time.time()
socketCliente.connect((IPServidor, puertoServidor))
horaCadena = socketCliente.recv(4096).decode()
final = time.time()
socketCliente.close()

tiempo = final - inicio
mitadtiempo = tiempo / 2

horaServidor = convertirCadenaAHora(horaCadena)
horaAjustada = horaServidor + datetime.timedelta(seconds=mitadtiempo)

horaCliente = datetime.datetime.now()

print("RTT total:", tiempo)
print("Tiempo estimado de ida:", mitadtiempo)
print("Hora servidor:", horaServidor)
print("Hora ajustada:", horaAjustada)
print("Hora cliente:", horaCliente)

# Comparación C vs Cc
if horaCliente > horaAjustada:
    print("El cliente está ADELANTADO respecto al servidor.")
elif horaCliente < horaAjustada:
    print("El cliente está ATRASADO respecto al servidor.")
else:
    print("El cliente y el servidor están sincronizados.")
