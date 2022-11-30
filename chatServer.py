import socket
from threading import Thread, Lock
import time

lock = Lock()

class Th(Thread):

    def __init__(self, mode):
        Thread.__init__(self)
        global nickname
        self.nickname = nickname
        global s
        self.sock = s
        self.mode = mode

    def run(self):
        global listaAddr
        global listaTime
        if self.mode == 'r':
            while True:
                (data, addr) = self.sock.recv(500)
                msgPessoa = data.decode('utf-8')
                print(msgPessoa)
                lock.acquire()
                if addr not in listaAddr:
                    nickPessoa = msgPessoa[0:msgPessoa.index(":")]
                    listaAddr[addr] = nickPessoa
                listaTime[addr] = time.time()
                lock.release()
        elif self.mode == 'e':
            while True:
                msg = input("Escreve sua msg:")
                if msg == "#list":
                    lock.acquire()
                    for endereco in listaTime.keys():
                        if listaTime[endereco] - time.time() > 60:
                            del listaAddr[endereco]
                            del listaTime[endereco]
                        print(listaAddr[endereco])
                    lock.release()
                else:
                    enviado = self.nickname + ":" + msg
                    self.sock.sendto(bytes(enviado, 'utf-8'), ("224.0.0.200", 2020))

HOSTIP = "172.16.1.4"
PORTA = 8123 # The port used by the server
addr = (HOSTIP, PORTA)

nickname = input("Insere teu nickname:")

listaAddr = {}
listaTime = {}

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(addr)

thEnvia = Th('e')
thRecebe = Th('r')
thEnvia.start()
thRecebe.start()
