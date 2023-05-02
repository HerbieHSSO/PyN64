







from PyN64.CPU import cpu
from PyN64.CPU.cpu import CPU
from PyN64.CPU.cpu import Registers
from PyN64.CPU.cpu import Memory
from PyN64.rom import ROM
from PyN64.RSP import *
from PyN64.RSP.rsp import RSP
from PyN64.RDP.rdp import RDP
from PyN64.RDP import *
from PyN64.CPU.instruction import ADD
from PyN64.CPU.instruction_decoding import FetchAndDecode
from PyN64.RSP.decode import FetchAndDecodeRSP


import sys
import keyboard
import time
import multiprocessing as mp
from multiprocessing import Process, Queue
from datetime import timedelta
import traceback

import dis


    
def BOOT(cpu, rom):

    dmem = {}
   
    for i in range(0x40, 0x1000, 4):
        dmem.update({f'{i}' : f'{rom.read(i):02x}{rom.read(i+1):02x}{rom.read(i+2):02x}{rom.read(i+3):02x}'})
    
    
    cpu.memory.overwrite('DMEM', dmem)



    del dmem

    


    
    cpu.set_pc(0xA4000040)
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
    cpu.cp0.registers.set('cause', 0x34000000)
    cpu.cp0.registers.set('count', 0x34000000)


def debug(q):

    
    while True:
       
        print(q.get())        

def main(q):
    
    args = sys.argv
    if len(args) < 2:
        filename_arg = f"Super Mario 64 (USA).z64"
    elif len(args) == 2:
        filename_arg = args[1]

    with open(filename_arg, "rb") as file:
        cartridge_data = list(file.read())
        
        #q.put(f"Loaded game ROM {len(cartridge_data)} bytes")
        print(f"Loaded game ROM {len(cartridge_data)} bytes")


    ram_data = [0] * (8192 * 1024)

    rom = ROM(cartridge_data, ram_data)
   
    rsp = RSP()
    #rdp = RDP()
    memory = Memory(rom, rdp, rsp)
    registers = Registers()
    cpu = CPU(registers, memory,  0)

    
    BOOT(cpu, rom)


    
    #rdp.set_title(f'{rom.getImageName()} -  {rom.getCountry()} Version')



    

    i = 0
    start = time.time()
    while True:

        "80327EA8 ERET"

        i += 1
    
        try:
            #print(f'pc: {hex(cpu.get_pc())}, ', end="")
            start_time = time.time()

            fetch = cpu.fetch() 

            #print('pc: ', hex(cpu.get_pc()))    
            if hex(cpu.get_pc()) == hex(0x80323948):
                print(hex(cpu.get_pc()))
                None

            
                
            #print(f'instruction: {fetch}, ', end="")
            decode = cpu.decode(fetch)

            #print(f'op: {cpu.get_op()}, ', end="")EZ
            #print(f'time: {time.time() - start_time}')

            #q.put(f'pc: {hex(cpu.get_pc())}, instruction: {fetch}, op: {i}, time: {time.time() - start_time}')
            #print(f'pc: {hex(cpu.get_pc())}, instruction: {fetch}, op: {i}, time: {time.time() - start_time}')
       
               #rdp.draw()
        except Exception as e:
            print(f'An Error Occurred: {e}, pc: {hex(cpu.get_pc())} asm: {fetch} op: {cpu.get_op()}, {traceback.format_exc()}')
            break
    print(time.time() - start)


    #quit()






if __name__ == "__main__":

    main("q")
    """
    q = Queue()
    debugger = Process(target=debug, args=(q,))
    worker = Process(target=main, args=(q,))
    
    worker.start()
    debugger.start()
    
    """






















