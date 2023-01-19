# Import required modules
import socket
import threading

# Import the RSA functions from a separate module
from rsa_fun import *

# IP address for connection
IP = "localhost"

# Port for sending messages
PORT_S = 1234

# Port for receiving messages
PORT_R = 50036

# Define a thread for the client
class Client1 (threading.Thread):
    def __init__(self, login, sendTo):
        # Store the client's login name and the name of the person to send messages to
        self.login = login
        self.sendTo = sendTo

        # Generate the client's RSA keys and store them
        self.myKey, self.pubKey = getKeys(login, sendTo)

        # Start two threads, one for sending messages and one for receiving messages
        x1 = threading.Thread(target=self.sending)
        x2 = threading.Thread(target=self.receiving)
        x1.start()
        x2.start()

    def sending(self):
        # Open a UDP socket for sending messages
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((IP, PORT_S))

        # Continuously prompt the user to enter a message to send
        while True:
            print()
            msg = input("Enter the message you want to send")

            # Encrypt the message using the recipient's public key
            encrytMsg = encrypt(msg, self.pubKey)

            # Send the encrypted message
            s.send(encrytMsg)
            print()

    def receiving(self):
        # Open a UDP socket for receiving messages
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((IP, PORT_R))

        # Continuously receive messages and print them
        while True:
            encrytedMsg = s.recvfrom(PORT_S)

            # Decrypt the received message using the client's private key
            Msg = decrypt(encrytedMsg[0], self.myKey)
            print()
            print("from ", self.sendTo, " :", Msg)
            print()

# Create a Client1 object with login name "salma" and recipient name "amira"
c = Client1("salma", "amira")
