from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.types import String, Integer, Text, LargeBinary, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from snep_ai.database import Base

# InformationCategory   = Parent Table  (Many)
# InformationList       = Child Table   (One)
class InformationList(Base):
    __tablename__ = 'information_lists'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # One to Many relationship
    information_category_id: Mapped[int] = mapped_column(ForeignKey("information_categories.id"))
    information_category: Mapped["InformationCategory"] = relationship(back_populates="information_lists")

    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)
    image: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timerelevancy: Mapped[str] = mapped_column(Date)
    
    # Representation
    def __repr__(self):
        return f'<InformationList {self.title!r}>'