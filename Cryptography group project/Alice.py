import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_rsa_keys():
    key = RSA.generate(1024)
    public_key = key.publickey().export_key()
    private_key = key.export_key()
    return public_key, private_key

def decrypt_message(private_key, ciphertext):
    cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
    return cipher.decrypt(ciphertext)

def start_server(host='localhost', port=12345):
    public_key, private_key = generate_rsa_keys()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print("Alice waiting for connection...")

        client_socket, address = server_socket.accept()
        with client_socket:
            print(f"Connected to Bob at {address}")
            client_socket.send(public_key)

            ciphertext = client_socket.recv(1024)
            plaintext = decrypt_message(private_key, ciphertext)
            print("Decrypted message from Bob:", plaintext.decode())

if __name__ == "__main__":
    try:
        start_server()
    except Exception as e:
        print(f"An error occurred: {e}")
