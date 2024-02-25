from cryptography.fernet import Fernet
import json
import os

class PasswordManager:
    def __init__(self, key_file="key.key", data_file="data.json"):
        self.key_file = key_file
        self.data_file = data_file
        self.load_key()

    def load_key(self):
        if not os.path.exists(self.key_file):
            self.generate_key()

        with open(self.key_file, "rb") as key_file:
            self.key = key_file.read()

    def generate_key(self):
        self.key = Fernet.generate_key()
        with open(self.key_file, "wb") as key_file:
            key_file.write(self.key)

    def encrypt_password(self, password):
        cipher_suite = Fernet(self.key)
        return cipher_suite.encrypt(password.encode())

    def decrypt_password(self, encrypted_password):
        cipher_suite = Fernet(self.key)
        return cipher_suite.decrypt(encrypted_password).decode()

    def save_password(self, service, username, password):
        encrypted_password = self.encrypt_password(password)
        data = {}
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                data = json.load(file)
        data[service] = {"username": username, "password": encrypted_password.decode()}
        with open(self.data_file, "w") as file:
            json.dump(data, file)

    def get_password(self, service):
        with open(self.data_file, "r") as file:
            data = json.load(file)
            if service in data:
                username = data[service]["username"]
                encrypted_password = data[service]["password"]
                password = self.decrypt_password(encrypted_password.encode())
                return username, password
            else:
                return None, None

# Exemplo de utilização:
pm = PasswordManager()
pm.save_password("example_service", "example_user", "example_password")
username, password = pm.get_password("example_service")
if username and password:
    print(f"Username: {username}, Password: {password}")
else:
    print("Service not found or password not set.")
