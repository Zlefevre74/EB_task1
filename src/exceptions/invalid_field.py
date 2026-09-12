from exceptions.base import SchemaError

class InvalidField(SchemaError):
    def __init__(self, field_name: str, reason: str) -> None:
        self.field_name = field_name
        self.reason = reason
        super().__init__(f'Invalid field "{field_name}". Reason: "{reason}"')