




class CP0:
    def __init__(self, registers):
        self.registers = registers







class CP0_Registers:
    def __init__(self):
        self._registers = {
            "index" : 0,
            "random": 0,
            "entryLo0": 0,
            "entryLo1": 0,
            "context": 0,
            "pageMask": 0,
            "wired": 0,
            "hwrEna": 0,
            "badvAddr": 0,
            "count": 0,
            "entryHi": 0,
            "compare": 0,
            "status": 0,
            "cause": 0,
            "epc": 0,
            "prid": 0,
            "config": 0,
            "lladdr": 0,
            "watchLo": 0,
            "watchHi": 0,
            "?20?": 0,
            "?21?": 0,
            "?22?": 0,
            "debug": 0,
            "depc": 0,
            "perfctl": 0,
            "ecc": 0,
            "cacheerr": 0,
            "taglo": 0,
            "taghi": 0,
            "errorepc": 0,
            "desave": 0,
        }


    def set(self, register_name, value):
        self._registers[register_name] = value
    def get(self, register_name):
        return self._registers[register_name]



















