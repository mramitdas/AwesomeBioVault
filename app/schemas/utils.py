from datetime import datetime

import secrets
import pytz
from pydantic import BaseModel


class TimestampMixin(BaseModel):
    """
    A Pydantic mixin class to provide timestamp fields for created and updated times.

    This mixin class extends Pydantic's `BaseModel` to include timestamp fields for both 'created_at' and 'updated_at' times. The timestamps are automatically generated in the 'Asia/Kolkata' timezone when an instance of a model that inherits from this mixin is created.

    Attributes:
        created_at (datetime): The timestamp indicating the creation time of the object.
        updated_at (datetime): The timestamp indicating the last update time of the object.

    Note:
        - The timestamps are generated in the 'Asia/Kolkata' timezone.
        - The format for the timestamps is '%Y-%m-%d || %H:%M:%S:%f'.
    """

    created_at: str = datetime.now(pytz.timezone("Asia/Kolkata")).strftime(
        "%Y-%m-%d || %H:%M:%S:%f"
    )
    updated_at: str = datetime.now(pytz.timezone("Asia/Kolkata")).strftime(
        "%Y-%m-%d || %H:%M:%S:%f"
    )


def generate_password() -> str:
    """
    Generate a random password using secrets.token_urlsafe.

    Returns:
        str: A randomly generated password.

    The password is generated with 12 characters using secrets.token_urlsafe,
    making it suitable for secure password generation.
    """
    return secrets.token_urlsafe(12)
