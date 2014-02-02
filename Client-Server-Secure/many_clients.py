import threading
import socket
import random
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES

def getName(num):
    name = "HLO "+ "name"+num
    return name

def getNMR():
    nmr = "NMR " + str(random.randint(0,100))
    return nmr
    

def genKey():
    key = RSA.generate(1024)
    return key

def obtainAESKey(rsa_key, msg):
    return rsa_key.decrypt(msg)

def encryptMsg(s,string, aes_key):
    temp = string
    for i in range(0,16-len(temp)%16):
        string+=' '
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(aes_key,AES.MODE_CBC,iv)
    ciphertext = cipher.encrypt(string)
    msg = iv + ciphertext
    s.sendall(msg)

def getAndDecryptMsg(s,aes_key):
    response = s.recv(1024)
    msg = response
    cipher = AES.new(aes_key,AES.MODE_CBC, msg[:AES.block_size])
    decrypted = cipher.decrypt(msg[AES.block_size:])
    


def runClient(num):
    hostname ="localhost"
    port = 1234
    #ipaddr = socket.gethostbyname(hostname)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    helloInput="msg: "
    pbk_key_sent = False
    rsa_key = genKey()
    aes_key = None
    name = getName(num)
    s.sendall(name.encode("utf8"))
    s.recv(1024)
    count = 100
    string="PBK"    
    while True:
        if not pbk_key_sent:
            if string=="PBK":
                pbk_key_sent = True
                msg = b'PBK ' + rsa_key.publickey().exportKey()
                s.sendall(msg)
                response = s.recv(1024)
                aes_key = obtainAESKey(rsa_key,response)
            else:
                s.sendall(string.encode("utf8"))    
                response = s.recv(1024)
                if response.decode("utf8")=="Login accepted":
                    helloInput=string.strip().split()[1]+"@"+hostname+"$:"
                if string=="BYE":
                    break
        else: 
            count-=1
            actionNumber = random.randint(0,2)
            if actionNumber==0:
                string=getNMR()
            elif actionNumber==1:
                string="SUM"
            elif actionNumber==2:
                string=getName(num)
            if count==0:
                string="BYE"
            encryptMsg(s,string,aes_key)
            response = getAndDecryptMsg(s,aes_key)
            if string=="BYE":
                break        
    s.close()
    

    
    
    

threads = []

for i in range(0,10):
    thread = threading.Thread(target=runClient, args=(str(i)))
    thread.start()
    threads += [thread]

for thread in threads:
    thread.join()
