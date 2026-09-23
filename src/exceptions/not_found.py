from exceptions.base import AppError


class NotFound(AppError):
    status_code: int = 404
