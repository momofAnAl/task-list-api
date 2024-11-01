from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    complete_at: Mapped[datetime] = mapped_column(nullable=True, default=None)

    def task_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            complete_at=self.complete_at
        )