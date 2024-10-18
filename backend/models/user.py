from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    salt: Mapped[bytes]
    name: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
