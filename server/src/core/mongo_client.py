from pymongo import MongoClient
from pymongo.errors import ConnectionFailure



from src.core.config import mongodb_settings
from src.utils.logging import get_logger

logger = get_logger(__file__)


class MongoDatabaseConnector:
    """Singleton class to connect to MongoDB database."""

    _instance: MongoClient | None = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            try:
                cls._instance = MongoClient(mongodb_settings.MONGODB_URL)
                logger.info(
                    f"Connection to database with uri: {mongodb_settings.MONGODB_URL} successful"
                )
            except ConnectionFailure:
                logger.error(f"Couldn't connect to the database.")

                raise

        return cls._instance

    def get_database(self, database_name: str | None = None):
        assert self._instance, "Database connection not initialized"

        return self._instance[database_name]

    def close(self):
        if self._instance:
            self._instance.close()
            logger.info("Connected to database has been closed.")


connection = MongoDatabaseConnector()
