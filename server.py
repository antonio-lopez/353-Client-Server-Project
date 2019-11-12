import socket
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import ast

#Generate private and public keys
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()

#Declartion
mysocket = socket.socket()
host = socket.gethostbyname(socket.getfqdn())
port = 7777
encrypt_str = "encrypted_message="  # used to detect start of encrypted message
client_response = "Client: OK".encode() # convert string to bytes

print("host = " + host)

#Prevent socket.error: [Errno 98] Address already in use
mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

mysocket.bind((host, port))

mysocket.listen(5)

c, addr = mysocket.accept()

while True:
    #Wait until data is received.
    data = c.recv(1024)
    data = data.replace("\r\n".encode(), ''.encode()) #remove new line character

    # comparisons are made between bytes in the if-statements
    if data == client_response:
        c.send(public_key.exportKey())
        print("OK received from client")
        print("Public key sent to client\n")
        print(public_key.exportKey())

    elif encrypt_str.encode() in data:  # if encrypt_str "header" is detected 
        data = data.replace(encrypt_str.encode(), ''.encode())  # remove "header"
        print("\nReceived Encrypted message = ", data)
        decryptor = PKCS1_OAEP.new(private_key)
        decrypted = decryptor.decrypt(ast.literal_eval(str(data)))  # decrypt message
        c.send("Server: OK".encode())
        print("\nDecrypting message...")
        print("Decrypted message = ", decrypted)    # print decrypted message
        print("Sending OK to client")

    elif data == "Quit".encode(): 
        break

#Server to stop
c.send("Server stopped".encode())
print("Server stopped")
c.close()
