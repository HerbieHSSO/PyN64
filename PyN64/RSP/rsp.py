from PyN64.RSP.cp0 import *
from PyN64.RSP.decode import *



class Registers:
    def __init__(self):
        
        
     
        self._registers = {
            "zr": 0,
            "at": 0,
            "v0": 0,
            "v1": 0,
            "a0": 0,
            "a1": 0,
            "a2": 0,
            "a3": 0,
            "t0": 0,
            "t1": 0,
            "t2": 0,
            "t3": 0,
            "t4": 0,
            "t5": 0,
            "t6": 0,
            "t7": 0,
            "s0": 0,
            "s1": 0,
            "s2": 0,
            "s3": 0,
            "s4": 0,
            "s5": 0,
            "s6": 0,
            "s7": 0,
            "t8": 0,
            "t9": 0,
            "k0": 0,
            "k1": 0,
            "gp": 0,
            "sp": 0,
            "s8": 0,
            "ra": 0,
        }

  
       
    def set(self, register_name, value):
        if register_name != "zr":

            self._registers[register_name] = value
  



    def get(self, register_name):
        return self._registers[register_name]
  

class RSP:
    def __init__(self):
        self.registers = Registers()
        self.cp0 = CP0(CP0_Registers())
        
        self.program_counter = 0
        
        self.halted = True




    def fetch(self, memory):
        if self.halted == True:
            return
        value = memory.read(0xA4001000 + self.program_counter)
        self.program_counter = (self.program_counter + 4) & 0xFFC
        
        
        return f'0x{value:08x}'
    def decode(self, instruction):
        if self.halted == True:
            return
        FetchAndDecodeRSP(self, instruction)

    def get_pc(self):
        return self.program_counter
    def set_pc(self, value):
        self.program_counter = value

    def get_halt(self):
        return self.halted
    def set_halt(self, boolean):
        self.halted = boolean
     
    def execute_next_instruction(self, rsp, pc):
        value = self.memory.read(0xA4001000 + self.program_counter)
        #print(f'pc: {hex(self.get_pc())}, instruction: 0x{value:08x}')
        return f'{value:08x}'  




class DMEM:
    def __init__(self):
        self.DMEM = []


    def setDMEM(self, value):
        self.DMEM = value
