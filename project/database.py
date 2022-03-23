"""All database connection information is defined here"""
from sqlmodel import SQLModel, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy import event


DB_FILE = "devices.db"
sqlite_url = f"sqlite:///{DB_FILE}"

connect_args = {"check_same_thread": False}
engine = create_engine(
    sqlite_url, connect_args=connect_args, echo=True
)  # set echo=True to view output


# From SQLAlchemy docs to allow foreign Key support
# https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#foreign-key-support
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Used to enable foreign keys in sqlite"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_db_and_tables():
    """Used to create and initialize DB"""
    SQLModel.metadata.create_all(engine)
