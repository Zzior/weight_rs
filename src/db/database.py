from datetime import datetime, timedelta
from typing import Sequence
from pathlib import Path

from sqlalchemy import create_engine, select, delete, and_
from sqlalchemy.orm import Session

from .models import Base, Temp


class DatabaseManager:
    def __init__(self, db_path: Path):
        self.engine = create_engine(f'sqlite:///{db_path.resolve()}')
        Base.metadata.create_all(self.engine)

    def add_temp(self, date: datetime, weight: int):
        with Session(self.engine) as session:
            week_measurement = Temp(date=date, weight=weight)
            session.add(week_measurement)
            session.commit()

    def get_temp(self) -> Sequence[Temp]:
        with Session(self.engine) as session:
            query = select(Temp).order_by(Temp.id.asc())  # From the oldest entry to newest
            return session.execute(query).scalars().all()

    def clear_temp(self):
        with Session(self.engine) as session:
            session.execute(delete(Temp).execution_options(synchronize_session=False))
            session.commit()
