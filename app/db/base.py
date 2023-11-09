from datetime import datetime

import pymongo
import pytz
from app.exceptions.custom_exceptions import MissingAttributeError


class DataBase:
    """
    A utility class for interacting with MongoDB databases.

    This class provides methods for connecting to a MongoDB instance, validating input data, and performing various database operations such as uploading, querying, updating, and deleting data.

    Args:
        db_url (str, optional): The connection URL for the MongoDB instance.

    Attributes:
        database_url (str): The URL of the connected MongoDB instance.
        mongod (pymongo.MongoClient): The MongoDB client instance established using the provided URL.

    Methods:
        - connect(): Establishes a connection to the MongoDB instance.
        - validate(): Validates input data and raises errors for missing or invalid attributes.
        - upload(): Inserts data into a specified database and collection.
        - query(): Retrieves data from a specified database and collection based on provided filters.
        - update(): Updates data in a specified database and collection based on provided filters.
        - delete(): Deletes data from a specified database and collection based on provided filters.

    Notes:
        - This class is designed for MongoDB database interactions.
        - You can connect to a MongoDB instance by providing the `db_url` parameter during initialization.
        - The provided methods handle data validation and various database operations.
    """

    def __init__(self, db_url=None):
        """Initialize the MongoDB client instance.

        Args:
            db_url (str): The database connection URL.

        Raises:
            MissingAttributeError: If `db_url` is not provided.
            TypeError: If `db_url` is not a string.
        """
        if not db_url:
            raise MissingAttributeError("db_url is required")
        elif not isinstance(db_url, str):
            raise TypeError(
                f"Expected a str for 'db_url' but received a {type(db_url).__name__}."
            )
        self.database_url = db_url
        self.mongod = self.connect()

    def connect(self):
        """Establish a connection to the MongoDB instance.

        Returns:
            pymongo.MongoClient: The MongoDB client instance.
        """
        return pymongo.MongoClient(self.database_url)

    def validate(
        self,
        db_name=None,
        table_name=None,
        data_opt=False,
        data=None,
        filter_opt=False,
        filter=None,
        bulk=False,
    ):
        """Validate input data and attributes.

        Acts as middleware for validating input data and attributes.

        Args:
            db_name (str): The name of the database.
            table_name (str): The name of the collection (table).
            data_opt (bool, optional): Indicates whether data validation is required.
            data (dict or list, optional): The data to be validated.
            filter_opt (bool, optional): Indicates whether filter validation is required.
            filter (dict, optional): The filter to be validated.
            bulk (bool, optional): Indicates whether bulk validation is required.

        Raises:
            MissingAttributeError: If any required attribute is missing.
            TypeError: If any attribute has an unexpected type.
        """
        if not db_name:
            raise MissingAttributeError("db_name is required")
        elif not isinstance(db_name, str):
            raise TypeError(
                f"Expected a str for 'db_name' but received a {type(db_name).__name__}."
            )

        if not table_name:
            raise MissingAttributeError("table_name is required")
        elif not isinstance(table_name, str):
            raise TypeError(
                f"Expected a str for 'table_name' but received a {type(table_name).__name__}."
            )

        if data_opt:
            if not data:
                raise MissingAttributeError("data is required")
            elif not (isinstance(data, dict) or isinstance(data, list)):
                raise TypeError(
                    f"Expected a dict/list for 'data' but received a {type(data).__name__}."
                )

        if filter_opt:
            if not filter:
                raise MissingAttributeError("filter is required")
            elif not isinstance(filter, dict):
                raise TypeError(
                    f"Expected a dict for 'filter' but received a {type(filter).__name__}."
                )

        if bulk and not isinstance(bulk, bool):
            raise TypeError(
                f"Expected a bool for 'bulk' but received a {type(bulk).__name__}."
            )

    def upload(self, db_name=None, table_name=None, data=None):
        """Insert data into a specified database and collection.

        Args:
            db_name (str): The name of the database.
            table_name (str): The name of the collection (table).
            data (dict or list): The data to be inserted.
                - If dict, used for single insertion.
                - If list, used for bulk insertion.

        Returns:
            pymongo.InsertOneResult or pymongo.InsertManyResult: The response object indicating the result of the insertion.
        """
        self.validate(db_name, table_name, data_opt=True, data=data)

        database = self.mongod[db_name]
        dataset = database[table_name]

        if data["user_uuid"] is None:
            user_id = (
                dataset.find()
                .sort("user_uuid", pymongo.DESCENDING)
                .limit(1)[0]["user_uuid"]
            )
            data.update({"user_uuid": user_id + 1})
            response = dataset.insert_one(data)

        if isinstance(data, dict):
            response = dataset.insert_one(data)
        else:
            response = dataset.insert_many(data)

        return response

    def query(self, db_name=None, table_name=None, filter=None, bulk=False):
        """Retrieve data from a specified database and collection based on filters.

        Args:
            db_name (str): The name of the database.
            table_name (str): The name of the collection (table).
            filter (dict): The filter to be applied to the search query.
            bulk (bool): If True, multiple results will be returned.

        Returns:
            pymongo.cursor.Cursor or dict: The retrieved data.
        """
        self.validate(
            db_name,
            table_name,
            filter_opt=True if filter else False,
            filter=filter,
            bulk=bulk,
        )

        database = self.mongod[db_name]
        dataset = database[table_name]

        if bulk:
            if filter:
                response = dataset.find(filter)
            else:
                response = dataset.find()
        elif filter:
            response = dataset.find_one(filter)
        else:
            response = dataset.find_one()

        return response

    def update(self, db_name=None, table_name=None, data=None, bulk=False):
        """Update data in a specified database and collection based on filters.

        Args:
            db_name (str): The name of the database.
            table_name (str): The name of the collection (table).
            data (dict): The data to be updated.
            bulk (bool): If True, multiple results will be updated.

        Returns:
            pymongo.UpdateResult: The response object indicating the result of the update operation.
        """
        self.validate(db_name, table_name, data_opt=True, data=data, bulk=bulk)

        database = self.mongod[db_name]
        dataset = database[table_name]

        data.get("user_data")["updated_at"] = datetime.now(
            pytz.timezone("Asia/Kolkata")
        ).strftime("%Y-%m-%d || %H:%M:%S:%f")
        update = {"$set": data["user_data"]}

        if bulk:
            response = dataset.update_many({"user_uuid": data["user_uuid"]}, update)
        else:
            response = dataset.update_one({"user_uuid": data["user_uuid"]}, update)

        return response

    def delete(self, db_name=None, table_name=None, filter=None):
        """
        Delete data from a specified database collection based on a filter.

        Args:
            db_name (str): The name of the database.
            table_name (str): The name of the collection (table) from which data will be deleted.
            filter (dict): The filter to be applied to specify which data to delete.

        Returns:
            pymongo.DeleteResult: The response object indicating the result of the delete operation.
        Raises:
            MissingAttributeError: If any required attribute is missing.
            TypeError: If any attribute has an unexpected type.
        """
        self.validate(db_name, table_name, filter_opt=True, filter=filter)

        database = self.mongod[db_name]
        dataset = database[table_name]
        response = dataset.delete_one(filter)

        return response
