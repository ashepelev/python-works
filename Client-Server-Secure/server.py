import socket
import threading
import socketserver
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.cur_thread = threading.current_thread()
        self.numbers = []
        self.userLogged = False
        self.pbk_recieved = False
        while True:
            if not self.pbk_recieved:
                data = self.getData()
                if data=="BYE":
                    self.sendRequest("Connection closed!")
                    break
                elif not (self.userLogged or data.startswith("HLO")):
                    self.sendRequest("You should authorize first")
                elif data.startswith("PBK"):
                    self.obtainPBK(data)                    
                    self.pbk_recieved = True    
                else:
                    self.obtainRequest(data)              
            else:
                data = self.getEncryptedData()
                if data.startswith("BYE"):
                    self.sendEncryptedRequest("Connection closed!")
                    break
                self.obtainRequest(data)             

    def getData(self):
        print("{}: client ({}) connected".format(self.cur_thread, \
                self.client_address))
        data = str(self.request.recv(1024),'utf8')
        print("{}: data accepted: {}".format(self.cur_thread, data))
        return data
    
    def getEncryptedData(self):
        data = self.request.recv(1024)
        msg = data
        cipher = AES.new(self.aes_key,AES.MODE_CBC, msg[:AES.block_size])
        data = cipher.decrypt(msg[AES.block_size:])
        print("{}: data accepted: {}".format(self.cur_thread, str(data,'utf8')))
        return str(data,'utf8')

    def obtainPBK(self,data):
        ss = data.split()
        publickey = data.replace('PBK ','')
        publickey = RSA.importKey(publickey)
        self.aes_key = Random.new().read(AES.block_size)
        ciphertext, *k = publickey.encrypt(self.aes_key, 0)
        msg = ciphertext    
        self.request.sendall(msg)

    def checkLogin(self,login):
        found=False
        for l in open("users.txt",'r'):
            if l==login:
                found=True
                break
        if found:
            f = open("users.txt",'a')
            print(login,file=f)
            f.close()
        return

    def obtainRequest(self,data):
        if data.startswith("HLO"):            
            ss = data.strip().split()
            if not self.checkMsg(ss,"Need login after HLO: HLO <login>"):
                return
            self.obtainLogin(ss)
        elif data.startswith("NMR"):
            if not self.makeChecks():
                return
            ss = data.strip().split()
            if not self.checkMsg(ss,"Need integer after NMR: NMR <integer>"):
                return
            self.obtainNumber(ss,data)
        elif data.startswith("SUM"):
            if not self.makeChecks():
                return
            calc_sum = self.calculateSum()
            self.sendEncryptedRequest("SUM = " + str(calc_sum))
        else:
            self.sendEncryptedRequest("Wrong Command!")
        return

    def sendRequest(self,text):
        self.request.sendall(bytes(text,'utf8'))
        print("{}: data sended: {}".format(self.cur_thread, text))

    def sendEncryptedRequest(self,text):
        temp = text
        for i in range(0,16-len(temp)%16):
            text+=' '
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.aes_key,AES.MODE_CBC,iv)
        msg = bytes(text,'utf8')
        ciphertext = cipher.encrypt(msg)
        msg = iv + ciphertext
        self.request.sendall(msg)

    def calculateSum(self):
        calc_sum = 0
        for i in self.numbers:
            calc_sum += i
        return calc_sum

    def checkMsg(self,ss,msg):
        if len(ss)==1:
            self.sendEncryptedRequest(msg)
            return False
        return True

    def makeChecks(self):
        if not self.userLogged:
            self.sendEncryptedRequest("You must login first!")
            return False
        return True

    def obtainNumber(self, ss, data):
        try:
            number = int(ss[1])
            self.numbers += [number]
            self.sendEncryptedRequest("Number accepted")
        except ValueError:
            response="Wrong number in " + data
            self.sendEncryptedRequest(response)
        return

    def obtainLogin(self,ss):
        login = ss[1]
        self.checkLogin(login)
        self.userLogged = True
        if self.pbk_recieved:
            self.sendEncryptedRequest("Login accepted")
        else:
            self.sendRequest("Login accepted")
        return

    def checkIfLogged(self):
        if self.userLogged:
            self.sendEncryptedRequest("You have already logged in!")
        
        
class MyThreadedTCPServer(socketserver.ThreadingMixIn,
        socketserver.TCPServer):
    pass

if __name__ =="__main__":
    
    HOST, PORT ="localhost", 1234
    server = MyThreadedTCPServer((HOST, PORT),MyTCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    #server_thread.daemon = True
    server_thread.start()
    print("Server started!")
