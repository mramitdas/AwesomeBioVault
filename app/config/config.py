import os

from dotenv import load_dotenv


class Config:
    """
    Configuration class for handling environment variables and settings.

    This class encapsulates configuration variables used in the application.
    It uses the `python-dotenv` library to load environment variables from a .env
    file in the project root directory.

    Attributes:
        - DB_URL (str): The URL for connecting to the database.
        - DB_NAME (str): The name of the database.
        - TABLE_NAME (str): The name of the table within the database.
        - REDIS_SERVER (str): The URL or IP address of the Redis server.
        - GITHUB_TOKEN (str): GitHub personal access token with the necessary permissions.
        - REPO_OWNER (str): Owner of the GitHub repository.
        - REPO_NAME (str): Name of the GitHub repository.
        - BRANCH (str): Default branch for GitHub operations.

    Note:
        Ensure that you have a .env file in the project root directory with the
        required environment variables.

    """

    load_dotenv()
    DB_URL = os.environ.get("DB_URL")
    DB_NAME = os.environ.get("DB_NAME")
    TABLE_NAME = os.environ.get("PROFILE_TABLE_NAME")
    REDIS_SERVER = os.environ.get("REDIS_SERVER")

    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
    REPO_OWNER = os.environ.get("REPO_OWNER")
    REPO_NAME = os.environ.get("REPO_NAME")
    BRANCH = os.environ.get("BRANCH")
