from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, str_uniq, int_pk


class FilmActor(Base):
    film_id: Mapped[int] = mapped_column(
        ForeignKey("films.id", ondelete="CASCADE"),
        primary_key=True
    )
    actor_id: Mapped[int] = mapped_column(
        ForeignKey("actors.id", ondelete="CASCADE"),
        primary_key=True
    )

    extend_existing = True

    def __str__(self):
        return (f"{self.__class__.__name__}(film_id={self.film_id}, "
                f"actor_id={self.actor_id}")

    def __repr__(self):
        return str(self)