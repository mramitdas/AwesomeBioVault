from app.config.config import Config
from app.db.base import DataBase
from typing import Union


class Base:
    """
    Represents a base class for generic data management.

    This class provides methods for interacting with a generic database table. It loads database configuration from environment variables and utilizes the `DataBase` class for performing common database operations such as saving, retrieving, filtering, updating, and deleting data.

    Attributes:
        - __db_url (str): The database connection URL obtained from the environment variables.
        - __db_name (str): The name of the database obtained from the environment variables.
        - __table_name (str): The name of the data table obtained from the environment variables.
        - __db (DataBase): An instance of the `DataBase` class for handling database operations.

    Methods:
        - save(data: dict) -> str: Inserts data into the database table.
        - get(data_id: int) -> dict: Retrieves data by data ID from the database table.
        - get_all() -> list[dict]: Retrieves all data from the database table.
        - filter(filter: dict) -> list[dict]: Retrieves data based on filter criteria from the database table.
        - update(data: dict) -> str: Updates data in the database table.
        - delete(data_id: int) -> str: Deletes data based on data ID from the database table.

    Note:
        - The class initializes database-related attributes from environment variables loaded via `load_dotenv()`.
        - It relies on the `DataBase` class for executing database operations.
    """

    def __init__(self, table_name: str):
        """
        Initialize a Base instance with the specified table name.

        Args:
            table_name (str): The name of the database table.
        """

        self.__db_url = Config.DB_URL
        self.__db_name = Config.DB_NAME
        self.__table_name = table_name
        self.__db = DataBase(db_url=self.__db_url)

    def save(self, data: dict) -> str:
        """
        Inserts data into the database table.

        Args:
            data (dict): The data to be saved.

        Returns:
            str: The response code from the database operation.
        """
        return self.__db.upload(
            db_name=self.__db_name, table_name=self.__table_name, data=data
        )

    def get(self, username: int) -> dict:
        """
        Retrieves data by data ID from the database table.

        Args:
            github_username (str): The github_username for identifying the user.

        Returns:
            dict: The data retrieved from the database.
        """
        return self.__db.query(
            db_name=self.__db_name,
            table_name=self.__table_name,
            filter={"github_username": username},
        )

    def get_all(self) -> list[dict]:
        """
        Retrieves all data from the database table.

        Returns:
            list[dict]: A list of all data retrieved from the database.
        """
        return list(
            self.__db.query(
                db_name=self.__db_name, table_name=self.__table_name, bulk=True
            )
        )

    def filter(self, filter: Union[dict, str]) -> list[dict]:
        """
        Retrieves data based on filter criteria from the database table.

        Args:
            filter (dict): The filter criteria for querying data.

        Returns:
            list[dict]: A list of data that matches the filter criteria.
        """
        if type(filter) == str:           
            if filter == "latest":
                aggregate_pipeline = [{"$sort": {"created_at": -1}}]
            elif filter == "trending":
                aggregate_pipeline = [{"$sort": {"profile_views": -1}}]
            elif filter == "popular":
                aggregate_pipeline = [{"$sort": {"profile_likes": -1}}]
            elif filter == "hot":
                aggregate_pipeline = [
                    {
                        "$addFields": {
                            "combined_score": {
                                "$sqrt": {
                                    "$multiply": ["$profile_likes", "$profile_views"]
                                }
                            }
                        }
                    },
                    {
                        "$sort": {
                            "combined_score": -1  # Sort in descending order (greater to smaller scores)
                        }
                    },
                ]
            elif filter == "creative":
                aggregate_pipeline = [{"$sort": {"profile_likes": -1}}]
            
            aggregate_pipeline.append(
                {"$project": {"_id": 0, "email": 0, "password": 0}},
            )

            return list(
                self.__db.query(
                    db_name=self.__db_name,
                    table_name=self.__table_name,
                    pipeline=aggregate_pipeline,
                )
            )

        return list(
            self.__db.query(
                db_name=self.__db_name,
                table_name=self.__table_name,
                filter=filter,
                bulk=True,
            )
        )

    def update(self, data: dict) -> str:
        """
        Updates data in the database table.

        Args:
            data (dict): The data to be updated.

        Returns:
            str: The response code from the database operation.
        """
        return self.__db.update(
            db_name=self.__db_name, table_name=self.__table_name, data=data
        )

    def delete(self, uuid: int) -> str:
        """
        Deletes data based on data ID from the database table.

        Args:
            uuid (int): The UUID for identifying the data to be deleted.

        Returns:
            str: The response code from the database operation.
        """
        return self.__db.delete(
            db_name=self.__db_name,
            table_name=self.__table_name,
            filter={"user_uuid": uuid},
        )
