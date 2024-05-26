from sqlalchemy import ForeignKey
from sqlalchemy.types import Integer, Text, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from snep_ai.database import Base

# InformationCategory   = Parent Table  (Many)
# PromptLog             = Child Table   (One)

# User                  = Parent Table  (Many)
# PromptLog             = Child Table   (One)
class PromptLog(Base):
    __tablename__ = 'prompt_logs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    information_category_id: Mapped[int] = mapped_column(ForeignKey("information_categories.id"))
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    date: Mapped[str] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(100))
    probability: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(Text)

    # One to Many relationship
    user: Mapped["User"] = relationship(back_populates="prompt_logs")
    information_category: Mapped["InformationCategory"] = relationship(back_populates="prompt_logs")
    
    # Representation
    def __repr__(self):
        return f'<PromptLog {self.title!r}>'