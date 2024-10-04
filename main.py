from typing import Any
from cryptography.fernet import Fernet

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
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)  # Corrected create_key to key

    def load_key(self, path: str) -> None:
        """
        Loads an existing encryption key.

        Args:
        ----
        path (str): The file path where the key is stored.
        """
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path: str, initial_values: dict = None) -> None:
        """
        Creates a new password file.

        Args:
        ----
        path (str): The file path where passwords will be stored.
        initial_values (dict, optional): Initial site-password pairs. Defaults to None.
        """
        self.password_file = path

        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

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

    def add_password(self, site: str, password: str) -> None:
        """
        Adds a new password.

        Args:
        ----
        site (str): The site associated with the password.
        password (str): The password to be stored.
        """
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

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
    
def main():

    password = {}
    pm = PasswordManager()

    print("""What do you want to do?
    (1) Create a new key
    (2) Load an existing key
    (3) Create a new password file
    (4) Load existing password file
    (5) Add a new password
    (6) Get a password
    (q) Quit          
    """)

    done = False

    while not done:
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                path = input("Enter path: ")
                pm.create_key(path)
            case "2":
                path = input("Enter path: ")
                pm.load_key(path)
            case "3":
                path = input("Enter path: ")
                pm.create_password_file(path, password)
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

        
