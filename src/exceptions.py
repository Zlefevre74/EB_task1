

class AppError(Exception):
    pass

class NotFound(AppError):
    def __init__(self, entity: str, entity_id) -> None:
        self.entity = entity
        self.entity_id = entity_id
        super().__init__(f'{entity} with id {entity_id} not found.')

