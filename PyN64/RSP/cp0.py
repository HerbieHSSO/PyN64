




class CP0:
    def __init__(self, registers):
        self.registers = registers







class CP0_Registers:
    def __init__(self):
        self._registers = {
            "SP_MEM_ADDR_REG" : 0,
            "SP_DRAM_ADDR_REG": 0,
            "SP_RD_LEN_REG": 0,
            "SP_WR_LEN_REG": 0,
            "SP_STATUS_REG": 1,
            "SP_DMA_FULL_REG": 0,
            "SP_DMA_BUSY_REG": 0,
            "SP_SEMAPHORE_REG": 0,
            "SP_PC_REG": 0,
            "SP_IBIST_REG": 0,

            "DP_CMD_DMA_START": 0,
            "DP_CMD_DMA_END": 0,
            "DP_CMD_DMA_CURRENT": 0,
            "DP_CMD_STATUS": 0,
            "DP_CLOCK_END": 0,
            "DP_BUFFER_BUSY": 0,
            "DP_PIPE_END": 0,
            "DP_TMEM_REG": 0,

        }


    def set(self, register_name, value, offset):

        
        byte1 = (self._registers[register_name] >> 24) & 0xFF
        byte2 = (self._registers[register_name] >> 16) & 0xFF
        byte3 = (self._registers[register_name] >> 8) & 0xFF
        byte4 = self._registers[register_name] & 0xFF
        if register_name == 'SP_MEM_ADDR_REG':
            # Master, SP memory address
            if offset == 2:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (value << 8) | byte4
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value
            self._registers[register_name] = self._registers[register_name] & 0x1FFF
        
        if register_name == 'SP_DRAM_ADDR_REG':
            if offset == 1:
                self._registers[register_name] =  (byte1 << 24) | (value << 16) | (byte3 << 8) | byte4
            if offset == 2:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (value << 8) | byte4
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value 
        if register_name == 'SP_RD_LEN_REG':
            if offset == 0:
                self._registers[register_name] =  (value << 24) | (byte2 << 16) | (byte3 << 8) | byte4
            if offset == 1:
                self._registers[register_name] =  (byte1 << 24) | (value << 16) | (byte3 << 8) | byte4
            if offset == 2:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (value << 8) | byte4
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value
        if register_name == 'SP_WR_LEN_REG':
            if offset == 0:
                self._registers[register_name] =  (value << 24) | (byte2 << 16) | (byte3 << 8) | byte4
            if offset == 1:
                self._registers[register_name] =  (byte1 << 24) | (value << 16) | (byte3 << 8) | byte4
            if offset == 2:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (value << 8) | byte4
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value
        if register_name == 'SP_STATUS_REG':
                if offset == 3:
                    #clear SP mask
                    if (value & 0b1) != 0:
                        # clear halt
                        self.clear_bit('SP_STATUS_REG', 0)     
                    if (value & 0b10) != 0:
                        # set halt
                        self.set_bit('SP_STATUS_REG', 0)
                    if (value & 0b100) != 0:
                        # clear broke
                        self.clear_bit('SP_STATUS_REG', 1)
                    if (value & 0b1000) != 0:
                        # clear intr
                        None
                    if (value & 0b10000) != 0:
                        # set intr
                        None
                    if (value & 0b100000) != 0:
                        # clear sstep
                        self.clear_bit('SP_STATUS_REG', 5)
                    if (value & 0b1000000) != 0:
                        # set sstep
                        self.set_bit('SP_STATUS_REG', 5)
                    if (value & 0b1000000) != 0:
                        # set sstep
                        self.set_bit('SP_STATUS_REG', 5)
                    if (value & 0x80) != 0:
                        # clear intr on break
                        self.clear_bit('SP_STATUS_REG', 6)
                    if (value & 0x100) != 0:
                        # set intr on break
                        self.set_bit('SP_STATUS_REG', 6)
                    if (value & 0x200) != 0:
                        # clear signal 0
                        self.clear_bit('SP_STATUS_REG', 7)
                    if (value & 0x400) != 0:
                        # set signal 0
                        self.set_bit('SP_STATUS_REG', 7)
                    if (value & 0x800) != 0:
                        # clear signal 1
                        self.clear_bit('SP_STATUS_REG', 8)
                    if (value & 0x1000) != 0:
                        # set signal 1
                        self.set_bit('SP_STATUS_REG', 8)
                    if (value & 0x2000) != 0:
                        # clear signal 2
                        self.clear_bit('SP_STATUS_REG', 9)
                    if (value & 0x4000) != 0:
                        # set signal 2
                        self.set_bit('SP_STATUS_REG', 9)
                    if (value & 0x8000) != 0:
                        # clear signal 3
                        self.clear_bit('SP_STATUS_REG', 10)
                    if (value & 0x10000) != 0:
                        # set signal 3
                        self.set_bit('SP_STATUS_REG', 10)
                    if (value & 0x20000) != 0:
                        # clear signal 4
                        self.clear_bit('SP_STATUS_REG', 11)
                    if (value & 0x40000) != 0:
                        # set signal 4
                        self.set_bit('SP_STATUS_REG', 11)
                    if (value & 0x80000) != 0:
                        # clear signal 5
                        self.clear_bit('SP_STATUS_REG', 12)
                    if (value & 0x100000) != 0:
                        # set signal 5
                        self.set_bit('SP_STATUS_REG', 12)
                    if (value & 0x200000) != 0:
                        # clear signal 6
                        self.clear_bit('SP_STATUS_REG', 13)
                    if (value & 0x400000) != 0:
                        # set signal 6
                        self.set_bit('SP_STATUS_REG', 13)
                    if (value & 0x800000) != 0:
                        # clear signal 7
                        self.clear_bit('SP_STATUS_REG', 14)
                    if (value & 0x1000000) != 0:
                        # set signal 7
                        self.set_bit('SP_STATUS_REG', 14)

        if register_name == 'SP_SEMAPHORE_REG':
            self._registers[register_name] = 0
        
        if register_name == 'SP_PC_REG':
            if offset == 0:
                self._registers[register_name] =  (value << 24) | (byte2 << 16) | (byte3 << 8) | byte4
            if offset == 1:
                self._registers[register_name] =  (byte1 << 24) | (value << 16) | (byte3 << 8) | byte4
            if offset == 2:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (value << 8) | byte4
            if offset == 3:
                self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value

            self._registers[register_name] = self._registers[register_name] & 0xFFF
        
        if register_name == 'SP_IBIST_REG':
            if offset == 3:
                if (value & 0b1) != 0:
                    self.set_bit('SP_IBIST_REG', 0)
                if (value & 0b10) != 0:
                    self.set_bit('SP_IBIST_REG', 1)
                if (value & 0b100) != 0:
                    self.clear_bit('SP_IBIST_REG', 0)
                    self.clear_bit('SP_IBIST_REG', 1)
        #self._registers[register_name] = value

    def get(self, register_name):
        #if self._registers['index'] == 
        return self._registers[register_name]

    def get_bit(self, register_name, bit):
        return (self._registers[register_name] & (1 << bit)) >> bit

    def set_bit(self, register_name, bit):
        self._registers[register_name] = self._registers[register_name] | (1<<bit)

    def clear_bit(self, register_name, bit):
        self._registers[register_name] = self._registers[register_name] & ~(1<<bit)









        """
        if register_name == 'SP_STATUS_REG':
            clear_bits = 0
            set_bits = 0

            start_rsp = False
            stop_rsp = False
            
            if (value & 0x01):
                clear_bits |= 1
                start_rsp = True
            if (value & 0x02):
                set_bits |= 1
                stop_rsp = True

            clear_bits |= (value & 4) >> 1
            clear_bits |= (value & 32)
            clear_bits |= (value & 128) >> 1
            clear_bits |= (value & 512) >> 2
            clear_bits |= (value & 2048) >> 3
            clear_bits |= (value & 8192) >> 4
            clear_bits |= (value & 32768) >> 5
            clear_bits |= (value & 131072) >> 6
            clear_bits |= (value & 524288) >> 7
            clear_bits |= (value & 2097152) >> 8
            clear_bits |= (value & 8388608) >> 9
            
            set_bits |= (value & 64) >> 1
            set_bits |= (value & 256) >> 2
            set_bits |= (value & 1024) >> 3
            set_bits |= (value & 4096) >> 4
            set_bits |= (value & 16384) >> 5
            set_bits |= (value & 65536) >> 6
            set_bits |= (value & 262144) >> 7
            set_bits |= (value & 1048576) >> 8
            set_bits |= (value & 4194304) >> 9
            set_bits |= (value & 16777216) >> 10


            value = self._registers['SP_STATUS_REG'] 
            value &= not clear_bits
            value |=  set_bits

            if start_rsp:
                None
        """







