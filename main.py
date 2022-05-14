







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
import win32api, win32con, win32process

import sys
from timeit import default_timer as timer
from multiprocessing import Process, Queue
from datetime import timedelta
import traceback




def analysis(value):
    value = hex(value)

    val = str(value).replace('0x','')
    if len(val) == 1:
        value = f'0x0{val}'
    return str(value).replace('0x', '')

    
def BOOT(cpu, rom):

    dmem = {}
   
    for i in range(0x40, 0x1000):
        dmem.update({f'{i}' : f'{rom.read(i)}'})
    
    
    cpu.memory.overwrite('DMEM', dmem)



    del dmem

    


    
    cpu.set_pc(0xA4000040)
    cpu.registers.set('at', 1)
    cpu.registers.set('v0', 247309622)
    cpu.registers.set('v1', 247309622)
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
    cpu.registers.set('s6', 63)
    cpu.registers.set('t8', 3)
    cpu.registers.set('t9', -1645497009)
    cpu.registers.set('sp', -1543495696)
    cpu.registers.set('ra', -1543498416)


def debug(q):
    i = 0
    while True:
        i += 1
        print(q.get(), i)        

def main(q):
    
    args = sys.argv
    if len(args) < 2:
        filename_arg = f"Super Mario 64 (USA).z64"
    elif len(args) == 2:
        filename_arg = args[1]
    with open(filename_arg, "rb") as file:
        cartridge_data = list(file.read())
        
        q.put(f"Loaded game ROM ({len(cartridge_data)} bytes)")

    with open("pifdata.bin", "rb") as bootfile:
        pifdata = list(bootfile.read())

        q.put(f"Loaded boot ROM ({len(pifdata)}) bytes")

    ram_data = [0] * (8192 * 1024)

    rom = ROM(cartridge_data, ram_data)
   
    rsp = RSP()
    #rdp = RDP()
    memory = Memory(rom, rdp, rsp)
    registers = Registers()
    cpu = CPU(registers, memory,  0)

    
    BOOT(cpu, rom)


    
    #rdp.set_title(f'{rom.getImageName()} -  {rom.getCountry()} Version')

    
    

    
    pid  = win32api.GetCurrentProcessId()
    mask = 1 # core 7
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetProcessAffinityMask(handle, mask)
    
    for i in range(99999999999):
        
        start = timer()
    
        try:
            
            fetch = cpu.fetch()
            
            decode = cpu.decode(fetch)
            q.put(f'pc: {hex(cpu.get_pc())}, {fetch}, time: {timedelta(seconds=timer()-start)}')
        except Exception as e:
            q.put(f'An Error Occurred: {e}, pc: {hex(cpu.get_pc())} asm: {fetch} {traceback.format_exc()}')
            break
       
               #rdp.draw()











if __name__ == "__main__":


    q = Queue()
    debugger = Process(target=debug, args=(q,))
    worker = Process(target=main, args=(q,))
    
    worker.start()
    debugger.start()
    






















