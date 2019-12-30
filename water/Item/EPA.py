import enum

class Code(enum):
    Stop = 0
    Normal = 10
    Test = 20
    Invalid = 30
    Maintain = 31
    PLCError = 32
    ReplaceByBackupMachine = 91
    ReplaceByGovMechanism = 92
    ReplaceByPastData = 93
    ReplaceByElse = 94 

class Type(enum):
    Column = 100
    PH = 246
    Ohm = 247
    Liter = 248
    Celsius = 259
    Camera = 330