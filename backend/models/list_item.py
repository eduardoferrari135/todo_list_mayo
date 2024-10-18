import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base

class ListItem(Base):
    __tablename__ = "list_items"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    task: Mapped[str]
    status: Mapped[str]

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "task": self.task,
            "status": self.status
        }
