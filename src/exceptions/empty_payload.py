from exceptions.base import SchemaError

class EmptyPayload(SchemaError):
    def __init__(self) -> None:
        super().__init__('At least one field is expected')