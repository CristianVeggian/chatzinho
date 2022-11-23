import socket
import threading
import time
from multiprocessing import shared_memory

shm_a = shared_memory.SharedMemory(create=True, size=1024)
conexoes = shm_a

HOSTNAME = socket.gethostname()
#HOSTIP = socket.gethostbyname(HOSTNAME)
HOSTIP = ""
PORTA = 12000 # The port used by the server

def counter():
    while True:
        for con in conexoes:
            if time.time() - con[2] > 60:
                print(f"{con[0]} saiu por inatividade.")
                con[1].close()
                shm_a.buf.pop(con)

print("Inicializando Servidor\n")
print(f"{HOSTNAME} hosteando {HOSTIP}:{PORTA}\n")
print("Aguardando conexões\n")

listaAddr = {}

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOSTIP, PORTA))
    while True:
        (data, addr) = s.recv(1024)
        if addr not in listaAddr:
            s.send(b"Conectado em Varzinha:")
            print(f"{data} entrou no chat!\n")
            listaAddr[addr] = data
        else:
            nickname = listaAddr[addr]
            if data == "#sair":
                break
            print(f"{nickname}:{data}")
            shm_a.buf[id] = time.time()
            s.sendall(data)

