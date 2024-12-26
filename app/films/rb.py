class RBFilm:
    def __init__(self, film_id: int | None = None,
                 title: str | None = None
                 ):
        self.id = film_id
        self.title = title

        
    def to_dict(self) -> dict:
        data = {'id': self.id, 'title': self.title}
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data