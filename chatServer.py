import socket
import threading
import time
from multiprocessing import shared_memory

conexoes = list()
shm_a = shared_memory.SharedMemory(create=True, size=1024)
shm_a.buf = conexoes

HOSTNAME = socket.gethostname()
HOSTIP = socket.gethostbyname(HOSTNAME)
PORTA = 8000 # The port used by the server

def counter():
    while True:
        for con in conexoes:
            if time.time() - con[2] > 60:
                print(f"{con[0]} saiu por inatividade.")
                con[1].close()
                shm_a.buf.pop(con)

print("Aguardando conexões\n")

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOSTIP, PORTA))
        s.listen()
        conexao, endereco = s.accept()
        nickname = conexao.recv(128)
        conexoes.append((nickname, conexao, time.time()))
        with conexao:
            conexao.sendall(b"Varzinha")
            print(f"{nickname} entrou no chat!\n")
            while True:
                data = conexao.recv(1024)
                print(f"{nickname}: {data}\n")
                if data == "#sair":
                    break
                shm_a.buf[id] = time.time()
                conexao.sendall(data)

