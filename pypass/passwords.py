"Defines class model for passwords and defines how they are to be saved."

import json


class PasswordSet:
    "A set of passwords for accounts of a particular service (Amazon, Google, etc.)"

    def __init__(self, service_name: str, account_info: dict = None):

        # The name of the service.
        self.service_name = service_name

        # A dictionary of the usernames and passwords for the service.
        self.account_info = account_info


    @classmethod
    def from_json(cls, jsonstr: str):
        "Builds a PasswordSet from the provided JSON"

        data = json.loads(jsonstr)

        return cls(service_name=data["service_name"], account_info=data["account_info"])









def test_module():
    "Test function for passwords.py, run when this file is executed directly."

    print("Testing passwords.py module...")



if __name__ == "__main__":
    test_module()
