"The main running file for PyPass."

from typing import List
from os import path
from pypass.heplers import to_json
from pypass.passwords import PasswordSet, sets_from_json
from enum import Enum


PWDS_FILE = "data.pwd"

class UIExitCode(Enum):
    "The Exit Code given by the UI to determine how to terminate the program."

    EXIT_SAVING = 0
    EXIT_NOSAVE = 1
    CRASH = 2



def ui_crash_catch(f):
    "Decorator to catch a crash in the UI and return the right value."

    def wrap(*args):
        try:
            return f(*args)
        except:
            return UIExitCode.CRASH

    return wrap



@ui_crash_catch
def console_ui(passwords: List[PasswordSet]) -> UIExitCode:
    "The main console UI for the application."

    print("PyPass. By Andrew Huffman.")
    print()

    while True:
        for pwdset in passwords:
            print(pwdset.service_name)
            for key, value in pwdset.account_info.items(): # For some reason this method in't working to iterate over a dictionary....
                print("\t{0}\t{1}".format(key, value))

        print()
        print("1\t...\tAdd a new password.")
        print("2\t...\tRemove a password.")
        print("3\t...\tExit the program.")
        print("4\t...\tExit the program without saving.")
        print()

        response = input("Enter an option >> ")

        if response.startswith("1"):
            print()
            service = input("Enter the name of the service >> ")
            username = input("Enter your username >> ")
            password = input("Enter your password >> ")
            print()
            decision = input("Is this okay? {0} {1} {2} (y/n) >> ".format(service, username, password))


            if decision.startswith("y"):
                found_service = False
                for element in passwords:
                    if element.service_name == service:
                        found_service = True

                        element.account_info[username] = password
                        break

                if not found_service:
                    passwords.append(PasswordSet(service, {username:password}))
        elif response.startswith("2"):
            print()
            service = input("Enter the name of the service >> ")
            service_index = -1
            for i in range(0, len(passwords)):
                if passwords[i].service_name == service:
                    service_index = i
                    break

            if service_index == -1:
                print("Service not found!")
            else:
                username = input("Enter the username associated with the account >> ")
                found_username = False
                for key, value in passwords[service_index].account_info.items():
                    if key == username:
                        found_username = True
                        break

                if not found_username:
                    print("Username not found!")
                else:
                    decision = input("Are you sure? (y/n) >> ")

                    if decision.startswith("y"):
                        del passwords[service_index].account_info[username]

                        if len(passwords[service_index].account_info) == 0:
                            del passwords[service_index]

        elif response.startswith("3"):
            print()

            decision = input("Save and exit? (y/n) >> ").lower()

            if decision.startswith("y"):
                print("Goodbye!")
                return UIExitCode.EXIT_SAVING
        elif response.startswith("4"):
            print()

            decision =  input("Exit without saving? (y/n) >> ").lower()

            if decision.startswith("y"):
                print("Goodbye!")
                return UIExitCode.EXIT_NOSAVE





def main():
    "The top-level executing function for PyPass."

    # The loaded passwords.
    passwords: List[PasswordSet] = None

    # Load password data from local file.
    if path.exists(PWDS_FILE):
        with open(PWDS_FILE, mode="r") as file:
            passwords = sets_from_json(file.read())
    else:
        passwords = list()


    # Pass loaded data to the UI.
    exit_code = console_ui(passwords)


    # Save the no-doubt changed data (if we are exiting and saving.)
    if exit_code == UIExitCode.EXIT_SAVING:
        with open(PWDS_FILE, mode="w") as file:
            file.write(to_json(passwords))
    elif exit_code == UIExitCode.CRASH:
        print("Oops! Something went wrong!")



if __name__ == "__main__":
    main()
