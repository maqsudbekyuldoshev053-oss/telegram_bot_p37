from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from models.base import Model

class Category(Model):
    name: Mapped[str] = mapped_column(String(255))


    def __str__(self):
        return f"{self.id} - {self.name}"



