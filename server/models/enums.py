from enum import Enum


class AlignmentStatus(str, Enum):
    MATCHES = "MATCHES"
    CONFLICTS = "CONFLICTS"
    NO_OFFICIAL_DATA = "NO_OFFICIAL_DATA"
    CANNOT_VERIFY = "CANNOT_VERIFY"
    DATA_UPDATED = "DATA_UPDATED"


class ElectionLevel(str, Enum):
    PRESIDENTIAL = "presidential"
    PARLIAMENTARY = "parliamentary"
    LOCAL = "local"
