from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")
    
    def goal_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            tasks=[task.task_dict() for task in self.tasks]
        )
        
