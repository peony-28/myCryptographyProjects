def caesar_cipher_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        # Check if character is uppercase letter
        if char.isupper():
            # Shift within the range of uppercase letters (A-Z)
            encrypted_text += chr((ord(char) + shift - 65) % 26 + 65)
        # Check if lowercase letter
        elif char.islower():
           
            encrypted_text += chr((ord(char) + shift - 97) % 26 + 97)
        # If not a letter, leave it as it is
        else:
            encrypted_text += char
    return encrypted_text

def main():
    # get input from the user
    message = input("Enter the message to encrypt: ")
    # Ask the user for the shift value
    shift = int(input("Enter the shift value: "))
    
    # Encrypt using Caesar Cipher
    encrypted_message = caesar_cipher_encrypt(message, shift)
    
    # Print the encrypted message
    print("Encrypted message:", encrypted_message)

if __name__ == "__main__":
    main()
