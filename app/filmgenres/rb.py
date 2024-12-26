class RBFilmGenre:
    def __init__(self, genre_id: int | None = None,
                 film_id: int | None = None
                 ):
        self.genre_id = genre_id
        self.film_id = film_id

        
    def to_dict(self) -> dict:
        data = {'film_id': self.film_id, 'genre_id': self.genre_id}
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data