# Import the required libraries for socket programming and RSA encryption
import socket
import threading
from rsa_fun import *

# IP address and port number for the client and server
IP = "localhost"
PORT_R = 1234
PORT_S = 50036

# Define the Client2 class as a threading.Thread class
class Client2(threading.Thread):
    def __init__(self, login, sendTo):
        # Initialize the login name and sendTo name
        self.login = login
        self.sendTo = sendTo
        # Get the private key and public key for the client
        self.myKey, self.pubKey = getKeys(login, sendTo)
        # Start two threads for sending and receiving messages
        x1 = threading.Thread(target=self.sending)
        x2 = threading.Thread(target=self.receiving)
        x1.start()
        x2.start()

    def sending(self):
        # The client creates a UDP socket and connects to the server at IP and PORT_S
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((IP, PORT_S))
        while True:
            # Prompt user to enter a message to send
            print()
            msg = input("Enter the message you want to send")
            # Encrypt the message using the public key of the receiver
            encrytMsg = encrypt(msg, self.pubKey)
            # Send the encrypted message through the socket
            s.send(encrytMsg)
            print()

    def receiving(self):
        # The client creates another UDP socket and binds to IP and PORT_R
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((IP, PORT_R))
        while True:
            # Receive encrypted message from the socket
            encrytedMsg = s.recvfrom(PORT_S)
            # Decrypt the message using the client's private key
            Msg = decrypt(encrytedMsg[0], self.myKey)
            print()
            # Print the received message along with the sender's name
            print("from ", self.sendTo, " :", Msg)
            print()

# Create an instance of the Client2 class with login name "amira" and sendTo name "samer"
c = Client2("amira", "salma")
