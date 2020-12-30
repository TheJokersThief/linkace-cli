from enum import Enum


class OrderBy(Enum):
    ID = "id"
    URL = "url"
    TITLE = "title"
    DESCRIPTION = "description"
    IS_PRIVATE = "is_private"
    STATUS = "status"
    CHECK_DISABLED = "check_disabled"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class OrderDir(Enum):
    ASC = "asc"
    DESC = "desc"
