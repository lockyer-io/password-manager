from typing import Any
from cryptography.fernet import Fernet
import os
import logging
import customtkinter as ctk

class PasswordManager:
    """
    A class used to manage passwords securely.

    Attributes:
    ----------
    key : bytes
        The encryption key used for password encryption and decryption.
    password_file : str
        The file path where passwords are stored.
    password_dict : dict
        A dictionary storing site-password pairs.


    Methods:
    -------
    create_key(path)
        Generates and saves an encryption key.
    load_key(path)
        Loads an existing encryption key.
    create_password_file(path, initial_values)
        Creates a new password file.
    load_password_file(path)
        Loads existing passwords from a file.
    add_password(site, password)
        Adds a new password.
    get_password(site)
        Retrieves a password.
    """

    def __init__(self):
        """
        Initializes a PasswordManager object.
        """
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path: str) -> None:
        """
        Generates and saves an encryption key.

        Args:
        ----
        path (str): The file path where the key will be saved.
        """
        if not path:
            path = os.path.join(os.getcwd(), 'default_key.key')
            logging.info(f"Using default key path: {path}")
        try:
            # Generate key
            self.key = Fernet.generate_key()
            
            # Ensure directory exists
            directory = os.path.dirname(path)
            os.makedirs(directory, exist_ok=True)
            
            # Save key to file
            with open(path, 'wb') as f:
                f.write(self.key)
            
            logging.info(f"Encryption key saved to {path}")
        
        except PermissionError:
            logging.error(f"Permission denied: Unable to save key to {path}")
        
        except OSError as e:
            logging.error(f"Error saving key to {path}: {e}")
        
        except Exception as e:
            logging.error(f"Unexpected error generating/saving key: {e}")

    def load_key(self, path: str) -> None:
        """
        Loads an existing encryption key.

        Args:
        ----
        path (str): The file path where the key is stored.
        """
        if path is None:
            print("\n!! Path cannot be empty !!\n")
            return
        with open(path, 'rb') as f:
            self.key = f.read()
        print("-- Key loaded successfully --")

    def manually_load_key(self, key: str) -> None:
        """
        Lets user manually input their encryption key.

        Args:
        ----
        key (str): The users encryption key.
        """
        self.key = key
        print("-- Key input successfully --")

    def create_password_file(self, path: str) -> None:
        """
        Creates a new password file.

        Args:
        ----
        path (str): The file path where passwords will be stored.
        initial_values (dict, optional): Initial site-password pairs. Defaults to None.
        """
        if path:
            self.password_file = path
        else:
            path = os.path.join(os.getcwd(), 'passwords.pass')
            self.password_file = path
        with open(path, "w") as f:
            pass
        print("-- Password file created --")
            
    def load_password_file(self, path: str) -> None:
        """
        Loads existing passwords from a file.

        Args:
        ----
        path (str): The file path where passwords are stored.
        """
        self.password_file = path
        
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
        print("-- Password file loaded --")

    def add_password(self, site: str, password: str) -> None:
        """
        Adds a new password.

        Args:
        ----
        site (str): The site associated with the password.
        password (str): The password to be stored.
        """

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")
        self.password_dict[site] = password
        print("-- Password added --")

    def get_password(self, site: str) -> str:
        """
        Retrieves a password.

        Args:
        ----
        site (str): The site associated with the password.

        Returns:
        -------
        str: The password associated with the site.
        """
        return self.password_dict[site]

def get_user_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'q':
            print("Bye")
            exit()
        elif user_input == "":
            return None
        else:
            return user_input

class PasswordManagerApp:
    def __init__(self):
        self.pm = PasswordManager()
        self.states = {
            "key": self.create_or_load_key,
            "password_file": self.create_or_load_password_file,
            "password_management": self.manage_passwords
        }
        self.current_state = "key"

    def run(self):
        while True:
            self.states[self.current_state]()
    
    def go_back(self):
        if self.current_state == "password_management":
            self.current_state = "password_file"
        elif self.current_state == "password_file":
            self.current_state = "key"

    def create_or_load_key(self):
        # Step 1: Create or load key
        while True:
            print("""Create or load encryption key:
                  
            (1) Create a new key
            (2) Use an existing key
            (b) Back
            (q) Quit
                        """)
            choice = get_user_input("Enter your choice: ")

            if choice is None:
                continue
            match choice:
                case "b":
                    self.go_back()
                    continue
                case "1":
                    print("""
            (1) Generate random key
            (2) Manually type key
            (b) Back
            (q) Quit
                        """)
                    choice_2 = get_user_input("Enter your choice: ")
                    match choice_2:
                        case "1":
                            path = get_user_input("Enter path of desired key save location: ")
                            self.pm.create_key(path)
                            break
                        case "2":
                            key = get_user_input("Type the desired key: ")
                            self.pm.key = key
                            break
                case "2":
                    print("""
            (1) Load key file
            (2) Manually enter key
            (b) Back
            (q) Quit
                        """)
                    choice_2 = get_user_input("Enter your choice: ")
                    match choice_2:
                        case "1":
                            path = get_user_input("Enter path to key file: ")
                            self.pm.load_key(path)
                            break
                        case "2":
                            key = get_user_input("Enter the key: ")
                            self.pm.manually_load_key(key)
                            break
                case _:
                    print("Invalid choice!")
        self.current_state = "password_file"

    def create_or_load_password_file(self):
        # Step 2: Create or load password file
        while True:
            print("""Create or load password file:
                  
            (1) Create a new password file
            (2) Load existing password file
            (b) Back
            (q) Quit
            """)
            choice = get_user_input("Enter your choice: ")

            if choice is None:
                continue
            match choice:
                case "b":
                    self.go_back()
                    break
                case "1":
                    path = get_user_input("Enter path to create password file: ")
                    self.pm.create_password_file(path)
                    break
                case "2":
                    path = get_user_input("Enter path to load password file: ")
                    self.pm.load_password_file(path)
                    break
                case _:
                    print("Invalid choice!")
            self.current_state = "password_management"

    def manage_passwords(self):
        # Step 3: Add or get password
        while True:
            print("""Manage passwords:
                  
            (1) Add a new password
            (2) Get a password
            (b) Back
            (q) Quit
            """)
            choice = get_user_input("Enter your choice: ")

            if choice is None:
                continue
            match choice:
                case "b":
                    self.go_back()
                    break
                case "1":
                    site = get_user_input("Enter the site: ")
                    password = get_user_input("Enter the password: ")
                    self.pm.add_password(site, password)
                case "2":
                    site = get_user_input("What site do you want: ")
                    print(f"Password for {site} is {self.pm.get_password(site)}")
                case _:
                    print("Invalid choice!")

class PasswordManagerGUI:
    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.pm = PasswordManager()
        self.root = ctk.CTk()
        self.root.title("Password Manager")
        self.root.geometry("500x500")

        # Create widgets
        self.title_label = ctk.CTkLabel(self.root, text="Password Manager", font=("Arial", 24))
        self.key_button = ctk.CTkButton(self.root, text="Create/Load Key", command=self.create_load_key)
        self.password_file_button = ctk.CTkButton(self.root, text="Create/Load Password File", command=self.create_load_password_file)

def main():
    gui = PasswordManagerGUI()
    gui.run()

if __name__ == "__main__":
    main()
