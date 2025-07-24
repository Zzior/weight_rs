from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from utils.logger import LogWriter
from db.database import DatabaseManager
from meter.meter import WeightReader


class Config:
    def __init__(self):
        self.app_dir = Path(__file__).parent.parent
        self.configs_dir = self.app_dir / "storage"

        load_dotenv(self.configs_dir / ".env")
        self.logger = LogWriter(self.configs_dir / "app.log")

        # env
        self.url = getenv("URL")
        self.login = getenv("LOGIN")
        self.password = getenv("PASSWORD")

        self.port = getenv("PORT")
        self.location_name = getenv("LOCATION_NAME")
        self.read_interval = float(getenv("READ_INTERVAL"))
        self.send_interval = float(getenv("SEND_INTERVAL"))
        self.minimal_weight = int(getenv("MINIMAL_WEIGHT"))
        self.db_max_records = int(getenv("DB_MAX_RECORDS"))

        self.db = DatabaseManager(self.configs_dir / "database.db")
        self.meter = WeightReader(self.port)


conf = Config()
