import socket

HOST = input("Insira o ip do servidor ao qual quer se conectar\n")
PORT = input("Insira a porta do servidor ao qual quer se conectar\n")
SERVER_NAME = ""

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        SERVER_NAME = s.recv(64)
        print(f"Conectado ao servidor {SERVER_NAME}")
        message = input("Say: ")
        s.sendall(bytes(message, 'utf-8'))
