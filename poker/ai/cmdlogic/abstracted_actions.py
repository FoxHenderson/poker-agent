from enum import Enum

class AbstractAction(Enum):
    FOLD = 1
    CHECK = 2
    CALL = 3
    BET_HALF = 4
    BET_POT = 5
    RAISE_HALF = 6
    RAISE_POT = 7
    ALL_IN = 8

    @staticmethod
    def action_string(C:int):
        match C:
            case 1:
                return AbstractAction.FOLD
            case 2:
                return AbstractAction.CHECK
            case 3:
                return AbstractAction.CALL
            case 4:
                return AbstractAction.BET_HALF
            case 5:
                return AbstractAction.BET_POT
            case 6:
                return AbstractAction.RAISE_HALF
            case 7:
                return AbstractAction.RAISE_POT
            case 8:
                return AbstractAction.ALL_IN
            
