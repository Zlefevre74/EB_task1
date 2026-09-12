

class AppError(Exception):
    status_code: int = 500

class SchemaError(ValueError):
    pass