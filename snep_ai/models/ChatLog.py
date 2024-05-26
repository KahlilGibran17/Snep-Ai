from sqlalchemy import ForeignKey
from sqlalchemy.types import Integer, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from snep_ai.database import Base

# User      = Parent Table  (Many)
# ChatLog   = Child Table   (One)
class ChatLog(Base):
    __tablename__ = 'chat_logs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[str] = mapped_column(Date)
    message: Mapped[str] = mapped_column(Text)
    response: Mapped[str] = mapped_column(Text)

    # One to Many relationship
    user: Mapped["User"] = relationship(back_populates="chat_logs")
    
    # Representation
    def __repr__(self):
        return f'<ChatLog {self.message!r}>'