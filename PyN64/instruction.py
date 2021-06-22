from PyN64 import cpu
from PyN64.cpu import Registers
from PyN64.cpu import Memory
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Reg:
    register: str
    def read(self, registers: Registers):
        return registers.get(self.register)
    def write(self, registers: Registers, value: int):
        registes.set(self.register, value)

@dataclass
class Instruction:
    cycles = 1

    def execute(self, registers: Registers):
        raise Exception("Not implemented")
@dataclass
class Addr:
    address: int

    def read(self, memory: Memory) -> int:
        return memory.read(self.address)

    def write(self, memory: Memory, value: int):
        memory.write(self.address, value)


@dataclass
class ADD:
    """ ADD """
    destination: Any
    n: Any
    cycles: int
    def execute(self, registers: Registers):
        target = self.destination.read(registers)
        value = self.n.read(registers)
        result = self.destination + self.n
        self.destination.write(registers, result)
        

































