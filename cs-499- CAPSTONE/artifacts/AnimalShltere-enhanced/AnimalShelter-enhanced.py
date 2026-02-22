import os
import logging
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError


# Basic logging so errors are easier to track when something goes wrong
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnimalShelter:
    """
    This class handles all CRUD operations for the AAC animals collection.
    It is used by the dashboard to create, read, update, and delete records
    from the MongoDB database.
    """

    def __init__(
        self,
        mongo_uri: Optional[str] = None,
        db_name: str = "AAC",
        collection_name: str = "animals",
    ) -> None:
        # Try to get the MongoDB URI from an environment variable first.
        # If it is not set, fall back to the URI used in the original project.
        default_uri = "mongodb://aacuser:wm2360@nv-desktop-services.apporto.com:31475"
        self.mongo_uri: str = mongo_uri or os.getenv("MONGO_URI", default_uri)

        # Connect to MongoDB and set up the database and collection
        self.client: MongoClient = MongoClient(self.mongo_uri)
        self.database: Database = self.client[db_name]
        self.collection: Collection = self.database[collection_name]

        logger.info(
            "Connected to MongoDB database '%s' and collection '%s'",
            db_name,
            collection_name,
        )

    def create(self, data: Dict[str, Any]) -> bool:
        """
        Insert a new animal record into the database.
        Returns True if the insert works, otherwise False.
        """
        if not isinstance(data, dict):
            raise ValueError("Create expects data to be a dictionary.")
        if not data:
            raise ValueError("Empty data cannot be inserted.")

        try:
            result = self.collection.insert_one(data)
            return result.inserted_id is not None
        except PyMongoError as e:
            logger.exception("Insert error: %s", e)
            return False

    def read(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find and return records that match the given query.
        Returns an empty list if nothing is found.
        """
        if not isinstance(query, dict):
            raise ValueError("Read expects query to be a dictionary.")

        try:
            return list(self.collection.find(query))
        except PyMongoError as e:
            logger.exception("Read error: %s", e)
            return []

    def update(self, query: Dict[str, Any], new_values: Dict[str, Any]) -> int:
        """
        Update records that match the query.
        Returns the number of documents that were modified.
        """
        if not isinstance(query, dict):
            raise ValueError("Update expects query to be a dictionary.")
        if not isinstance(new_values, dict):
            raise ValueError("Update expects new_values to be a dictionary.")
        if not query:
            raise ValueError("Update requires a non-empty query.")
        if not new_values:
            raise ValueError("Update requires non-empty new values.")

        try:
            result = self.collection.update_many(query, {"$set": new_values})
            return result.modified_count
        except PyMongoError as e:
            logger.exception("Update error: %s", e)
            return 0

    def delete(self, query: Dict[str, Any]) -> int:
        """
        Delete records that match the query.
        Returns the number of documents deleted.
        """
        if not isinstance(query, dict):
            raise ValueError("Delete expects query to be a dictionary.")
        if not query:
            raise ValueError("Delete requires a non-empty query.")

        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError as e:
            logger.exception("Delete error: %s", e)
            return 0
