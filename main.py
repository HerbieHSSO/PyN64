







from PyN64.CPU import cpu
from PyN64.CPU.cpu import CPU
from PyN64.CPU.cp0 import *
from PyN64.CPU.cpu import Registers
from PyN64.CPU.cpu import Memory
from PyN64.rom import ROM
from PyN64.RSP import *
from PyN64.RSP.rsp import RSP
from PyN64.RDP.rdp import RDP
from PyN64.RDRAM.rdram import RDRAM
from PyN64.RDP import *
from PyN64.CPU.instruction import ADD
from PyN64.CPU.instruction_decoding import FetchAndDecode
from PyN64.RSP.decode import FetchAndDecodeRSP


import sys, os
import keyboard
import time
from PIL import Image, ImageTk
import tkinter as tk

import multiprocessing as mp

import traceback



class NullWriter(object):
    def write(self, text):
        pass
    
def BOOT(cpu, rom):

    dmem = {}
   
    for i in range(0x40, 0x1000, 1):
        dmem.update({f'{i}' : f'{rom.read(i):02x}'})
    
    
    cpu.memory.overwrite('DMEM', dmem)



    del dmem

  


    cpu.set_pc(0xA4000040)
    #cpu.set_pc(0xA4000040)
    cpu.registers.set('at', 1)
    cpu.registers.set('v0', 247309622)
    cpu.registers.set('v1', 247309622)
    cpu.registers.set('a0', 42294)
    cpu.registers.set('a1', -916884523)
    cpu.registers.set('a2', -1543495924)
    cpu.registers.set('a3', -1543495928)
    cpu.registers.set('t0', 192)
    cpu.registers.set('t2', 64)
    cpu.registers.set('t3', -1543503808)
    cpu.registers.set('t4', -317665101)
    cpu.registers.set('t5', 335717580)
    cpu.registers.set('t6', 608805734)
    cpu.registers.set('t7', 822337825)

    cpu.registers.set('s4', 1)
    cpu.registers.set('s6', 63)
    cpu.registers.set('t8', 3)
    cpu.registers.set('t9', -1645497009)
    cpu.registers.set('sp', -1543495696)
    
    cpu.registers.set('ra', -1543498416)
    

    cpu.cp0.registers.set('status', 0x34000000)
    cpu.cp0.registers.set('random', 0x1F)
    cpu.cp0.registers.set('config', 0x7006E463)
    cpu.cp0.registers.set('count', 0x5000)
    cpu.cp0.registers.set('cause', 0x5c)
    cpu.cp0.registers.set('context', 0x007FFFF0)
    cpu.cp0.registers.set('epc', 0xFFFFFFFF)
    cpu.cp0.registers.set('badvAddr', 0xFFFFFFFF)
    cpu.cp0.registers.set('errorepc', 0xFFFFFFFF)



    

   #FFFFFFFF803274FC




def debug(q):

    
    while True:
       
        print(q.get())        

def main(q):

    args = sys.argv
    if len(args) < 2:
        print("No n64 rom file provided.")
        #filename_arg = f"system-tests/CPULW.N64"
    elif len(args) == 2:
        filename_arg = args[1]

    with open(filename_arg, "rb") as file:
        cartridge_data = list(file.read())
        
        #q.put(f"Loaded game ROM {len(cartridge_data)} bytes")
        print(f"Loaded game ROM {len(cartridge_data)} bytes")


    ram_data = [0]

    rom = ROM(cartridge_data, ram_data)
   
    rsp = RSP()
    rdram = RDRAM()
    #rdp = RDP()

    coprocessor0 = CP0(CP0_Registers())
    memory = Memory(rom, rsp, rdp, rdram, coprocessor0)




    registers = Registers()
    cpu = CPU(registers, memory,  0, coprocessor0)
    
    
    BOOT(cpu, rom)

    image_queue = mp.Queue()

    display_process = mp.Process(target=display_image, args=(image_queue,))
    display_process.start()
    #rdp.set_title(f'{rom.getImageName()} -  {rom.getCountry()} Version')

    
    file_path = "saved_image.png"



    return_pc = 0
    i = 0

    
    start = time.time()
    while True:

        "80327EA8 ERET"

        i += 1
    
        try:
            #print(f'pc: {hex(cpu.get_pc())}, ', end="")


            #fetch_rsp = rsp.fetch(cpu.memory)
            #decode_rsp = rsp.decode(fetch_rsp)
      
            # MI ok; 



            fetch = cpu.fetch() 



            #print('pc: ', hex(cpu.get_pc()))     0xA4000AF0 0xA4000ACC 0x80322958 A4000040
            if hex(cpu.get_pc()) == hex(0x800013D4):
                print(hex(cpu.get_pc()))
                None


            """
            if hex(cpu.get_pc()) == hex(0x80327EA8):
                if return_pc == 0:
                    print(hex(cpu.get_pc()))
                    #rsp.set_halt(False)xxxxxxxx21x312
                    cpu.set_pc(0x80000180)
                    #cpu.set_pc(cpu.cp0.registers.get("epc") & 0xFFFF_FFFF) 0x803245A4
                    cpu.cp0.registers.set('epc', 0x80246DD8)
                    
                    cpu.cp0.registers.set('cause', 0x400)
                    #0x8032799cC

                    cpu.store(0xA4300008, 0xA)

                    fetch = cpu.fetch()
                    None
                    return_pc += 1                    
             
      
            """  
            if hex(cpu.get_pc()) == hex(0x80246ddc):
                print(hex(cpu.get_pc()))
                #rsp.set_halt(False)xxxxxxxx21x312
                cpu.set_pc(0x80000180)
                #cpu.set_pc(cpu.cp0.registers.get("epc") & 0xFFFF_FFFF) 0x803245A4
                cpu.cp0.registers.set('epc', 0x80246DD8)
                
                cpu.cp0.registers.set('cause', 0x400)
                #0x8032799cC
                fetch = cpu.fetch()
                None
            """
            if hex(cpu.get_pc()) == hex(0x803274fc):
                if return_pc == 1:
                    return_pc +=1 
                    print(hex(cpu.get_pc()))
                    cpu.set_pc(0x80000180) 
                    cpu.registers.set('LO', 0)
                    cpu.cp0.registers.set('cause', 1024)
                    cpu.cp0.registers.set('errorepc', 0xFFxxxxxxxFF_FFFF)
                    cpu.cp0.registers.set('epc', 0x803274FC)
                    fetch = cpu.fetch()
                  
                else:
                    return_pc +=1 
                """
               
                #0x8032w7d0c 0x803279    f8 80327808 0x800001F8
                #0x80246ddc 0x80327e88 0x80327 e88 0x80327e88  0x8032771c 0x803278d0
                #0x803276ec
                #178913280
            #print(f'instruction: {fetch}, ', end="")d
            decode = cpu.decode(fetch)

            if cpu.get_op() == 1000000:
                None
            if cpu.get_op() % 0x17D6C2 == 0:
                if cpu.memory.VI.currentHalflines < cpu.memory.VI.numHalflines:
                    cpu.memory.VI.registers._registers['vi_v_current_reg'] = (cpu.memory.VI.currentHalflines << 1)
                    cpu.memory.VI.currentHalflines  += 1
                    #image_queue.put(None)
             
                    cpu.memory.VI.render(cpu.memory)
                    image_queue.put(cpu.memory.VI.render(cpu.memory))
                    cpu.memory.VI.currentHalflines = 0
                
                if (cpu.memory.VI.registers._registers['vi_v_current_reg'] & 0x3FE) >= cpu.memory.VI.registers._registers['vi_v_intr']:
                        cpu.memory.mi.set_bit('MI_INTR_REG', 3)

                
            """
            if cpu.get_pc() == 0x80008DA0:
                input()
                cpu.memory.VI.render(cpu.memory)
            """
            #print(f'op: {cpu.get_op()}, ', end="")EZ
            #print(f'time: {time.time() - start_time}') 8031e290:

            #q.put(f'pc: {hex(cpu.get_pc())}, instruction: {fetch}, op: {i}, time: {time.time() - start_time}')
            #print(f'pc: {hex(cpu.get_pc())}, instruction: {fetch}, op: {i}, time: {time.time() - start_time}')
            #803237bc
               #rdp.draw()
            i += 1
        except Exception as e:
            print(f'An Error Occurred: {e}, pc: {hex(cpu.get_pc())} asm: {fetch} op: {cpu.get_op()}, {traceback.format_exc()}')
            break
    print(time.time() - start)


    #quit()


def display_image(image_queue):
    root = tk.Tk()
    root.title("PyN64")
    root.geometry("640x480")
    root.resizable(False, False)

    image_label = tk.Label(root)
    image_label.pack()
    

    def update_image():
        if image_queue.get() != None:
            image = image_queue.get()
            photo = ImageTk.PhotoImage(image)
            image_label.configure(image=photo)
            image_label.image = photo  
       
        root.update_idletasks()  
        root.after(100, update_image)  
    
    update_image()
    root.mainloop()




if __name__ == "__main__":





    main("q")
    """
    q = Queue()
    debugger = Process(target=debug, args=(q,))
    worker = Process(target=main, args=(q,))
    
    worker.start()
    debugger.start()
    
    
    worker.join()
    debugger.join()
    """




















