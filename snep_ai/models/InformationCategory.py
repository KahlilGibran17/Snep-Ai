from typing import List
from sqlalchemy.types import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from snep_ai.database import Base

# InformationCategory   = Parent Table  (Many)
# InformationList       = Child Table   (One)
class InformationCategory(Base):
    __tablename__ = 'information_categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[str] = mapped_column(String(50))
    
    # Many to One relationship
    information_lists: Mapped[List["InformationList"]] = relationship(back_populates="information_category")
    prompt_logs: Mapped[List["PromptLog"]] = relationship(back_populates="information_category")

    # Representation
    def __repr__(self):
        return f'<InformationCategory {self.title!r}>'