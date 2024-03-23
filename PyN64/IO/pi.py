



class Registers:
    def __init__(self, memory):

        self._registers = {
            "PI_DRAM_ADDR_REG": 0,
            "PI_CART_ADDR_REG": 0,
            "PI_RD_LEN_REG": 0,
            "PI_WR_LEN_REG": 0,
            "PI_STATUS_REG": 0,
            "PI_BSD_DOM1_LAT_REG ": 0,
            "PI_BSD_DOM1_PWD_REG": 0,
            "PI_BSD_DOM1_PGS_REG": 0,      
            "PI_BSD_DOM1_RLS_REG ": 0,
            "PI_BSD_DOM2_LAT_REG ": 0,
            "PI_BSD_DOM2_PWD_REG": 0,   
            "PI_BSD_DOM2_PGS_REG": 0,      
            "PI_BSD_DOM2_RLS_REG ": 0,
     
        }


        self.memory = memory





    def set(self, register_name, value, offset):

        byte1 = (self._registers[register_name] >> 24) & 0xFF
        byte2 = (self._registers[register_name] >> 16) & 0xFF
        byte3 = (self._registers[register_name] >> 8) & 0xFF
        byte4 = self._registers[register_name] & 0xFF  


        if register_name == "PI_DRAM_ADDR_REG":
            if offset == 1:
                self._registers[register_name] =  (byte1 << 24) | (value << 16) | (byte3 << 8) | byte4
            if offset == 2:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (value << 8) | byte4
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value
        if register_name == "PI_CART_ADDR_REG":
            if offset == 0:
                self._registers[register_name] =  (value << 24) | (byte2 << 16) | (byte3 << 8) | byte4
            if offset == 1:
                self._registers[register_name] =  (byte1 << 24) | (value << 16) | (byte3 << 8) | byte4
            if offset == 2:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (value << 8) | byte4
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value            
        if register_name == "PI_RD_LEN_REG":
            if offset == 1:
                self._registers[register_name] =  (byte1 << 24) | (value << 16) | (byte3 << 8) | byte4
            if offset == 2:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (value << 8) | byte4
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value
                if self._registers[register_name] > 127:
                    self._registers[register_name] = 127
                for i in range(self._registers['PI_RD_LEN_REG'] * 8 - 1):
                    self.memory.write(self._registers['PI_DRAM_ADDR_REG']+i, self._registers['PI_CART_ADDR_REG'] + i)
        if register_name == "PI_WR_LEN_REG":
            if offset == 1:
                self._registers[register_name] =  (byte1 << 24) | (value << 16) | (byte3 << 8) | byte4
            if offset == 2:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (value << 8) | byte4
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value
                if self._registers[register_name] > 127:
                    self._registers[register_name] = 127
                for i in range(self._registers['PI_WR_LEN_REG'] * 8 - 1):
                    self.memory.write(self._registers['PI_CART_ADDR_REG']+i, self._registers['PI_DRAM_ADDR_REG'] + i)
            
        if register_name == "PI_STATUS_REG":
            if offset == 3:
                if (value & 0b10) != 0:
                    self.memory.mi.clear_bit('MI_INTR_REG', 4)
        if register_name == "PI_BSD_DOM1_LAT_REG":
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value
        if register_name == "PI_BSD_DOM1_PWD_REG":
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value
        if register_name == "PI_BSD_DOM1_PGS_REG":
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value & 0b111
        if register_name == "PI_BSD_DOM1_RLS_REG":
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value & 0b1
        if register_name == "PI_BSD_DOM2_LAT_REG":
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value 
        if register_name == "PI_BSD_DOM2_PWD_REG":
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value 
        if register_name == "PI_BSD_DOM2_PGS_REG":
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value & 0b111
        if register_name == "PI_BSD_DOM2_RLS_REG":
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value & 0b1         

    def get(self, register_name):
     
        return self._registers[register_name]
    
       
    def get_bit(self, register_name, bit):
        return (self._registers[register_name] & (1 << bit)) >> bit

    def set_bit(self, register_name, bit):
        self._registers[register_name] = self._registers[register_name] | (1<<bit)

    def clear_bit(self, register_name, bit):
        self._registers[register_name] = self._registers[register_name] & ~(1<<bit)


 



















