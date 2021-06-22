




from PyN64.cpu import CPU
from PyN64.instruction import Reg, ADD
from PyN64 import cpu
from PyN64.cpu import Memory

T0 = Reg('T0')


OPCODE_TABLE = {
    0x20: ADD(T0, T0, 4),
    }



def FetchAndDecode(PC):
    Cpu = CPU(Memory, PC)
    opcode = Cpu.load()
    print(opcode)

    if opcode in list(OPCODE_TABLE):
        return print(OPCODE_TABLE[opcode])



















