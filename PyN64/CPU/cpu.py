from PyN64.rom import ROM
from PyN64 import RDP

from PyN64.RDRAM import ri, rdram
from PyN64.IO import si, mi, pi
from PyN64.RDP.vi import VideoInterface
from PyN64.CPU.instruction_decoding import FetchAndDecode
from PyN64.CPU.cp0 import *
from PyN64.CPU.cp1 import *
from functools import lru_cache



def signToUnsign(value, bits):
    if value < 0:
        value = value+(1 << bits)
    return value

def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)
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
    def __init__(self, rom: ROM, rsp, rdp: RDP, rdram, cp0):
        self.rom = rom
        self.rsp = rsp
        self.rdp = rdp
   
        self.rdram = rdram
        self.ri = ri.Registers()


        self.naddr = {}
        
        self.kseg1 = {}
        self.RDRAM = {}

        self.DMEM = {}
        self.IMEM = {}

  
        self.VI = VideoInterface()
        self.si = si.Registers()
        self.mi = mi.Registers(self)
        self.DPC = {}
        self.AI = {}
        self.PI = pi.Registers(self)
        self.DD = {}
   
        self.cp0 = cp0
    
    def read(self, address):
        address = address & 0xFFFF_FFFF
        #address = address & 0xFFFF_FFFF
        if address < 0:
            ValueError(f"Trying to write negative address to {hex(address)}")
        

        

        elif 0xA3F00000 <= address <= 0xA3F00003:
            #RDRAM Registers
            return self.rdram.registers.get("RDRAM_CONFIG_REG")
        elif 0xA3F00004 <= address <= 0xA3F00007:
            #RDRAM Registers
            return self.rdram.registers.get("RDRAM_DEVICE_ID_REG")
        elif 0xA3F00008 <= address <= 0xA3F0000B:
            #RDRAM Registers
            return self.rdram.registers.get("RDRAM_DELAY_REG")
        elif 0xA3F0000C <= address <= 0xA3F0000F:
            #RDRAM Registers
            return self.rdram.registers.get("RDRAM_MODE_REG")
        elif 0xA3F000010 <= address <= 0xA3F00013:
            #RDRAM Registers
            return self.rdram.registers.get("RDRAM_REF_INTERVAL_REG")
        elif 0xA3F000014 <= address <= 0xA3F00017:
            #RDRAM Registers
            return self.rdram.registers.get("RDRAM_REF_ROW_REG")
        elif 0xA3F000018 <= address <= 0xA3F0001B:
            #RDRAM Registers
            return self.rdram.registers.get("RDRAM_RAS_INTERVAL_REG")
        elif 0xA3F00001C <= address <= 0xA3F0001F:
            #RDRAM Registers
            return self.rdram.registers.get("RDRAM_MIN_INTERVAL_REG")
        elif 0xA3F000020 <= address <= 0xA3F00023:
            #RDRAM Registers
            return self.rdram.registers.get("RDRAM_ADDR_SELECT_REG")
        elif 0xA3F000024 <= address <= 0xA3F00027:
            #RDRAM Registers
            return self.rdram.registers.get("RDRAM_DEVICE_MANUF_REG")
        elif 0xA3F80000 <= address <= 0xA3FFFFFF:
            return None
        
        elif 0xA4000000 <= address <= 0xA40FFFFF:
            #SP_DMEM
            if 0xA4000000 <= address <= 0xA4000FFF:
                
                return int(self.DMEM[f'{address - 0xA4000000}'],16)
            #SP_IMEM
            if 0xA4001000 <= address <= 0xA4001FFF:
                try:
                    return self.IMEM[f'{address - 0xA4001000}']   #return self.IMEM[f'{address - 0xA4001000}']
                except:
                    return 0
            #SP Registers
            if 0xA4040010 <= address <= 0xA4040013:
                # SP_STATUS_REG
                return self.rsp.cp0.registers.get('SP_STATUS_REG')

            if 0xA4080000 <= address <= 0xA4080003:
                # SP_PC_REG
                return self.rsp.cp0.registers.get('SP_PC_REG')

        elif 0xA4100000 <= address <= 0xA41FFFFF:
            #DP Command Registers 
            print('Display')
            return int(self.DPC[f'{address - 0xA4100000}'])
  
        elif 0xA4300000 <= address <= 0xA43FFFFF:
            # MIPS Interface
          
            if 0xA4300000 <= address <= 0xA4300003:
                return self.mi.get('MI_INIT_MODE_REG', address - 0xA4300000)
            if 0xA4300004 <= address <= 0xA4300007:
                return self.mi.get('MI_VERSION_REG', address - 0xA4300004)
            if 0xA4300008 <= address <= 0xA430000B:
                return self.mi.get('MI_INTR_REG', address - 0xA4300008)
            if 0xA430000C <= address <= 0xA430000F:
                return self.mi.get('MI_INTR_MASK_REG', address - 0xA430000C)
        elif 0xa4400000 <= address <= 0xa44FFFFF:
            # Video Interface
            print('video')
                
            if 0xa4400000 <= address <= 0xa4400003:
                return self.VI.registers.get('vi_ctrl', address - 0xa4400000)
            if 0xa4400004 <= address <= 0xa4400007:
                return self.VI.registers.get('vi_origin/draw_addr_reg', address - 0xa4400004)
            if 0xa4400008 <= address <= 0xa440000B:
                return self.VI.registers.get('vi_width/h_width_reg', address - 0xa4400008)
            if 0xa440000C <= address <= 0xa440000F:
                return self.VI.registers.get('vi_v_intr', address - 0xa440000C)            
            if 0xa4400010 <= address <= 0xa4400013:
                
                return self.VI.registers.get('vi_v_current_reg', address - 0xa4400010)

            if 0xa4400014 <= address <= 0xa4400017:
                return self.VI.registers.get('vi_burst/timing_reg', address - 0xa4400014)
            if 0xa4400018 <= address <= 0xa440001B:
                return self.VI.registers.get('vi_v_sync_reg', address - 0xa4400018)
            if 0xa440001C <= address <= 0xa440001F:
                return self.VI.registers.get('vi_h_sync_reg', address - 0xa440001C)            
            if 0xa4400020 <= address <= 0xa4400023:
                return self.VI.registers.get('vi_leap/h_sync_leap_reg', address - 0xa4400020)  
            if 0xa4400024 <= address <= 0xa4400027:
                return self.VI.registers.get('vi_h_start/h_video_reg', address - 0xa4400024)  
            if 0xa4400028 <= address <= 0xa440002B:
                return self.VI.registers.get('vi_v_start/v_video_reg', address - 0xa4400028)  
            if 0xa440002C <= address <= 0xa440002F:
                return self.VI.registers.get('vi_v_burst_reg', address - 0xa440002C) 
            if 0xa4400030 <= address <= 0xa4400033:
                return self.VI.registers.get('vi_x_scale_reg', address - 0xa4400030) 
            if 0xa4400034 <= address <= 0xa4400037:
                return self.VI.registers.get('vi_y_scale_reg', address - 0xa4400034) 


        elif 0xA4500000 <= address <= 0xA45FFFFF:
            return int(self.AI[f'{address - 0xA4600000}'])
        elif 0xA4600000 <= address <= 0xA46FFFFF:
            if 0xA4600000 <= address <= 0xA4600003:
                return self.PI.get('PI_DRAM_ADDR_REG') 
            if 0xA4600004 <= address <= 0xA4600007:
                return self.PI.get('PI_CART_ADDR_REG') 
            if 0xA4600008 <= address <= 0xA460000B:
                return self.PI.get('PI_RD_LEN_REG') 
            if 0xA460000C <= address <= 0xA460000F:
                return self.PI.get('PI_WR_LEN_REG') 
            if 0xA4600010 <= address <= 0xA4600013:
                return self.PI.get('PI_STATUS_REG') 
            if 0xA4600014 <= address <= 0xA4600017:
                return self.PI.get('PI_BSD_DOM1_LAT_REG') 
            if 0xA4600018 <= address <= 0xA460001B:
                return self.PI.get('PI_BSD_DOM1_PWD_REG') 
            if 0xA460001C <= address <= 0xA460001F:
                return self.PI.get('PI_BSD_DOM1_PGS_REG') 
            if 0xA4600020 <= address <= 0xA4600023:
                return self.PI.get('PI_BSD_DOM1_RLS_REG') 
            if 0xA4600024 <= address <= 0xA4600027:
                return self.PI.get('PI_BSD_DOM2_LAT_REG') 
            if 0xA4600028 <= address <= 0xA460002B:
                return self.PI.get('PI_BSD_DOM2_PWD_REG') 
            if 0xA460002C <= address <= 0xA460002F:
                return self.PI.get('PI_BSD_DOM2_PGS_REG') 
            if 0xA4600030 <= address <= 0xA4600033:
                return self.PI.get('PI_BSD_DOM2_RLS_REG') 

        elif 0xA4700000 <= address <= 0xA48FFFFF:
            # RDRAM Interface
            if 0xA4700004 <= address <= 0xA4700007:
                return self.ri.get('current_control')
            
            elif 0xa470000c <= address <= 0xA470000F:
                return self.ri.get('ri_select_reg')
       
            elif 0xa4800000 <= address <= 0xa4800003:
                return self.si.get('SI_DRAM_ADDR_REG', address - 0xa4800000)
            elif 0xa4800004 <= address <= 0xa4800007:
                return self.si.get('SI_PIF_ADDR_RD64B_REG', address - 0xa4800004)
            elif 0xa4800008 <= address <= 0xa480000F: 
                return 0   
            elif 0xa4800010 <= address <= 0xa4800013:
                return self.si.get('SI_PIF_ADDR_WR64B_REG', address - 0xa4800010)
            elif 0xa4800018 <= address <= 0xa480001B:
                return self.si.get('SI_STATUS_REG', address - 0xa4800018)  
            else:
                return 0
        elif 0x10000000  <= address <= 0x1FBFFFFF:
            #Cartridge Domain 1 Address 2
            return self.rom.read(address)
      
       

        elif 0x80000000 <= address <= 0x803FFFFF:
            #RDRAM Cached
            try:
                return int(self.RDRAM[f'{address - 0x80000000}'])
            except:
                if address >= 0x80246000:
                    return self.rom.read(address - 0x80245000)
                    #                    return int(f'0x{self.rom.read(address - 0x80245000):02x}', 16)
                return 0



        elif 0xA0000000 <= address <= 0xA0800000:
            #RDRAM Uncached
            try:
                return int(self.RDRAM[f'{address - 0xA0000000}'])   
            except:
                return 0     

        elif 0xB0000000 <= address <= 0xBFC00000:            
        
           
         
            return self.rom.read(address - 0xB0000000)
        elif 0xBFC00000 <= address <= 0xBFCFFFFF:   
            try:
                return int(self.RDRAM[f'{address - 0xBFC00000}'])
            except:
                return 0
        else:
            raise ValueError(f'ERROR: Read from {hex(address)}')
    
    def write(self, address, value):

        # I need to implement write 32bit, 16bit, instead loads each byte once each
        address = address & 0xFFFF_FFFF

        if address == 0x8033A858:
            None
        if address < 0:
            ValueError(f"Trying to write negative address {hex(address)}")
        if value is None:
            raise ValueError(f"Trying to write None to {hex(address)}")

        elif 0xA3F00000 <= address <= 0xA3F00003:
            #RDRAM Registers
            return self.rdram.registers.set("RDRAM_CONFIG_REG", value, address - 0xA3F00000)
        elif 0xA3F00004 <= address <= 0xA3F00007:
            #RDRAM Registers
            return self.rdram.registers.set("RDRAM_DEVICE_ID_REG", value, address - 0xA3F00004)
        elif 0xA3F00008 <= address <= 0xA3F0000B:
            #RDRAM Registers
            return self.rdram.registers.set("RDRAM_DELAY_REG", value, address - 0xA3F00008)
        elif 0xA3F0000C <= address <= 0xA3F0000F:
             #RDRAM Registers
            
            return self.rdram.registers.set("RDRAM_MODE_REG", value, address - 0xA3F0000C)
        elif 0xA3F000010 <= address <= 0xA3F00013:
            #RDRAM Registers
            return self.rdram.registers.set("RDRAM_REF_INTERVAL_REG", value, address - 0xA3F000010)
        elif 0xA3F000014 <= address <= 0xA3F00017:
            #RDRAM Registers
            return self.rdram.registers.set("RDRAM_REF_ROW_REG", value, address - 0xA3F000014)
        elif 0xA3F000018 <= address <= 0xA3F0001B:
            #RDRAM Registers
            return self.rdram.registers.set("RDRAM_RAS_INTERVAL_REG", value, address - 0xA3F000018)
        elif 0xA3F00001C <= address <= 0xA3F0001F:
            #RDRAM Registers
            return self.rdram.registers.set("RDRAM_MIN_INTERVAL_REG", value, address - 0xA3F00001C)
        elif 0xA3F000020 <= address <= 0xA3F00023:
            #RDRAM Registers
            return self.rdram.registers.set("RDRAM_ADDR_SELECT_REG", value, address - 0xA3F000020)
        elif 0xA3F000024 <= address <= 0xA3F00027:
            #RDRAM Registers
            return self.rdram.registers.set("RDRAM_DEVICE_MANUF_REG", value, address - 0xA3F000024)
        elif 0xA3F00028 <= address <= 0xA3FFFFFF:
            return None        
        #SP Registers
        elif 0xA4000000 <= address <= 0xA40FFFFF:
            #SP_DMEMff
            if 0xA4000000 <= address <= 0xA4000FFF:

                self.DMEM.update({f'{address - 0xA4000000}': f'{int(value)}'})  #self.DMEM.update({f'{address - 0xA4000000}': f'{int(value)}'})
            #SP_IMEM
            if 0xA4001000 <= address <= 0xA4001FFF:
                self.IMEM.update({f'{address - 0xA4001000}': f'{int(value)}'}) #self.IMEM.update({f'{address - 0xA4001000}': f'{int(value)}'})
                
            if 0xA4040010 <= address <= 0xA4040013:
                # SP_STATUS_REG

                self.rsp.cp0.registers.set('SP_STATUS_REG', value, address - 0xA4040010)
                
                if address - 0xA4040010 == 3:
                    if (value & 0b1000) != 0:
                        self.mi.clear_bit('MI_INTR_REG', 0)
                    if (value & 0b10000) != 0:
                        self.mi.set_bit('MI_INTR_REG', 0)
            if 0xA4080000 <= address <= 0xA4080003:
                # SP_PC_REG
                self.rsp.cp0.registers.set('SP_PC_REG', value, address - 0xA4080000)





            
        elif 0xA4100000 <= address <= 0xA41FFFFF:
            #DP Command Registers
            print('DP Reg')
            self.DPC.update({f'{address - 0xA4100000}': f'{value}'})
        elif 0xA4300000 <= address <= 0xA43FFFFF:
            # MIPS Interface

            if 0xA4300000 <= address <= 0xA4300003:
                self.mi.set('MI_INIT_MODE_REG', value, address - 0xA4300000)
            if 0xA4300004 <= address <= 0xA4300007:
                self.mi.set('MI_VERSION_REG', value, address - 0xA4300004)
            if 0xA4300008 <= address <= 0xA430000B:
                self.mi.set('MI_INTR_REG', value, address - 0xA4300008)
            if 0xA430000C <= address <= 0xA430000F:
                self.mi.set('MI_INTR_MASK_REG', value, address - 0xA430000C)


         
        elif 0xA4400000 <= address <= 0xA44FFFFF:
            # Video Interface
            if 0xa4400000 <= address <= 0xa4400003:
                self.VI.registers.set('vi_ctrl', value, address - 0xa4400000)
            elif 0xa4400004 <= address <= 0xa4400007:
                self.VI.registers.set('vi_origin/draw_addr_reg', value, address - 0xa4400004)
            elif 0xa4400008 <= address <= 0xa440000B:
                self.VI.registers.set('vi_width/h_width_reg', value, address - 0xa4400008)
            elif 0xa440000C <= address <= 0xa440000F:
                self.VI.registers.set('vi_v_intr', value, address - 0xa440000C)   
                if self.VI.registers._registers['vi_v_current_reg'] & 0x3FF == self.VI.registers._registers['vi_v_intr']:
                    self.mi.clear_bit('MI_INTR_REG', 3)
                    self.cp0.registers.clear_bit('cause', 10)
            elif 0xa4400010 <= address <= 0xa4400013:
                self.VI.registers.set('vi_v_current_reg', value, address - 0xa4400010)
                if self.VI.registers._registers['vi_v_current_reg'] & 0x3FF == self.VI.registers._registers['vi_v_intr']:
                    self.mi.clear_bit('MI_INTR_REG', 3)
                    self.cp0.registers.clear_bit('cause', 10)


            elif 0xa4400014 <= address <= 0xa4400017:
                self.VI.registers.set('vi_burst/timing_reg', value, address - 0xa4400014)
            elif 0xa4400018 <= address <= 0xa440001B:
                self.VI.registers.set('vi_v_sync_reg', value, address - 0xa4400018)
                self.VI.numHalflines = self.VI.registers._registers['vi_v_sync_reg'] >> 1
                



            elif 0xa440001C <= address <= 0xa440001F:
                self.VI.registers.set('vi_h_sync_reg', value, address - 0xa440001C)            
            elif 0xa4400020 <= address <= 0xa4400023:
                self.VI.registers.set('vi_leap/h_sync_leap_reg', value, address - 0xa4400020)  
            elif 0xa4400024 <= address <= 0xa4400027:
                self.VI.registers.set('vi_h_start/h_video_reg', value, address - 0xa4400024)  
                #self.VI.draw = True
               
                


            elif 0xa4400028 <= address <= 0xa440002B:
                self.VI.registers.set('vi_v_start/v_video_reg', value, address - 0xa4400028)  
            elif 0xa440002C <= address <= 0xa440002F:
                self.VI.registers.set('vi_v_burst_reg', value, address - 0xa440002C) 
            elif 0xa4400030 <= address <= 0xa4400033:
                self.VI.registers.set('vi_x_scale_reg', value, address - 0xa4400030) 
            elif 0xa4400034 <= address <= 0xa4400037:
                self.VI.registers.set('vi_y_scale_reg', value, address - 0xa4400034) 
            else:
                return 0

        elif 0xA4600000 <= address <= 0xA46FFFFF:
            if 0xA4600000 <= address <= 0xA4600003:
                self.PI.set('PI_DRAM_ADDR_REG', value, address - 0xA4600000) 
            if 0xA4600004 <= address <= 0xA4600007:
                self.PI.set('PI_CART_ADDR_REG', value, address - 0xA4600004) 
            if 0xA4600008 <= address <= 0xA460000B:
                self.PI.set('PI_RD_LEN_REG', value, address - 0xA4600008) 




            if 0xA460000C <= address <= 0xA460000F:
                self.PI.set('PI_WR_LEN_REG', value, address - 0xA460000C) 
                
            if 0xA4600010 <= address <= 0xA4600013:
                self.PI.set('PI_STATUS_REG', value, address - 0xA4600010) 
            if 0xA4600014 <= address <= 0xA4600017:
                self.PI.set('PI_BSD_DOM1_LAT_REG', value, address - 0xA4600014) 
            if 0xA4600018 <= address <= 0xA460001B:
                self.PI.set('PI_BSD_DOM1_PWD_REG', value, address - 0xA4600018) 
            if 0xA460001C <= address <= 0xA460001F:
                self.PI.set('PI_BSD_DOM1_PGS_REG', value, address - 0xA460001C) 
            if 0xA4600020 <= address <= 0xA4600023:
                self.PI.set('PI_BSD_DOM1_RLS_REG', value, address - 0xA4600020) 
            if 0xA4600024 <= address <= 0xA4600027:
                self.PI.set('PI_BSD_DOM2_LAT_REG', value, address - 0xA4600024) 
            if 0xA4600028 <= address <= 0xA460002B:
                self.PI.set('PI_BSD_DOM2_PWD_REG', value, address - 0xA4600028) 
            if 0xA460002C <= address <= 0xA460002F:
                self.PI.set('PI_BSD_DOM2_PGS_REG', value, address - 0xA460002C) 
            if 0xA4600030 <= address <= 0xA4600033:
                self.PI.set('PI_BSD_DOM2_RLS_REG', value, address - 0xA4600030) 
        elif 0xA4500000 <= address <= 0xA45FFFFF:
            self.AI.update({f'{address - 0xA4500000}': f'{value}'})     
        elif 0xA4700000 <= address <= 0xA48FFFFF:
            # RDRAM Interface
            if 0xA4700000 <= address <= 0xA4700003:
                self.ri.set('ri_mode_reg', value, address - 0xA4700000)
            if 0xA4700004 <= address <= 0xA4700007:
                self.ri.set('ri_config_reg', value, address - 0xA4700004)
            if 0xA4700008 <= address <= 0xA470000B:
                self.ri.set('ri_current_load_reg', value, address - 0xA4700008)
            if 0xA470000C <= address <= 0xA470000F:
                self.ri.set('ri_select_reg', value, address - 0xA470000C)
            if 0xA4700010 <= address <= 0xA4700013:
                self.ri.set('ri_refresh/count_reg', value, address - 0xA4700010)
            if 0xA4700014 <= address <= 0xA4700017:
                self.ri.set('ri_latency_reg', value, address - 0xA4700014)
            if 0xA4700018 <= address <= 0xA470001B:
                self.ri.set('ri_rerror_reg', value, address - 0xA4700018)
            if 0xA470001C <= address <= 0xA470001F:
                self.ri.set('ri_rerror_reg', value, address - 0xA470001C)


            if 0xa4800000 <= address <= 0xa480001C:
                # Serial Interface
                if 0xa4800000 <= address <= 0xa4800003:
                    self.si.set('SI_DRAM_ADDR_REG',value, address - 0xa4800000)
                if 0xa4800004 <= address <= 0xa4800007:
                    self.si.set('SI_PIF_ADDR_RD64B_REG',value, address - 0xa4800004)
    
                    print("DMA transfer, PIF_RAM to RDRAM")
                    print(value)
                    if address - 0xa4800007 == 3:
                        rdrampos = self.si.get("SI_DRAM_ADDR_REG") 
                        for i in range(511):
                            self.write(rdrampos+i, self.si.get_pif_ram(i))
                        
                        self.mi.set('MI_INTR_REG', (self.mi.get("MI_INTR_REG") & 0xFF) | 0b10, 0)
                        
            
              
                if 0xa4800010 <= address <= 0xa4800013:
                    self.si.set('SI_PIF_ADDR_WR64B_REG',value, address - 0xa4800010)
                    print("DMA transfer, RDRAM to PIF RAM")
                    print(value)
                    if address - 0xa4800010 == 3:
                        block = {}
                        rdrampos = self.si.get("SI_DRAM_ADDR_REG")
                        for i in range(511):
                            block.update({f'{i}': f'{self.read(rdrampos+i)}'})
                        
                        self.si.overwrite_pif_ram(block)
                        self.mi.set_bit('MI_INTR_REG', 0b10)
                if 0xa4800018 <= address <= 0xa480001B:
                    self.mi.clear_bit('MI_INTR_REG', 0b10)
                    self.si.clear_bit('SI_STATUS_REG', 0x1000)
                #return 0
       
          


        elif 0x10000000  <= address <= 0x1FBFFFFF:
            #Cartridge Domain 1 Address 2
            None



        elif 0x80000000  <= address <= 0x803FFFFF:
            #RDRAM Cached
          
            self.RDRAM.update({f'{address - 0x80000000}': f'{value}'})
            #self.rom.write(address - 0x80000000, value)
        elif 0xA0000000  <= address <= 0xA0800000:
            #RDRAM Uncached
            self.RDRAM.update({f'{address - 0xA0000000}': f'{value}'})
        elif 0xB0000000 <= address <= 0xBFCFFFFF:            

            None
           #self.rom.read(address - 0xB0000000)#self.RDRAM.update({f'{address - 0xB0000000}': f'{value}'})

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
            "s8": 0,
            "ra": 0,
        }

        self.special_registers = {
            "HI": 0,
            "LO": 0,
        }
       
    def set(self, register_name, value):
        try:
            if value == None:
                None
            if value == 0x51465920:
                None
            if register_name != "zr":
                self._registers[register_name] = value



        except:
            self.special_registers[register_name] = value
    def get(self, register_name):

        try:
            return self._registers[register_name]
        except:
            return self.special_registers[register_name]









class CPU:

    def __init__(self, registers, memory, program_counter: int, cop0):
        self.registers = registers
        self.memory = memory
        self.program_counter = program_counter
        
        self.cp0 = cop0
        self.cp1 = CP1(CP1_Registers())
        self.op = 0
    

    

    def decode(self, instruction):
        FetchAndDecode(self, instruction)
   
    
    def fetch(self):
    

        value = f'0x{self.memory.read(self.program_counter):02x}{self.memory.read(self.program_counter+1):02x}{self.memory.read(self.program_counter+2):02x}{self.memory.read(self.program_counter+3):02x}'
        self.program_counter += 4
        
        return value

    def store(self, address, value):
        if address < 0:
            address = int(address & 0xFFFF_FFFF)

        if str(value) == "0x-5bffeab0":
            None
        if address == int(0x803672D0) and value == 0:
            None
        #print(f'store: {hex(address)}, {value}')
        
        if value == 0x51465920:
            None
        if address == 2751471260:
            None
        if address == -1543496036:
            None        
        self.memory.write(address, (value >> 24) & 0xFF)
        self.memory.write(address+1, (value >> 16) & 0xFF)
        self.memory.write(address+2, (value >> 8) & 0xFF)
        self.memory.write(address+3, value & 0xFF)
    def store_u8(self, address, value):
        if address < 0:
            address = int(address & 0xFFFF_FFFF)

        if str(value) == "0x-5bffeab0":
            None
        if address == int(0x803672D0) and value == 0:
            None
        #print(f'store: {hex(address)}, {value}')
        
        if address == 2150868800:
            None   
        if address == 2150848936:
            None        
        if address == 2150865598:
            None
       
        self.memory.write(address, value & 0xFF)
    def store_u16(self, address, value):
        if address < 0:
            address = int(address & 0xFFFF_FFFF)

        if str(value) == "0x-5bffeab0":
            None
        if address == int(0x803672D0) and value == 0:
            None
        #print(f'store: {hex(address)}, {value}')
        
        if address == 2150868800:
            None   
        if value == 178913280:
            None
        if address == 2150865598:
            None       
        self.memory.write(address, (value >> 8) & 0xFF)
        self.memory.write(address+1, (value & 0xFF))
    def store_u64(self, address, value):
        if address < 0:
            address = int(address & 0xFFFF_FFFF)

        if str(value) == "0x-5bffeab0":
            None
        if address == int(0x803672D0) and value == 0:
            None
        #print(f'store: {hex(address)}, {value}')
        
        if address == 2150868800:
            None   
        if address == 2150848936:
            None      
        if value == 178913280:
            None
        self.memory.write(address, (value >> 56) & 0xFF)
        self.memory.write(address+1, (value >> 48) & 0xFF)
        self.memory.write(address+2, (value >> 40) & 0xFF)
        self.memory.write(address+3, (value >> 32) & 0xFF)
        self.memory.write(address+4, (value >> 24) & 0xFF)
        self.memory.write(address+5, (value >> 16) & 0xFF)
        self.memory.write(address+6, (value >> 8) & 0xFF)
        self.memory.write(address+7, value & 0xFF)
    
    def load(self,address):
     
        address = int(address &  0xFFFF_FFFF)
        #print(f'address: {address}')
        value = (int(self.memory.read(address)) << 24) | (int(self.memory.read(address+1)) << 16) | (int(self.memory.read(address+2)) << 8) | (int(self.memory.read(address+3)))

        if address == 0xB0000010:
            None
        #print(f'value: {value}')
        return sign_extend(value & 0xFFFF_FFFF,32)
    def load_u(self,address):
     
        address = int(address &  0xFFFF_FFFF)
        #print(f'address: {address}')
        value = (int(self.memory.read(address)) << 24) | (int(self.memory.read(address+1)) << 16) | (int(self.memory.read(address+2)) << 8) | (int(self.memory.read(address+3)))
        print(value)
   
        if address == 0xB0000010:
            None
        #print(f'value: {value}')
        return value & 0xFFFF_FFFF
    def load_s8(self,address):
        if address < 0:
            address = int(address &  0xFFFF_FFFF)
        #print(f'address: {address}')
        
        value = self.memory.read(address)
        print(value)

        #print(f'value: {value}')
        return sign_extend(value & 0xFF,8)

    def load_u8(self,address):
        if address < 0:
            address = int(address &  0xFFFF_FFFF)
        #print(f'address: {address}')
        

        value = int(self.memory.read(address))
        print(value)
        if address == 0xB0000010:
            None

        #print(f'value: {value}')
        return value & 0xFF

    def load_s16(self,address):
        if address < 0:
            address = int(address &  0xFFFF_FFFF)
        #print(f'address: {address}')

        value = (self.memory.read(address) << 8) | self.memory.read(address+1)
        print(value)
        if address == 0xB0000010:
            None
        #print(f'value: {value}')
        return sign_extend(value & 0xFFFF, 16)
    
    def load_u16(self,address):
        if address < 0:
            address = int(address &  0xFFFF_FFFF)
        #print(f'address: {address}')
        value = (self.memory.read(address) << 8) | self.memory.read(address+1)
        print(value)
        if address == 0xB0000010:
            None
 
        #print(f'value: {value}')
        return value & 0xFFFF
    
    def load_u64(self,address):
        if address < 0:
            address = int(address &  0xFFFF_FFFF)
        #print(f'address: {address}')
        value = (self.memory.read(address) << 56) | (self.memory.read(address+1) << 48) | (self.memory.read(address+2) << 40) | (self.memory.read(address+3) << 32) | (self.memory.read(address+4) << 24) | (self.memory.read(address+5) << 16) | (self.memory.read(address+6) << 8) | (self.memory.read(address+7))
        print(value)
        if address == 0xB0000010:
            None
        #print(f'value: {value}')
        return value & 0xFFFF_FFFF_FFFF_FFFF
    
    def load_s64(self,address):
        if address < 0:
            address = int(address &  0xFFFF_FFFF)
        #print(f'address: {address}')
        value = (self.memory.read(address) << 56) | (self.memory.read(address+1) << 48) | (self.memory.read(address+2) << 40) | (self.memory.read(address+3) << 32) | (self.memory.read(address+4) << 24) | (self.memory.read(address+5) << 16) | (self.memory.read(address+6) << 8) | (self.memory.read(address+7))
        print(value)
        if address == 0xB0000010:
            None
        #print(f'value: {value}')
        return sign_extend(value & 0xFFFF_FFFF_FFFF_FFFF,64)
    
    def set_pc(self, value):
        self.program_counter = value

    def get_pc(self):
        return int(self.program_counter) 

    def increase_op(self):
        self.op += 1
    def get_op(self):
        return self.op

    def execute_next_instruction(self, cpu, pc):


        value = int(f'0x{self.memory.read(self.program_counter):02x}{self.memory.read(self.program_counter+1):02x}{self.memory.read(self.program_counter+2):02x}{self.memory.read(self.program_counter+3):02x}',16)
        print("executing: ", value)
        #print(f'pc: {hex(self.get_pc())}, instruction: 0x{value:08x}')
        return f'{value:08x}'        
    




















