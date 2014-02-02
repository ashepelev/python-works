import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
import random


key = RSA.generate(1024)
pemKey = key.exportKey('PEM')
publickey=key.publickey().exportKey()
print(pemKey)
print(publickey)
#print(len(publickey))


aes_key = Random.new().read(AES.block_size)
#for i in range(0,16):
#	aes_key+=chr(random.randint(0,128))
print(aes_key)
print(len(aes_key))


publickey = key.publickey()
message = aes_key
ciphertext, *k = publickey.encrypt(message, 0)
print(ciphertext)
print(len(ciphertext))

message = key.decrypt(ciphertext)

print(message)
print(aes_key)
print(len(aes_key))
iv = Random.new().read(AES.block_size)
cipher = AES.new(aes_key,AES.MODE_CBC,iv)

msg = b'PBK ' + key.publickey().exportKey()
print(msg)
