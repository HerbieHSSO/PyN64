from PyN64.rom import ROM
from PyN64 import RDP
from PyN64 import RSP
from PyN64.RDRAM import ri
from PyN64.CPU.instruction_decoding import FetchAndDecode
from PyN64.CPU.cp0 import *
from PyN64.CPU.cp1 import *
from functools import lru_cache





def analysis(value):
    value = hex(value)

    val = str(value).replace('0x','')
    if len(val) == 1:
        value = f'0x0{val}'
    return str(value).replace('0x', '')

def padhexa(s):
    s = str(s)
    return '0x' + s[2:].zfill(8)




    



 
class Memory:
    def __init__(self, rom: ROM, rdp: RDP, rsp: RSP):
        self.rom = rom
        self.rdp = rdp

        self.ri = ri.Registers()


        self.naddr = {}
        
        self.kseg1 = {}
        self.RDRAM = {}

        self.DMEM = {}
        self.IMEM = {}

        self.MI = {}

    def read(self, address):
       
        if address < 0:
            ValueError(f"Trying to write negative address to {hex(address)}")
            

        
        elif 0x03F00000 <= address <= 0x03FFFFFF:
            #RDRAM Registers
            return 0
        #SP Registers
        elif 0xA4000000 <= address <= 0xA40FFFFF:
            #SP_DMEM
            if 0xA4000000 <= address <= 0xA4000FFF:
                return int(self.DMEM[f'{address - 0xA4000000}'], 16)
            #SP_IMEM
            if 0xA4001000 <= address <= 0xA4001FFF:
                return int(self.IMEM[f'{address}'])
            elif 0xA4080000 <= address <= 0xA4080008:
                return 0

        elif 0x04100000 <= address <= 0x041FFFFF:
            #DP Command Registers
            print('Display')
            return 0
        elif 0xA4300000 <= address <= 0xA43FFFFF:
            # MIPS Interface
            return int(self.MI[f'{address - 0xA4300000}'])
        elif 0x04400000 <= address <= 0x044FFFFF:
            # Video Interface
            print('video')
        elif 0xA4600000 <= address <= 0xA46FFFFF:
            return 0
        elif 0xA4700000 <= address <= 0xA48FFFFF:
            # RDRAM Interface
            if 0xA4700004 <= address <= 0xA4700007:
                return self.ri.get('current_control')
            if 0xa470000c <= address <= 0xA470000F:
                return self.ri.get('ri_select_reg')
            if 0xa4800000 <= 0xa480000F:
                return 0
        elif 0x10000000  <= address <= 0x1FBFFFFF:
            #Cartridge Domain 1 Address 2
            return self.rom.read(address)
      
       

        elif 0x80000000 <= address <= 0x80800000:
            #RDRAM Cached
            if address >= 0x80246000:
                return int(f'0x{self.rom.read(address - 0x80245000):02x}{self.rom.read(address+1 - 0x80245000):02x}{self.rom.read(address+2 - 0x80245000):02x}{self.rom.read(address+3 - 0x80245000):02x}', 16)
            try:
                return int(self.RDRAM[f'{address - 0x80000000}'])
            except:
                return 0


        elif 0xA0000000 <= address <= 0xA0800000:
            #RDRAM Uncached
         
            return int(self.RDRAM[f'{address - 0xA0000000}'])        

        elif 0xB0000000 <= address <= 0xBFC00000:            
        
           
         
            return int(f'0x{self.rom.read(address - 0xB0000000):02x}{self.rom.read(address+1 - 0xB0000000):02x}{self.rom.read(address+2 - 0xB0000000):02x}{self.rom.read(address+3 - 0xB0000000):02x}', 16)
        elif 0xBFC00000 <= address <= 0xBFCFFFFF:   
            try:
                return int(self.RDRAM[f'{address}'])
            except:
                return 0
        else:
            raise ValueError(f'ERROR: Read from {hex(address)}')
    
    def write(self, address, value):
        
        if address < 0:
            ValueError(f"Trying to write negative address {hex(address)}")
        if value is None:
            raise ValueError(f"Trying to write None to {hex(address)}")

        elif 0x03F00000 <= address <= 0x03FFFFFF:
            #RDRAM Registers
            None
        
        #SP Registers
        elif 0xA4000000 <= address <= 0xA40FFFFF:
            #SP_DMEM
            if 0xA4000000 <= address <= 0xA4000FFF:
                self.DMEM.update({f'{address}': f'{value}'})
            #SP_IMEM
            if 0xA4001000 <= address <= 0xA4001FFF:
                self.IMEM.update({f'{address}': f'{value}'})






            
        elif 0x04100000 <= address <= 0x041FFFFF:
            #DP Command Registers
            print('DP Reg')
            None
        elif 0xA4300000 <= address <= 0xA43FFFFF:
            # MIPS Interface
            self.MI.update({f'{address - 0xA4300000}': f'{value}'})
            
        elif 0xA4600000 <= address <= 0xA46FFFFF:
            if address == 0xA4600000:
                return 0
            if address == 0xA4600010:
                return 0
        elif 0xA4500000 <= address <= 0xA45FFFFF:


                return 0        
        elif 0xA4700000 <= address <= 0xA48FFFFF:
            # RDRAM Interface
            if 0xA4700004 <= address <= 0xA4700007:
                self.ri.set('current_control', value)
            elif 0xA470000C <= address <= 0xA470000F:
                self.ri.set('ri_select_reg', value)
            if 0xa4800000 <= 0xa480000F:
                return 0
            else:
                return 0
        elif 0x10000000  <= address <= 0x1FBFFFFF:
            #Cartridge Domain 1 Address 2
            None





        elif 0x80000000  <= address <= 0x80800000:
            #RDRAM Cached
            
            self.RDRAM.update({f'{address - 0x80000000}': f'{value}'})
            
        elif 0xA0000000  <= address <= 0xA0800000:
            #RDRAM Uncached
            self.RDRAM.update({f'{address - 2684354560}': f'{value}'})
        elif 0xB0000000 <= address <= 0xBFCFFFFF:            
            
           self.RDRAM.update({f'{address}': f'{value}'})

        else:
            raise ValueError(f'ERROR: Write from {hex(address)}')



    def overwrite(self, memory, value):
        if memory == "DMEM":
            self.DMEM = value









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
            "fp": 0,
            "ra": 0,
        }

        self.special_registers = {
            "HI": 0,
            "LO": 0,
        }
       
    def set(self, register_name, value):
        try:

            if register_name != "zr":
                self._registers[register_name] = value

            if register_name == "a3":
                if self._registers[register_name] == 335766205774460:
                    None
                    
        except:
            self.special_registers[register_name] = value
    def get(self, register_name):

        try:
            return self._registers[register_name]
        except:
            return self.special_registers[register_name]









class CPU:

    def __init__(self, registers, memory, program_counter: int):
        self.registers = registers
        self.memory = memory
        self.program_counter = program_counter
        
        self.cp0 = CP0(CP0_Registers())
        self.cp1 = CP1(CP1_Registers())
        self.op = 0
    

    

    def decode(self, instruction):
        FetchAndDecode(self, instruction)
   
    
    def fetch(self):
        value = self.memory.read(self.program_counter)
        self.program_counter += 4
        
        return f'0x{value:08x}'
        
    def store(self, address, value):
        if address < 0:
            address = int(address & 0xFFFF_FFFF)

        if str(value) == "0x-5bffeab0":
            None
        #print(f'store: {hex(address)}, {value}')
        
        if address == 2952790036:
            None   
        
        self.memory.write(address, value)

        
    def load(self,address):
        if address < 0:
            address = int(address &  0xFFFF_FFFF)
        #print(f'address: {address}')
        print(self.memory.read(address))
        value = int(f'0x{int(self.memory.read(address) & 0xFFFF_FFFF):08x}', 16)
        if address == 0xB0000010:
            None
        #print(f'value: {value}')
        return value

    def set_pc(self, value):
        self.program_counter = value

    def get_pc(self):
        return int(self.program_counter) 

    def increase_op(self):
        self.op += 1
    def get_op(self):
        return self.op

    def execute_next_instruction(self, cpu, pc):
        value = self.memory.read(self.program_counter)
        print(f'pc: {hex(self.get_pc())}, instruction: 0x{value:08x}')
        return f'{value:08x}'        




















