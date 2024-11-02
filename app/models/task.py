from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(nullable=True)

    def task_dict(self):
        complete_at_null = False
        if self.completed_at:
            complete_at_null = True
        
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete = complete_at_null   
        )