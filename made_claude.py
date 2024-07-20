import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

# Constants
FILE_NAME = "hello.txt"
ENCRYPTED_FILE_NAME = FILE_NAME + ".enc"
SALT_FILE_NAME = FILE_NAME + ".salt"

def generate_key_from_passphrase(passphrase, salt=None):
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    return key, salt

def secure_delete(file_path):
    """Securely delete a file by overwriting it with random data before deletion."""
    if not os.path.exists(file_path):
        return

    # Get the file size
    file_size = os.path.getsize(file_path)
    
    # Overwrite the file with random data
    with open(file_path, "wb") as f:
        f.write(os.urandom(file_size))
    
    # Delete the file
    os.remove(file_path)

def encrypt_file(passphrase):
    try:
        # Generate a key from the passphrase
        key, salt = generate_key_from_passphrase(passphrase)
        
        # Create a Fernet instance
        fernet = Fernet(key)
        
        # Read the file content
        with open(FILE_NAME, 'rb') as file:
            file_data = file.read()
        
        # Encrypt the data
        encrypted_data = fernet.encrypt(file_data)
        
        # Write the encrypted data
        
        with open(ENCRYPTED_FILE_NAME, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
        
        # Store the salt
        with open(SALT_FILE_NAME, 'wb') as salt_file:
            salt_file.write(salt)
        
        # Securely delete the original file
        secure_delete(FILE_NAME)
        
        print(f"File '{FILE_NAME}' encrypted successfully and original securely deleted.")
    except FileNotFoundError:
        print(f"Error: The file '{FILE_NAME}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to access '{FILE_NAME}'.")
    except Exception as e:
        print(f"This is not the correct passkey: {str(e)}")

def decrypt_file(passphrase):
    try:
        # Read the salt
        with open(SALT_FILE_NAME, 'rb') as salt_file:
            salt = salt_file.read()
        
        # Generate the key from the passphrase and salt
        key, _ = generate_key_from_passphrase(passphrase, salt)
        
        # Create a Fernet instance
        fernet = Fernet(key)
        
        # Read the encrypted data
        with open(ENCRYPTED_FILE_NAME, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
        
        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Write the decrypted data back to the original file
        with open(FILE_NAME, 'wb') as file:
            file.write(decrypted_data)
        
        # Securely delete the encrypted file and salt file
        secure_delete(ENCRYPTED_FILE_NAME)
        secure_delete(SALT_FILE_NAME)
        
        print(f"File '{FILE_NAME}' decrypted successfully and encrypted version securely deleted.")
    except FileNotFoundError:
        print(f"Error: The encrypted file or salt file was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to access the files.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    while True:
        action = input("Enter 'e' to encrypt, 'd' to decrypt, or 'q' to quit: ").lower()
        
        if action == 'q':
            break
        elif action in ['e', 'd']:
            passphrase = input("Enter the passphrase: ")
            
            if action == 'e':
                encrypt_file(passphrase)
            else:
                decrypt_file(passphrase)
        else:
            print("Invalid action. Please try again.")

if __name__ == "__main__":
    main()