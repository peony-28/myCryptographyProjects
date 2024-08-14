def caesar_cipher_decrypt(cipher_text, shift):
    decrypted_text = ""
    for char in cipher_text:
        # Check if the character is an uppercase letter
        if char.isupper():
            # Shift within the range of uppercase letters (A-Z) in the reverse direction
            decrypted_text += chr((ord(char) - 65 - shift) % 26 + 65)
        # Check if the character is a lowercase letter
        elif char.islower():
            # Shift within the range of lowercase letters (a-z) in the reverse direction
            decrypted_text += chr((ord(char) - 97 - shift) % 26 + 97)
        # If the character is not a letter, leave it unchanged
        else:
            decrypted_text += char
    return decrypted_text

# Example usage
cipher_text = input("Enter the cipher text to decrypt: ")
shift_value = int(input("Enter the shift value: "))
print("Decrypted text:", caesar_cipher_decrypt(cipher_text, shift_value))
