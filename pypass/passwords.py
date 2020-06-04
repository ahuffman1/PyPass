"Defines class model for passwords and defines how they are to be saved."

import json

class PasswordSet:
    "A set of passwords for accounts of a particular service (Amazon, Google, etc.)"

    def __init__(self, service_name: str, account_info: dict = dict()):
        self.service_name = service_name # The name of the service.
        self.account_info = account_info # A dictionary of the usernames and passwords for the service.

    #region JSON
    @classmethod
    def from_json(cls, jsonstr: str):
        "Builds a PasswordSet from the provided JSON"

        data = json.loads(jsonstr)

        return cls( service_name=data["service_name"], account_info=data["account_info"] )

    def to_json(self) -> str:
        "Builds a JSON string from the current PasswordSet instance."

        return json.dumps(self, default=lambda o: o.__dict__)


    #endregion







def test_module():
    print("Testing passwords.py module...")
    passwords = dict()

    passwords["hello"] = "123"
    passwords["goodbye"] = "456"

    set = PasswordSet( service_name="amazon", account_info=passwords )

    print( set.to_json() )
    set2 = PasswordSet.from_json( jsonstr=set.to_json() )
    print( set2.to_json() )



if __name__ == "__main__":
    test_module()