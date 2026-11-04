from exceptions.base import AppError

class Conflict(AppError):
    status_code: int = 409