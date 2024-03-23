

















class Registers:
    def __init__(self):
        self._registers = {
            "RDRAM_CONFIG_REG": 0,
            "RDRAM_DEVICE_ID_REG" : 0,
            "RDRAM_DELAY_REG": 0,
            "RDRAM_MODE_REG": 0,
            "RDRAM_REF_INTERVAL_REG": 0,
            "RDRAM_REF_ROW_REG": 0,
            "RDRAM_RAS_INTERVAL_REG": 0,
            "RDRAM_MIN_INTERVAL_REG": 0,
            "RDRAM_ADDR_SELECT_REG": 0,
            "RDRAM_DEVICE_MANUF_REG": 0,
        }
    def set(self, register_name, value, offset):

        byte1 = (self._registers[register_name] >> 24) & 0xFF
        byte2 = (self._registers[register_name] >> 16) & 0xFF
        byte3 = (self._registers[register_name] >> 8) & 0xFF
        byte4 = self._registers[register_name] & 0xFF  
        if offset == 0:
            self._registers[register_name] =  (value << 24) | (byte2 << 16) | (byte3 << 8) | byte4
        if offset == 1:
            self._registers[register_name] =  (byte1 << 24) | (value << 16) | (byte3 << 8) | byte4
        if offset == 2:
            self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (value << 8) | byte4
        if offset == 3:
            self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value

    def get(self, register_name):
        return self._registers[register_name]







class RDRAM:
    def __init__(self):
        self.registers = Registers()