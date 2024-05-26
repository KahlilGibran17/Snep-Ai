from typing import Optional, List
from sqlalchemy.types import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from snep_ai.database import Base

# User                  = Parent Table  (Many)
# PromptLog             = Child Table   (One)
class User(Base, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(default=False)
    token: Mapped[Optional[str]]
    
    # Many to One relationship
    prompt_logs: Mapped[List["PromptLog"]] = relationship(back_populates="user")
    chat_logs: Mapped[List["ChatLog"]] = relationship(back_populates="user")

    # Representation
    def __repr__(self):
        return f'<User {self.username!r}>'
