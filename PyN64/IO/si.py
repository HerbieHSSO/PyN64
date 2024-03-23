



class Registers:
    def __init__(self):

        self._registers = {
            "SI_DRAM_ADDR_REG": 0,
            "SI_PIF_ADDR_RD64B_REG": 0,
            "SI_PIF_ADDR_WR64B_REG": 0,
            "SI_STATUS_REG": 0,


        }


        self.pif_ram = {}





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
            
            
            
    def get(self, register_name, offset):
        byte1 = (self._registers[register_name] >> 24) & 0xFF
        byte2 = (self._registers[register_name] >> 16) & 0xFF
        byte3 = (self._registers[register_name] >> 8) & 0xFF
        byte4 = self._registers[register_name] & 0xFF  
        if offset == 0:
            return byte1
        if offset == 1:
            return byte2
        if offset == 2:
            return byte3
        if offset == 3:
            return byte4

    
    def get_pif_ram(self, address):
        return self.pif_ram[address]

    def overwrite_pif_ram(self, block):
        self.pif_ram = block



    def get_bit(self, register_name, bit):
        return (self._registers[register_name] & (1 << bit)) >> bit

    def set_bit(self, register_name, bit):
        self._registers[register_name] = self._registers[register_name] | (1<<bit)

    def clear_bit(self, register_name, bit):
        self._registers[register_name] = self._registers[register_name] & ~(1<<bit)



















