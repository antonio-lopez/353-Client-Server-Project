import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

server = socket.socket()
host = "192.168.1.114"
port = 7777

server.connect((host, port))

#Tell server that connection is OK
server.sendall("Client: OK".encode())
print("Connection established")
print("Sending OK to server...\n")

#Receive public key string from server
server_string = server.recv(1024)
print("Recieved public key from server: ", server_string)

#Remove extra characters
#server_string = server_string.replace("public_key=".encode(), ''.encode())
#server_string = server_string.replace("\r\n".encode(), ''.encode())
#print("New Recieved public key: ", server_string)

#Convert string to key
server_public_key = RSA.importKey(server_string)
encryptor = PKCS1_OAEP.new(server_public_key)

#Encrypt message and send to server
message = "Krabby Patty Formula"
encrypted = encryptor.encrypt(message.encode())
print("\nEncrypting message...")
print("Encrypted message = ", encrypted)
server.sendall("encrypted_message=".encode() + encrypted)

#Server's response
server_response = server.recv(1024)
print("\nServer_response: ", server_response.decode())
if server_response.decode() == "Server: OK":
    print("Server decrypted message successfully")
    server.sendall("Quit".encode())

#Tell server to finish connection
print(server.recv(1024).decode()) #Quit server response
server.close()
