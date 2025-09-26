from multiprocessing import Process, Pipe, Manager
from os import getpid
from datetime import datetime

# =======================
# Funciones auxiliares
# =======================

def local_time(counter):
    return f" Lamport={counter}"

def calc_recv_timestamp(recv_time_stamp, counter):
    return max(recv_time_stamp, counter) + 1

def event(pid, counter, process_map):
    counter += 1
    logical_id = process_map.get(pid, "??")
    print(f"Lonely event at {logical_id}" + local_time(counter))
    return counter

def send_message(pipe, pid, counter, process_map):
    counter += 1
    pipe.send(("Mensaje", counter))
    logical_id = process_map.get(pid, "??")
    print(f"Sent from {logical_id}" + local_time(counter))
    return counter

def recv_message(pipe, pid, counter, process_map):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    logical_id = process_map.get(pid, "??")
    print(f"Recived in {logical_id}" + local_time(counter))
    return counter

# =======================
# Definición de procesos
# =======================

def process_one(p12, p13, p41, p71, process_map):
    pid = getpid()
    process_map[pid] = 1
    counter = 0

    counter = event(pid, counter, process_map)
    counter = send_message(p12, pid, counter, process_map)
    counter = send_message(p13, pid, counter, process_map)
    counter = recv_message(p41, pid, counter, process_map)
    counter = recv_message(p71, pid, counter, process_map)
    counter = event(pid, counter, process_map)

def process_two(p21, p24, p25, p62, process_map):
    pid = getpid()
    process_map[pid] = 2
    counter = 0

    counter = recv_message(p21, pid, counter, process_map)
    counter = event(pid, counter, process_map)
    counter = send_message(p24, pid, counter, process_map)
    counter = send_message(p25, pid, counter, process_map)
    counter = recv_message(p62, pid, counter, process_map)

def process_three(p31, p36, p73, process_map):
    pid = getpid()
    process_map[pid] = 3
    counter = 0

    counter = recv_message(p31, pid, counter, process_map)
    counter = event(pid, counter, process_map)
    counter = send_message(p36, pid, counter, process_map)
    counter = recv_message(p73, pid, counter, process_map)

def process_four(p42, p47, p41, process_map):
    pid = getpid()
    process_map[pid] = 4
    counter = 0

    counter = recv_message(p42, pid, counter, process_map)
    counter = event(pid, counter, process_map)
    counter = send_message(p47, pid, counter, process_map)
    counter = send_message(p41, pid, counter, process_map)

def process_five(p52, p56, p57, process_map):
    pid = getpid()
    process_map[pid] = 5
    counter = 0

    counter = recv_message(p52, pid, counter, process_map)
    counter = event(pid, counter, process_map)
    counter = send_message(p56, pid, counter, process_map)
    counter = send_message(p57, pid, counter, process_map)

def process_six(p63, p65, p62, process_map):
    pid = getpid()
    process_map[pid] = 6
    counter = 0

    counter = recv_message(p63, pid, counter, process_map)
    counter = recv_message(p65, pid, counter, process_map)
    counter = event(pid, counter, process_map)
    counter = send_message(p62, pid, counter, process_map)

def process_seven(p74, p75, p71, p73, process_map):
    pid = getpid()
    process_map[pid] = 7
    counter = 0

    counter = recv_message(p74, pid, counter, process_map)
    counter = recv_message(p75, pid, counter, process_map)
    counter = event(pid, counter, process_map)
    counter = send_message(p71, pid, counter, process_map)
    counter = send_message(p73, pid, counter, process_map)

# =======================
# Programa principal
# =======================

if __name__ == "__main__":
    manager = Manager()
    process_map = manager.dict()

    # Crear Pipes (bidireccionales, usamos un extremo por proceso)
    p12, p21 = Pipe()
    p13, p31 = Pipe()
    p24, p42 = Pipe()
    p25, p52 = Pipe()
    p36, p63 = Pipe()
    p56, p65 = Pipe()
    p47, p74 = Pipe()
    p57, p75 = Pipe()
    p41, p14 = Pipe()
    p62, p26 = Pipe()
    p71, p17 = Pipe()
    p73, p37 = Pipe()

    # Crear procesos
    process1 = Process(target=process_one, args=(p12, p13, p14, p17, process_map))
    process2 = Process(target=process_two, args=(p21, p24, p25, p26, process_map))
    process3 = Process(target=process_three, args=(p31, p36, p37, process_map))
    process4 = Process(target=process_four, args=(p42, p47, p41, process_map))
    process5 = Process(target=process_five, args=(p52, p56, p57, process_map))
    process6 = Process(target=process_six, args=(p63, p65, p62, process_map))
    process7 = Process(target=process_seven, args=(p74, p75, p71, p73, process_map))

    # Iniciar procesos
    process1.start()
    process2.start()
    process3.start()
    process4.start()
    process5.start()
    process6.start()
    process7.start()

    # Esperar que terminen
    process1.join()
    process2.join()
    process3.join()
    process4.join()
    process5.join()
    process6.join()
    process7.join()

    # Mostrar mapeo final
    print("\n=== Mapa de Procesos (PID -> Número lógico) ===")
    print(dict(process_map))
