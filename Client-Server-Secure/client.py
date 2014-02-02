import socket
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES

def genKey():
    key = RSA.generate(1024)
    return key

def obtainAESKey(rsa_key, msg):
    return rsa_key.decrypt(msg)

def encryptMsg(string, aes_key):
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
    print(decrypted.decode("utf8"))
    
hostname ="localhost"
port = 1234
#ipaddr = socket.gethostbyname(hostname)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((hostname, port))
helloInput="msg: "
pbk_key_sent = False
rsa_key = genKey()
aes_key = None
while True:
    string = input(helloInput)
    if not pbk_key_sent:
        if string=="PBK":
            pbk_key_sent = True
            msg = b'PBK ' + rsa_key.publickey().exportKey()
            s.sendall(msg)
            response = s.recv(1024)
            aes_key = obtainAESKey(rsa_key,response)
            print("Recieved AES-key: " + str(aes_key))
        else:
            s.sendall(string.encode("utf8"))    
            response = s.recv(1024)
            print(response.decode("utf8"))
            if response.decode("utf8")=="Login accepted":
                helloInput=string.strip().split()[1]+"@"+hostname+"$:"
            if string=="BYE":
                break
    else: 
        encryptMsg(string,aes_key)
        response = getAndDecryptMsg(s,aes_key)
        if string=="BYE":
            break
s.close()
