from enum import Enum

class Action(Enum):
    FOLD = 1,
    CHECK = 2,
    CALL = 3,
    BET = 4,
    RAISE = 5,
    ALL_IN = 6,