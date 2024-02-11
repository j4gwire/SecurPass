#!/usr/bin/python3

import time
import secrets
import string
import logging
import argparse
import sys
import pyperclip

WELCOME_COLOR = '\033[1;35m'
RED_COLOR = '\033[1;31m'
SUCCESS_COLOR = '\033[1;32m'
GOLD_COLOR = '\033[1;33m'
ERROR_COLOR = '\033[1;31m'
INFO_COLOR = '\033[1;36m'
WHITE_COLOR = '\033[1;37m'
RESET_COLOR = '\033[0m'

DEFAULT_SLEEP_DURATION = 3
DEFAULT_PASSWORD_LENGTH = 12
LOG_FILE = 'securpass.log'

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
password_history = []

def generate_password(pw_length=DEFAULT_PASSWORD_LENGTH, use_special_chars=True):
    try:
        if not isinstance(pw_length, int) or pw_length <= 0:
            raise ValueError("Password length must be a positive integer.")

        alphabet = string.ascii_letters + string.digits
        if use_special_chars:
            alphabet += string.punctuation

        pwd = ''
        pw_strong = False

        print(f"{INFO_COLOR}Generating password...{RESET_COLOR}")
        while not pw_strong:
            pwd = ''.join(secrets.choice(alphabet) for _ in range(pw_length))

            if any(char in string.punctuation for char in pwd) and sum(char in string.digits for char in pwd) >= 2:
                pw_strong = True

        password_history.append(pwd)
        time.sleep(3)  # Introduce a 3-second delay after password generation
        return pwd

    except ValueError as ve:
        logging.error(f"Error in generate_password: {ve}")
        print(f"{ERROR_COLOR}Error generating password. Please try again.{RESET_COLOR}")
        sys.exit(1)

def print_welcome_message():
    print(f"{WELCOME_COLOR}Welcome to SecurPass, the Python Password Generator!{RESET_COLOR}")

def print_exit_message():
    print(f"{INFO_COLOR}Exiting...{RESET_COLOR}")
    logging.info("Program exited.")

def print_invalid_option_message():
    print(f"{ERROR_COLOR}Invalid option. Please try again.{RESET_COLOR}")

def print_password_history():
    if not password_history:
        print(f"{INFO_COLOR}Password history is empty.{RESET_COLOR}")
    else:
        print(f"{INFO_COLOR}Password History:{RESET_COLOR}")
        for i, password in enumerate(password_history, start=1):
            print(f"{i}. {password}")

def select_option():
    while True:
        print(f"{RED_COLOR}Select an option:\n1. Generate password\n2. Check password history\n3. Exit{RESET_COLOR}")
        option = input("Select an option (1/2/3): ")

        if option == '1':
            password_length = input("Enter password length (default is 12): ")
            try:
                password_length = int(password_length) if password_length else DEFAULT_PASSWORD_LENGTH
            except ValueError:
                print(f"{ERROR_COLOR}Invalid input for password length. Using default.{RESET_COLOR}")
                password_length = DEFAULT_PASSWORD_LENGTH

            use_special_chars = input("Include special characters? (y/n): ").lower() == 'y'
            password = generate_password(password_length, use_special_chars)
            print(f"{SUCCESS_COLOR}New password generated: {password}{RESET_COLOR}")

            handle_password(password)

            generate_another = input("Do you want to generate another password? (y/n): ").lower()
            if generate_another != 'y':
                print_exit_message()
                break

        elif option == '2':
            print_password_history()

        elif option == '3':
            print_exit_message()
            break

        else:
            print_invalid_option_message()

def handle_password(password):
    try:
        pyperclip.copy(password)
        print(f"{GOLD_COLOR}Password copied to clipboard.{RESET_COLOR}")

        with open("generated_password.txt", "w") as file:
            file.write(password)
        print(f"{WHITE_COLOR}Password saved to 'generated_password.txt'.{RESET_COLOR}")

    except Exception as e:
        logging.error(f"Error in handle_password: {e}")
        print(f"{ERROR_COLOR}Error handling password securely. Please ensure clipboard and file access permissions.{RESET_COLOR}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SecurPass - Python Password Generator')
    parser.add_argument('--sleep', type=int, default=DEFAULT_SLEEP_DURATION, help='Sleep duration before starting')
    args = parser.parse_args()

    sleep_duration = args.sleep
    print_welcome_message()
    time.sleep(sleep_duration)

    select_option()
