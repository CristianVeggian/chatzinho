import socket

HOST = input("Insira o ip do servidor ao qual quer se conectar\n")
PORT = input("Insira a porta do servidor ao qual quer se conectar\n")
SERVER_NAME = ""
addr = (HOST, int(PORT))

aux = 0

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        if aux == 0:
            aux = 1
            SERVER_NAME = s.recv(64)
            print(f"Conectado ao servidor {SERVER_NAME}")
        message = input("Escreve aqui: ")
        s.sendto(bytes(message, 'utf-8'), addr)
        if message == '#sair':
            break
