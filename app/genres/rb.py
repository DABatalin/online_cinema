class RBGenre:
    def __init__(self, genre_id: int | None = None,
                 name: str | None = None
                 ):
        self.id = genre_id
        self.name = name

        
    def to_dict(self) -> dict:
        data = {'id': self.id, 'name': self.name}
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data