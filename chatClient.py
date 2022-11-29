import socket

HOST = "172.16.1.4"#input("Insira o ip do servidor ao qual quer se conectar\n")
PORT = 8123 #input("Insira a porta do servidor ao qual quer se conectar\n")
SERVER_NAME = ""
addr = (HOST, int(PORT))
nick = "Vorotex"

aux = 0


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
	while True:    
		if aux == 0:
		    aux = 1
		    s.sendto(bytes(nick, 'utf-8'), addr)
		    x = s.recvfrom(64)
		    SERVER_NAME = x[0].decode('utf-8')
		    print(f"Conectado ao servidor {SERVER_NAME}")
		message = input("Escreve aqui: ")
		s.sendto(bytes(message, 'utf-8'), addr)
		if message == '#sair':
		    break
		msg = s.recvfrom(1024)
		print(msg[0].decode('utf-8'))
