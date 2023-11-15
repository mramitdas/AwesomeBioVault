from app.config.config import Config

from .base import Base


class User(Base):
    """
    Represents a class for managing user data.

    This class inherits from the `Base` class, which provides generic methods for interacting with a database table. The `User` class is specialized for managing user-related data and is configured to interact with a specific database table specified by the "USER_TABLE_NAME" environment variable.

    Attributes:
        None

    Methods:
        - __init__(): Initializes a `User` instance, inheriting the database connection and methods from the `Base` class.

    Note:
        - This class is designed for managing user data specifically and relies on the generic database operations provided by the `Base` class.
        - The database table name is configured through the "USER_TABLE_NAME" environment variable.
    """

    def __init__(self):
        """
        Initialize a User instance for managing user-related data.

        The database table name is determined by the "USER_TABLE_NAME" environment variable.

        Args:
            None
        """
        super().__init__(table_name=Config.TABLE_NAME)
