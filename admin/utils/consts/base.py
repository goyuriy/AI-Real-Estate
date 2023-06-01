from enum import Enum

class ReprEnum(Enum):
    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value
