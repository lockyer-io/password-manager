##Introduction

The Password Manager is a Python application that helps manage your passwords securely using encryption. It provides functionalities to create or load encryption keys, create or load password files, and securely store and retrieve passwords for various websites. The application also has a GUI version built using the customtkinter library for a modern and intuitive interface.

Features
	•	Generate and load encryption keys: You can either create a new key or load an existing key.
	•	Create and load password files: Create a new password file to securely store site-password pairs or load an existing file.
	•	Add and retrieve passwords: Securely add new passwords for websites or retrieve existing passwords.
	•	GUI and CLI interface: The application provides both a Command-Line Interface (CLI) and Graphical User Interface (GUI) for password management.

Requirements
	•	Python 3.x
	•	cryptography package
	•	customtkinter package (for GUI version)

You can install the required dependencies using pip:

```bash
pip install cryptography customtkinter
```

##Getting Started

Command-Line Interface (CLI)

To use the Password Manager via the CLI:
	1.	Create or load encryption key: Choose whether to create a new key or load an existing one. You can also manually input a key.
	2.	Create or load password file: Choose to create a new password file or load an existing one.
	3.	Add or retrieve passwords: You can add a new password for a site or retrieve an existing password.

Graphical User Interface (GUI)

To run the GUI version, simply execute the program as follows:

```bash
python password_manager_gui.py
```
The GUI will allow you to interact with the Password Manager using buttons and dialogs, making the process more intuitive.

##Usage

CLI Example
```bash
$ python password_manager.py
Create or load encryption key:
(1) Create a new key
(2) Use an existing key
(b) Back
(q) Quit
Enter your choice: 1

(1) Generate random key
(2) Manually type key
(b) Back
(q) Quit
Enter your choice: 1
Enter path of desired key save location: ./key.key
Encryption key saved to ./key.key

Create or load password file:
(1) Create a new password file
(2) Load existing password file
(b) Back
(q) Quit
Enter your choice: 1
Enter path to create password file: ./passwords.pass
Password file created

Manage passwords:
(1) Add a new password
(2) Get a password
(b) Back
(q) Quit
Enter your choice: 1
Enter the site: example.com
Enter the password: securepassword
Password added

(1) Add a new password
(2) Get a password
(b) Back
(q) Quit
Enter your choice: 2
What site do you want: example.com
Password for example.com is securepassword
```

GUI Example
	1.	Click “Create/Load Key” to generate or load an encryption key.
	2.	Click “Create/Load Password File” to create or load your password file.
	3.	Use the buttons in the password management section to add new passwords or retrieve existing ones.

##Methods

PasswordManager Class
	•	create_key(path: str): Generates and saves a new encryption key at the specified file path.
	•	load_key(path: str): Loads an existing encryption key from the specified file path.
	•	manually_load_key(key: str): Manually sets an encryption key.
	•	create_password_file(path: str): Creates a new password file at the specified path.
	•	load_password_file(path: str): Loads an existing password file.
	•	add_password(site: str, password: str): Adds a new site-password pair to the password file.
	•	get_password(site: str): Retrieves a password for the given site.

PasswordManagerApp Class (CLI Interface)
	•	run(): Runs the CLI application allowing the user to interact with the password manager.
	•	go_back(): Allows the user to go back to the previous state in the CLI.

PasswordManagerGUI Class (GUI Interface)
	•	Provides an interactive GUI interface using customtkinter to manage passwords.

##Error Handling
	•	Permission Errors: If there are permission issues when saving the key or password file, an appropriate error message will be shown.
	•	File I/O Errors: Errors related to loading or saving files will be handled and logged.
	•	Invalid Inputs: Invalid choices will be caught and prompt the user to enter a valid choice.

##Conclusion

This Password Manager helps you securely manage your passwords by providing encryption and offering both CLI and GUI interfaces for ease of use. Whether you prefer a text-based interface or a modern graphical interface, this tool provides a comprehensive solution for password management.

