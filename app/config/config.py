import os

from dotenv import load_dotenv


class Config:
    """
    Configuration class for handling environment variables and settings.

    Attributes:
    - DB_URL (str): The URL for connecting to the database.
    - DB_NAME (str): The name of the database.
    - TABLE_NAME (str): The name of the table within the database.

    Note:
    This class uses the `python-dotenv` library to load environment variables
    from a .env file in the project root directory.

    Example:
    ```
    # .env file
    DB_URL=your_database_url
    DB_NAME=your_database_name
    TABLE_NAME=your_table_name
    ```

    Usage:
    ```
    # Import the Config class in your application
    from your_module import Config

    # Access configuration variables
    db_url = Config.DB_URL
    db_name = Config.DB_NAME
    table_name = Config.TABLE_NAME
    ```
    """

    load_dotenv()
    DB_URL = os.environ.get("DB_URL")
    DB_NAME = os.environ.get("DB_NAME")
    TABLE_NAME = os.environ.get("DB_NAME")
