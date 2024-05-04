




class CP0:
    def __init__(self, registers):
        self.registers = registers







class CP0_Registers:
    def __init__(self):
        self._registers = {
            "index" : 0,
            "random": 0,
            "entrylo0": 0,
            "entrylo1": 0,
            "context": 0,
            "pagemask": 0,
            "wired": 0,
            "hwrena": 0,
            "badvaddr": 0,
            "count": 0,
            "entryhi": 0,
            "compare": 0,
            "status": 0,
            "cause": 0,
            "epc": 0,
            "prid": 0,
            "config": 0,
            "lladdr": 0,
            "watchlo": 0,
            "watchhi": 0,
            "?20?": 0,
            "?21?": 0,
            "?22?": 0,
            "debug": 0,
            "depc": 0,
            "perfcnt": 0,
            "errctl": 0,
            "cacheerr": 0,
            "taglo": 0,
            "taghi": 0,
            "errorepc": 0,
            "desave": 0,
        }


    def set(self, register_name, value):
        self._registers[register_name] = value


        
    def get(self, register_name):
        #if self._registers['index'] == 
        return self._registers[register_name]




    def get_bit(self, register_name, bit):
        return (self._registers[register_name] & (1 << bit)) >> bit

    def set_bit(self, register_name, bit):
        self._registers[register_name] = self._registers[register_name] | (1<<bit)

    def clear_bit(self, register_name, bit):
        self._registers[register_name] = self._registers[register_name] & ~(1<<bit)














