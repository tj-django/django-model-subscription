from enum import Enum, unique


@unique
class OperationType(str, Enum):
    """
    Operation Types.
    """

    CREATE = "create"
    BULK_CREATE = "bulk_create"
    UPDATE = "update"
    BULK_UPDATE = "bulk_update"
    DELETE = "delete"
    BULK_DELETE = "bulk_delete"
