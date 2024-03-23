



class Registers:
    def __init__(self, cpu):

        self._registers = {
            "MI_INIT_MODE_REG": 0,
            "MI_VERSION_REG": 33685762,
            "MI_INTR_REG": 0,
            "MI_INTR_MASK_REG": 0,
        }








    def set(self, register_name, value, offset):



            if register_name == "MI_INIT_MODE_REG":
                if offset == 3:  
                    self._registers[register_name] = (self._registers[register_name] & ~0x7F) | (value & 0b1111111)
                    #clear init mode
                    if (value & 0b10000000) != 0:
                        self.clear_bit('MI_INIT_MODE_REG', 7)
                    #self._registers[register_name] =  (value << 24) | (byte2 << 16) | (byte3 << 8) | byte4
                if offset == 2:
                    #set init mode
                    if (value & 0b1) != 0:
                        self.set_bit('MI_INIT_MODE_REG', 7)
                    #clr ebus test mode
                    if (value & 0b10) != 0:
                        self.clear_bit('MI_INIT_MODE_REG', 8)
                    #set ebus test mode
                    if (value & 0b100) != 0:
                        self.clear_bit('MI_INIT_MODE_REG', 8)
                    #clear DP interrupt
                    if (value & 0b1000) != 0:
                        self.clear_bit('MI_INTR_REG', 5)
                    #clear RDRAM reg
                    if (value & 0b10000) != 0:
                        self.clear_bit('MI_INIT_MODE_REG', 9)
                    #set RDRAM reg
                    if (value & 0b100000) != 0:
                        self.set_bit('MI_INIT_MODE_REG', 9)

            if register_name == "MI_INTR_MASK_REG":           
                if offset == 3:
                    #clear SP mask
                    if (value & 0b1) != 0:
                        self.clear_bit('MI_INTR_MASK_REG', 0)
                    #set SP mask
                    if (value & 0b10) != 0:
                        self.set_bit('MI_INTR_MASK_REG', 0)
                    #clear SI mask
                    if (value & 0b100) != 0:
                        self.clear_bit('MI_INTR_MASK_REG', 1)
                    #set SI mask
                    if (value & 0b1000) != 0:
                        self.set_bit('MI_INTR_MASK_REG', 1)
                    #clear AI mask
                    if (value & 0x10) != 0:
                        self.clear_bit('MI_INTR_MASK_REG', 2)
                    #set AI mask
                    if (value & 0x20) != 0:
                        self.set_bit('MI_INTR_MASK_REG', 2)
                    #clear VI mask
                    if (value & 0x40) != 0:
                        self.clear_bit('MI_INTR_MASK_REG', 3)
                    #set VI mask
                    if (value & 0x80) != 0:
                        self.set_bit('MI_INTR_MASK_REG', 3)

                    #self._registers[register_name] =  (value << 24) | (byte2 << 16) | (byte3 << 8) | byte4
                if offset == 2:
                    #clear PI mask
                    if (value & 0b1) != 0:
                        self.clear_bit('MI_INTR_MASK_REG', 4)
                    #set PI mask
                    if (value & 0b10) != 0:
                        self.set_bit('MI_INTR_MASK_REG', 4)
                    #clear DP mask
                    if (value & 0b100) != 0:
                        self.set_bit('MI_INTR_MASK_REG', 5)
                    #set DP mask
                    if (value & 0b1000) != 0:
                        self.set_bit('MI_INTR_MASK_REG', 5)          


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
        return self._registers[register_name]
    
       
    def get_bit(self, register_name, bit):
        return (self._registers[register_name] & (1 << bit)) >> bit

    def set_bit(self, register_name, bit):
        self._registers[register_name] = self._registers[register_name] | (1<<bit)

    def clear_bit(self, register_name, bit):
        self._registers[register_name] = self._registers[register_name] & ~(1<<bit)


 



















