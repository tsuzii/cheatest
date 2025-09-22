from sqlalchemy import BigInteger, ForeignKey, Integer, Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import created_at, Base


class TextInsertModel(Base):
    __tablename__ = "text_inserts"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    text: Mapped[str]
    created_at: Mapped[created_at]

    user = relationship("UserModel", back_populates="text_inserts")
