import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def encrypt_message(public_key, message):
    cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
    return cipher.encrypt(message.encode())

def connect_to_alice_and_send_message(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print("Connected to Alice")

        public_key = client_socket.recv(1024)
        message = input("Enter a message to send to Alice: ")
        ciphertext = encrypt_message(public_key, message)

        client_socket.send(ciphertext)
        print("Message sent to Alice")

if __name__ == "__main__":
    try:
        connect_to_alice_and_send_message()
    except Exception as e:
        print(f"An error occurred: {e}")
