from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, str_uniq, int_pk


class FilmGrade(Base):
    film_id: Mapped[int] = mapped_column(
        ForeignKey("films.id", ondelete="CASCADE"),
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    grade: Mapped[int]
    extend_existing = True

    def __str__(self):
        return (f"{self.__class__.__name__}(film_id={self.film_id}, "
                f"user_id={self.user_id}")

    def __repr__(self):
        return str(self)