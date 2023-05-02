



class CP1:
    def __init__(self, registers):
        self.registers = registers







class CP1_Registers:
    def __init__(self):
        self._control = {
            "f0" : 0,
            "f1": 0,
            "f2": 0,
            "f3": 0,
            "f4": 0,
            "f5": 0,
            "f6": 0,
            "f7": 0,
            "f8": 0,
            "f9": 0,
            "f10": 0,
            "f11": 0,
            "f12": 0,
            "f13": 0,
            "f14": 0,
            "f15": 0,
            "f16": 0,
            "f17": 0,
            "f18": 0,
            "f19": 0,
            "f20": 0,
            "f21": 0,
            "f22": 0,
            "f23": 0,
            "f24": 0,
            "f25": 0,
            "f26": 0,
            "f27": 0,
            "f28": 0,
            "f29": 0,
            "f30": 0,
            "f31": 0,
        }
        self._value = {
            "f0" : 0,
            "f1": 0,
            "f2": 0,
            "f3": 0,
            "f4": 0,
            "f5": 0,
            "f6": 0,
            "f7": 0,
            "f8": 0,
            "f9": 0,
            "f10": 0,
            "f11": 0,
            "f12": 0,
            "f13": 0,
            "f14": 0,
            "f15": 0,
            "f16": 0,
            "f17": 0,
            "f18": 0,
            "f19": 0,
            "f20": 0,
            "f21": 0,
            "f22": 0,
            "f23": 0,
            "f24": 0,
            "f25": 0,
            "f26": 0,
            "f27": 0,
            "f28": 0,
            "f29": 0,
            "f30": 0,
            "f31": 0,
        }

    def set_control(self, register_name, value):
        self._control[register_name] = value
    def get_control(self, register_name):
        return self._control[register_name]
    def set_value(self, register_name, value):
        self._value[register_name] = value
    def get_value(self, register_name):
        return self._value[register_name]