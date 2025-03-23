from abc import ABC, abstractmethod
import psycopg2  # type: ignore
import os
import dotenv

dotenv.load_dotenv()


class Database(ABC):
    """
    Database context manager
    """

    def __init__(self, driver) -> None:
        # what is type of driver?
        self.driver = driver

    @abstractmethod
    def connect_to_database(self):
        raise NotImplementedError()

    # Special method used in Python's context manager protocol
    # Related to the "with" keyword
    def __enter__(self):
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()
        return self

    # Leaving the "with" block
    def __exit__(self, exception_type, exc_val, traceback):
        self.cursor.close()
        self.connection.close()


class PgDatabase(Database):
    """PostgreSQL Database context manager"""

    def __init__(self) -> None:
        self.driver = psycopg2
        super().__init__(self.driver)

    def connect_to_database(self):
        return self.driver.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
