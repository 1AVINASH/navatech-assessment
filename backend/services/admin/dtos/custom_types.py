import re

from pydantic import constr

class UserPassword(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, field=None):
        if not isinstance(value, str):
            raise TypeError("Password must be a string")

        # Rule 1: No special characters (only alphanumeric allowed)
        if not re.fullmatch(r'^[a-zA-Z0-9]+$', value):
            raise ValueError("Password must only contain alphanumeric characters (letters and numbers).")

        # Rule 2: Contains at least one uppercase letter
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter.")

        # Rule 3: Contains at least one lowercase letter
        if not re.search(r'[a-z]', value):
            raise ValueError("Password must contain at least one lowercase letter.")

        # Rule 4: Contains at least one number
        if not re.search(r'[0-9]', value):
            raise ValueError("Password must contain at least one number.")

        # Optional: Add a minimum length check (e.g., 8 characters)
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        return value
