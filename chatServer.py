import socket
import threading
import time
from multiprocessing import shared_memory

shm_a = shared_memory.SharedMemory(create=True, size=1024)

conexoes = list()

shm_a.buf = conexoes

HOSTNAME = socket.gethostname()
HOSTIP = socket.gethostbyname(HOSTNAME)
PORTA = 8000 # The port used by the server

def thread_user(id, conexao):
    with conexao:
        nickname = conexao.recv(100)
        print(f"{nickname} entrou no chat!\n")
        shm_a.buf[id] = time.time()
        while True:
            data = conexao.recv(1024)
            if data < 0:
                if shm_a.buf[id] - time.time() > 60:
                    break
            else:
                print(f"{nickname}: {data}\n")
                if data == "#sair":
                    break
                shm_a.buf[id] = time.time()
                conexao.sendall(data)

print("Aguardando conexões\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOSTIP, PORTA))
    s.listen()
    conexao, endereco = s.accept()
    nickname = conexao.recv()
    conexoes.append(conexao)


while len(conexoes) != 0:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOSTIP, PORTA))
        s.listen()
        conexao, endereco = s.accept()
