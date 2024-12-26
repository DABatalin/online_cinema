from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk, str_null_true


class Film(Base):
    id: Mapped[int_pk]
    title: Mapped[str]
    film_link: Mapped[str_null_true]
    description: Mapped[str_null_true]
    vote_count: Mapped[int]
    average_rating: Mapped[float]

    genres: Mapped[list['Genre']] = relationship(
        back_populates="films",
        secondary="filmgenres"
    )

    directors: Mapped[list['Director']] = relationship(
        back_populates="films",
        secondary="filmdirectors"
    )

    actors: Mapped[list['Actor']] = relationship(
        back_populates="films",
        secondary="filmactors"
    )

    extend_existing = True

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"film_title={self.title!r}, "
                f"film_link={self.film_link!r}, "
                f"description={self.description!r}, "
                f"vote_count={self.vote_count!r}, "
                f"average_rating={self.average_rating!r})")

    def __repr__(self):
        return str(self)