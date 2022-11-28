import socket
import threading
import time
from multiprocessing import shared_memory

shm_a = shared_memory.SharedMemory(create=True, size=1024)
listaAddr = shm_a

HOSTNAME = socket.gethostname()
#HOSTIP = socket.gethostbyname(HOSTNAME)
HOSTIP = "127.0.0.1"
PORTA = 8123 # The port used by the server
addr = (HOSTIP, PORTA)

def counter(listaTime, listaAddr):
    while True:
        for el in listaTime:
            if time.time() - el.value:
                print(f"{listaAddr[el.key]} saiu por inatividade.")
                listaTime.pop(el.key)
                listaAddr.pop(el.key)

print("Inicializando Servidor")
print(f"{HOSTNAME} hosteando {HOSTIP}:{PORTA}")
print("Aguardando conexões\n")

listaAddr = {}
listaTime = {}

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # Bind the socket to the port
    server_address = addr
    s.bind(server_address)
    while True:
        (data, addr) = s.recv(1024)
        if addr not in listaAddr:
            s.send(b"Varzinha")
            print(f"{data} entrou no chat!\n")
            listaAddr[addr] = data
        else:
            nickname = listaAddr[addr]
            if data == "#sair":
                break
            print(f"{nickname}:{data}")
            s.sendall(data)
        listaTime[addr] = time.time()
