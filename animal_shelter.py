"""CRUD module for the Grazioso Salvare animal shelter database.

This module defines the :class:`AnimalShelter` class, which provides
Create, Read, Update, and Delete (CRUD) access to the ``animals``
collection of the ``aac`` MongoDB database. Other Python scripts can
import this module and instantiate the class to interface with MongoDB.
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError


class AnimalShelter:
    """Perform CRUD operations on the Austin Animal Center (aac) database."""

    def __init__(
        self,
        username,
        password,
        host="localhost",
        port=27017,
        db="aac",
        collection="animals",
    ):
        """Initialize the MongoClient connection to the aac database.

        Args:
            username: Authenticated MongoDB user (e.g. ``aacuser``).
            password: Password for the MongoDB user.
            host: Hostname where the mongod instance is running.
            port: Port the mongod instance is listening on.
            db: Name of the database to connect to.
            collection: Name of the collection to operate on.
        """
        # Build the connection string and open the authenticated client.
        self.client = MongoClient(
            "mongodb://%s:%s@%s:%d/%s" % (username, password, host, port, db)
        )
        self.database = self.client[db]
        self.collection = self.database[collection]

    def create(self, data):
        """Insert a document into the collection.

        Args:
            data: A dictionary (key/value pairs) representing the document.

        Returns:
            bool: ``True`` if the insert succeeded, ``False`` otherwise.
        """
        if data is None:
            raise ValueError("Nothing to save: data parameter is empty.")

        if not isinstance(data, dict):
            raise TypeError("data parameter must be a dictionary.")

        try:
            result = self.collection.insert_one(data)
            # acknowledged is True when the write was successfully applied.
            return result.acknowledged
        except PyMongoError as error:
            print("An error occurred while inserting the document: %s" % error)
            return False

    def read(self, query):
        """Query for document(s) in the collection.

        Args:
            query: A dictionary of key/value lookup pair(s) for ``find()``.

        Returns:
            list: Matching documents, or an empty list if none/failure.
        """
        if query is None:
            raise ValueError("Nothing to search: query parameter is empty.")

        if not isinstance(query, dict):
            raise TypeError("query parameter must be a dictionary.")

        try:
            # find() returns a cursor; convert it to a list to return results.
            return list(self.collection.find(query))
        except PyMongoError as error:
            print("An error occurred while reading documents: %s" % error)
            return []

    def update(self, query, new_values, update_many=True):
        """Update document(s) matching a query.

        Args:
            query: A dictionary of key/value lookup pair(s) for ``find()``.
            new_values: A dictionary of key/value pairs to apply. These are
                wrapped in a ``$set`` operator before updating.
            update_many: When ``True`` (default) update all matching
                documents; when ``False`` update only the first match.

        Returns:
            int: The number of documents modified.
        """
        if query is None:
            raise ValueError("Nothing to search: query parameter is empty.")

        if new_values is None:
            raise ValueError("Nothing to update: new_values parameter is empty.")

        if not isinstance(query, dict) or not isinstance(new_values, dict):
            raise TypeError("query and new_values parameters must be dictionaries.")

        try:
            if update_many:
                result = self.collection.update_many(query, {"$set": new_values})
            else:
                result = self.collection.update_one(query, {"$set": new_values})
            return result.modified_count
        except PyMongoError as error:
            print("An error occurred while updating documents: %s" % error)
            return 0

    def delete(self, query, delete_many=True):
        """Remove document(s) matching a query.

        Args:
            query: A dictionary of key/value lookup pair(s) for ``find()``.
            delete_many: When ``True`` (default) remove all matching
                documents; when ``False`` remove only the first match.

        Returns:
            int: The number of documents removed.
        """
        if query is None:
            raise ValueError("Nothing to search: query parameter is empty.")

        if not isinstance(query, dict):
            raise TypeError("query parameter must be a dictionary.")

        try:
            if delete_many:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)
            return result.deleted_count
        except PyMongoError as error:
            print("An error occurred while deleting documents: %s" % error)
            return 0
