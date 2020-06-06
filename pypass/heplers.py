"Helper methods used within PyPass."

import json
from typing import Any

def to_json(obj: Any) -> str:
    "Converts any object into a JSON string based upon its members."

    return json.dumps(obj, default=lambda o: o.__dict__)
