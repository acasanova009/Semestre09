from multiprocessing import Process, Pipe, Manager
from os import getpid
from datetime import datetime

# =======================
# Funciones auxiliares
# =======================

# Muestra el tiempo lógico y físico

def local_time(counter):
    return ' Lamport={}'.format(counter)

#def local_time(counter):
    return ' (Lamp={}, LocalTime={})'.format(counter, datetime.now())


# Regla de Lamport al recibir un mensaje
def calc_recv_timestamp(recv_time_stamp, counter):
    return max(recv_time_stamp, counter) + 1

# Evento local
def event(pid, counter, process_map):
    counter += 1
    logical_id = process_map.get(pid, "??")
    print(f'Lonely event at {logical_id}' + local_time(counter))
    return counter

# Enviar mensaje
def send_message(pipe, pid, counter, process_map):
    counter += 1
    pipe.send(('Mensaje', counter))
    logical_id = process_map.get(pid, "??")
    print("\n")

    print(f'Sent from {logical_id} '  + local_time(counter))
    return counter

# Recibir mensaje
def recv_message(pipe, pid, counter, process_map):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    logical_id = process_map.get(pid, "??")
    print(f'Recived in {logical_id} ' + local_time(counter))

    return counter

# =======================
# Definición de procesos
# =======================

def process_one(pipe12, process_map):
    pid = getpid()
    process_map[pid] = 1  # Asigna número lógico
    counter = 0

    counter = event(pid, counter, process_map)
    counter = send_message(pipe12, pid, counter, process_map)
    counter = event(pid, counter, process_map)
    counter = recv_message(pipe12, pid, counter, process_map)
    counter = event(pid, counter, process_map)

def process_two(pipe21, pipe23, process_map):
    pid = getpid()
    process_map[pid] = 2
    counter = 0

    counter = recv_message(pipe21, pid, counter, process_map)
    counter = send_message(pipe21, pid, counter, process_map)
    counter = send_message(pipe23, pid, counter, process_map)
    counter = recv_message(pipe23, pid, counter, process_map)

def process_three(pipe32, process_map):
    pid = getpid()
    process_map[pid] = 3
    counter = 0

    counter = recv_message(pipe32, pid, counter, process_map)
    counter = send_message(pipe32, pid, counter, process_map)

# =======================
# Programa principal
# =======================
if __name__ == '__main__':
    manager = Manager()
    process_map = manager.dict()  # Diccionario compartido entre procesos

    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    # Crear procesos
    process1 = Process(target=process_one, args=(oneandtwo, process_map))
    process2 = Process(target=process_two, args=(twoandone, twoandthree, process_map))
    process3 = Process(target=process_three, args=(threeandtwo, process_map))


    # Iniciar procesos
    process1.start()
    process2.start()
    process3.start()

    # Esperar que terminen
    process1.join()
    process2.join()
    process3.join()


    # Mostrar mapeo final PID -> número lógico
    print("\n=== Mapa de Procesos (PID -> Número lógico) ===")
    print(dict(process_map))
