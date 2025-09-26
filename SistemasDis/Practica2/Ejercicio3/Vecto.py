from multiprocessing import Process, Pipe, Manager
from os import getpid

# =======================
# Funciones auxiliares
# =======================

def local_time(vector):
    return f" VC={vector}"

def event(pid, vector, process_map, n):
    idx = process_map.get(pid, None)
    vector[idx] += 1
    print(f"Lonely event at P{idx+1}" + local_time(vector))
    return vector

def send_message(pipe, pid, vector, process_map, n):
    idx = process_map.get(pid, None)
    vector[idx] += 1
    pipe.send(("Mensaje", vector.copy()))
    print(f"Sent from P{idx+1}" + local_time(vector))
    return vector

def recv_message(pipe, pid, vector, process_map, n):
    msg, msg_vector = pipe.recv()
    idx = process_map.get(pid, None)

    # merge step
    for i in range(n):
        vector[i] = max(vector[i], msg_vector[i])

    # increment own clock
    vector[idx] += 1
    print(f"Received in P{idx+1}" + local_time(vector))
    return vector

# =======================
# Definición de procesos
# =======================

def process_one(pipe12, process_map, n):
    pid = getpid()
    process_map[pid] = 0  # index 0 for P1
    vector = [0]*n

    vector = event(pid, vector, process_map, n)
    vector = send_message(pipe12, pid, vector, process_map, n)
    vector = event(pid, vector, process_map, n)
    vector = recv_message(pipe12, pid, vector, process_map, n)
    vector = event(pid, vector, process_map, n)

def process_two(pipe21, pipe23, process_map, n):
    pid = getpid()
    process_map[pid] = 1
    vector = [0]*n

    vector = recv_message(pipe21, pid, vector, process_map, n)
    vector = send_message(pipe21, pid, vector, process_map, n)
    vector = send_message(pipe23, pid, vector, process_map, n)
    vector = recv_message(pipe23, pid, vector, process_map, n)

def process_three(pipe32, process_map, n):
    pid = getpid()
    process_map[pid] = 2
    vector = [0]*n

    vector = recv_message(pipe32, pid, vector, process_map, n)
    vector = send_message(pipe32, pid, vector, process_map, n)

# =======================
# Programa principal
# =======================

if __name__ == '__main__':
    manager = Manager()
    process_map = manager.dict()
    n = 3  # number of processes

    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    process1 = Process(target=process_one, args=(oneandtwo, process_map, n))
    process2 = Process(target=process_two, args=(twoandone, twoandthree, process_map, n))
    process3 = Process(target=process_three, args=(threeandtwo, process_map, n))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()

    print("\n=== Mapa de Procesos (PID -> Índice lógico) ===")
    print(dict(process_map))
