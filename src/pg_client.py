import psycopg2
from config import config


class PgClient:
    def __init__(self, host=config["host"], user=config["user"],
                 password=config["password"], db_name=config["db_name"]):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.connection = None

    def connect(self, autocommit=True):
        self.connection = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name,
        )
        self.connection.autocommit = autocommit
        # print("🆗  🔗 Connected to db")

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            # print("🆗  ✖️ Connection to db closed")
