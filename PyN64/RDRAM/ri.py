



class Registers:
    def __init__(self):

        self._registers = {
            "current_control": 0,
            "ri_select_reg": 1
        }








    def set(self, register_name, value):
        self._registers[register_name] = value


    def get(self, register_name):
        try:
            return self._registers[register_name]
        except:
            return 0
























