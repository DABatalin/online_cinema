class RBFilmDirector:
    def __init__(self, director_id: int | None = None,
                 film_id: int | None = None
                 ):
        self.director_id = director_id
        self.film_id = film_id

        
    def to_dict(self) -> dict:
        data = {'film_id': self.film_id, 'director_id': self.director_id}
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data