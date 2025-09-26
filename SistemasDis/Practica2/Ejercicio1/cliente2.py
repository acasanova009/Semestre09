import socket
import time
import datetime

def convertirCadenaAHora(cadena):
    formato = '%Y%m%d %H:%M:%S.%f'
    horaCadena = datetime.datetime.strptime(cadena, formato)
    return horaCadena

IPServidor = "192.168.1.169"
puertoServidor = 9899

socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

inicio = time.time()
socketCliente.connect((IPServidor, puertoServidor))
horaCadena = socketCliente.recv(4096).decode()
time.sleep(2)
final = time.time()
socketCliente.close()

tiempo = final - inicio
mitadtiempo = tiempo / 2

horaServidor = convertirCadenaAHora(horaCadena)
horaAjustada = horaServidor + datetime.timedelta(seconds=mitadtiempo)

horaCliente = datetime.datetime.now()

# Función auxiliar para formatear segundos en min, s, ms
def formatear_tiempo(segundos):
    minutos = int(segundos // 60)
    segundos_enteros = int(segundos % 60)
    milisegundos = int((segundos - int(segundos)) * 1000)
    return f"{minutos} min {segundos_enteros} s {milisegundos} ms"


# Mostrar horas legibles
print("Hora servidor:", horaServidor.strftime("%H:%M:%S.%f")[:-3])  # hasta ms
print("Hora cliente:", horaCliente.strftime("%H:%M:%S.%f")[:-3])


print("Hora ajustada:", horaAjustada.strftime("%H:%M:%S.%f")[:-3])

# Comparación
if horaCliente > horaAjustada:
    print("El cliente está ADELANTADO respecto al servidor.")
elif horaCliente < horaAjustada:
    print("El cliente está ATRASADO respecto al servidor.")
else:
    print("El cliente y el servidor están sincronizados.")
