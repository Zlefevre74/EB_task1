import enum

class PermissionLevel(enum.StrEnum):
    READ = 'read'
    WRITE = 'write'
    ADMIN = 'admin'