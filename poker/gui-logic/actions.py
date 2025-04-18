from enum import Enum

class Action(Enum):
    FOLD = 1
    CHECK = 2
    CALL = 3
    BET = 4
    RAISE = 5
    ALL_IN = 6

    @staticmethod
    def action_string(C:int):
        match C:
            case 1:
                return Action.FOLD
            case 2:
                return Action.CHECK
            case 3:
                return Action.CALL
            case 4:
                return Action.BET
            case 5:
                return Action.RAISE
            case 6:
                return Action.ALL_IN