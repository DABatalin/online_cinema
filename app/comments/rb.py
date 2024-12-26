class RBComment:
    def __init__(self, id: int | None = None,
                 user_id: int | None = None,
                 film_id: int | None = None
                 ):
        self.id = id
        self.user_id = user_id
        self.film_id = film_id

        
    def to_dict(self) -> dict:
        data = {'id': id, 'film_id': self.film_id, 'user_id': self.user_id}
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data