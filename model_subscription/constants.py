from enum import Enum


class OperationType(str, Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
