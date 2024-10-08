from typing import Any
from cryptography.fernet import Fernet
import os
import logging

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
    user_input = input(prompt)
    if user_input.lower() == 'q':
        print("Bye")
        exit()
    elif user_input.lower() == 'b':
        return None
    return user_input
    
def main():

    password = {}
    pm = PasswordManager()

    print("""What do you want to do?
    (1) Create a new key
    (2) Use an existing key
    (3) Create a new password file
    (4) Load existing password file
    (5) Add a new password
    (6) Get a password
    (q) Quit          
    """)
    
    while True:
        choice = get_user_input("Enter your choice: ")

        if choice is None:
            continue

        match choice:
            case "1":
                path = input("Enter path: ")
                pm.create_key(path)
            case "2":
                print("""
    (1) Load key file
    (2) Manually enter key
                      """)
                choice_2 = input("Enter your choice: ")
                match choice_2:
                    case "1":
                        path = input("Enter path: ")
                        pm.load_key(path)
                    case "2":
                        key = input("Enter the key: ")
                        pm.manually_load_key(key)
            case "3":
                path = input("Enter path: ")
                pm.create_password_file(path)
            case "4":
                path = input("Enter path: ")
                pm.load_password_file(path)
            case "5":
                site = input("Enter the site: ")
                passworkd = input("Enter the password: ")
                pm.add_password(site, password)
            case "6":
                site = input("What site do you want: ")
                print(f"Password for {site} is {pm.get_password(site)}")
            case "q":
                done = True
                print("Bye")
            case _:
                print("Invalid choice!")

if __name__ == "__main__":
    main()

        
