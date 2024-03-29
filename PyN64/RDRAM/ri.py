



class Registers:
    def __init__(self):

        self._registers = {
            "ri_mode_reg": 0,
            "ri_config_reg": 0,
            "ri_current_load_reg": 0,
            "ri_select_reg": 0,
            "ri_refresh/count_reg": 0,
            "ri_latency_reg": 0,
            "ri_rerror_reg": 0,
            "ri_werror_reg": 0,
        }








    def set(self, register_name, value, offset):
     

        byte1 = (self._registers[register_name] >> 24) & 0xFF
        byte2 = (self._registers[register_name] >> 16) & 0xFF
        byte3 = (self._registers[register_name] >> 8) & 0xFF
        byte4 = self._registers[register_name] & 0xFF  
        if offset == 0:
            self._registers[register_name] =  (value << 24) | (byte2 << 16) | (byte3 << 8) | byte4
        if offset == 1:
            self._registers[register_name] =  (byte1 << 24) | (value << 16) | (byte3 << 8) | byte4
        if offset == 2:
            self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (value << 8) | byte4
        if offset == 3:
            self._registers[register_name] =  (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | value

    def get(self, register_name):
   
        return self._registers[register_name]

























