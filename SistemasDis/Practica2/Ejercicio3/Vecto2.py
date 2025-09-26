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

    vector[idx] += 1
    print(f"Received in P{idx+1}" + local_time(vector))
    return vector

# =======================
# Definición de procesos
# =======================

def process_one(p12, p51, process_map, n):
    pid = getpid()
    process_map[pid] = 0
    vector = [0]*n

    vector = event(pid, vector, process_map, n)
    vector = send_message(p12, pid, vector, process_map, n)
    vector = recv_message(p51, pid, vector, process_map, n)
    vector = event(pid, vector, process_map, n)

def process_two(p21, p23, p24, process_map, n):
    pid = getpid()
    process_map[pid] = 1
    vector = [0]*n

    vector = recv_message(p21, pid, vector, process_map, n)
    vector = event(pid, vector, process_map, n)
    vector = send_message(p23, pid, vector, process_map, n)
    vector = send_message(p24, pid, vector, process_map, n)

def process_three(p32, p35, process_map, n):
    pid = getpid()
    process_map[pid] = 2
    vector = [0]*n

    vector = recv_message(p32, pid, vector, process_map, n)
    vector = event(pid, vector, process_map, n)
    vector = send_message(p35, pid, vector, process_map, n)

def process_four(p42, p45, process_map, n):
    pid = getpid()
    process_map[pid] = 3
    vector = [0]*n

    vector = recv_message(p42, pid, vector, process_map, n)
    vector = event(pid, vector, process_map, n)
    vector = send_message(p45, pid, vector, process_map, n)

def process_five(p53, p54, p51, process_map, n):
    pid = getpid()
    process_map[pid] = 4
    vector = [0]*n

    vector = recv_message(p53, pid, vector, process_map, n)
    vector = recv_message(p54, pid, vector, process_map, n)
    vector = event(pid, vector, process_map, n)
    vector = send_message(p51, pid, vector, process_map, n)

# =======================
# Programa principal
# =======================

if __name__ == "__main__":
    manager = Manager()
    process_map = manager.dict()
    n = 5  # number of processes

    # Crear Pipes
    p12, p21 = Pipe()
    p23, p32 = Pipe()
    p24, p42 = Pipe()
    p35, p53 = Pipe()
    p45, p54 = Pipe()
    p51, p15 = Pipe()

    # Crear procesos
    process1 = Process(target=process_one, args=(p12, p15, process_map, n))
    process2 = Process(target=process_two, args=(p21, p23, p24, process_map, n))
    process3 = Process(target=process_three, args=(p32, p35, process_map, n))
    process4 = Process(target=process_four, args=(p42, p45, process_map, n))
    process5 = Process(target=process_five, args=(p53, p54, p51, process_map, n))

    # Iniciar procesos
    process1.start()
    process2.start()
    process3.start()
    process4.start()
    process5.start()

    # Esperar que terminen
    process1.join()
    process2.join()
    process3.join()
    process4.join()
    process5.join()

    # Mostrar mapeo final
    print("\n=== Mapa de Procesos (PID -> Índice lógico) ===")
    print(dict(process_map))
