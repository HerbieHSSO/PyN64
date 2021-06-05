

class Memory:
    def __init__(self):
        self.internal_ram = [0] * 0x2000
        self._high_internal_ram = [0] * 127

    def read(self, address):
        return address
    def write(self, address, value):
        if address < 0:
            raise ValueError(f"Trying to write negative address {address} (value:{value})")
        if value is None:
            raise ValueError(f"Trying to write None to {hex(address)}")
class CPU:
    def __init__(self, memory: Memory, program_counter: int):
        self.registers = Registers()
        self.memory = memory
    def load(self):
        value = self.memory.read(self.program_counter)
        self.program_counter += 1
        return value
class Registers:
    def __init__(self):
        
        self.stack_pointer = 0xa4000040
        self._registers = {
            "ZERO": 0,
            "AT": 0,
            "V0": 0,
            "V1": 0,
            "A0": 0,
            "A1": 0,
            "A2": 0,
            "A3": 0,
            "T0": 0,
            "T1": 0,
            "T2": 0,
            "T3": 0,
            "T4": 0,
            "T5": 0,
            "T6": 0,
            "T7": 0,
            "S0": 0,
            "S1": 0,
            "S2": 0,
            "S3": 0,
            "S4": 0,
            "S5": 0,
            "S6": 0,
            "S7": 0,
            "T8": 0,
            "T9": 0,
            "K0": 0,
            "K1": 0,
            "GP": 0,
            "SP": 0,
            "FP": 0,
            "RA": 0,
        }

    def set(self, register_name, value):
        if register_name == "SP":
            self.stack_pointer = value
            return
        self._registers[register_name] = value

    def get(self, register_name):
        if register_name == "SP":
            return self.stack_pointer
        return self._registers[register_name]
    def decrement(self, register_name):
        self.set(register_name, self.get(register_name) - 1)
    def increment(self, register_name):
        self.set(register_name, self.get(register_name) + 1)
    def set_bit(self, register_name, bit, value):
        if value:
            self._registers[register_name] = self._registers[register_name] | (1 << bit)
        else:
            self._registers[register_name] = self._registers[register_name] & ~(1 << bit)
    def get_bit(self, register_name, bit) -> bool:
        return bool(self._registers[register_name] & (1 << bit))





























