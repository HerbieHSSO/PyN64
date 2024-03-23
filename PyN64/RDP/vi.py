



class Registers:
    def __init__(self):

        self._registers = {
            "vi_status/control_reg": 0,
            "vi_origin/draw_addr_reg": 0,
            "vi_width/h_width_reg": 0,
            "vi_intr/v_width_reg": 0,
            "vi_current/current_line_reg": 0,
            "vi_burst/timing_reg": 0,
            "vi_v_sync_reg": 0,
            "vi_h_sync_reg": 0,
            "vi_leap/h_sync_leap_reg": 0,
            "vi_h_start/h_video_reg": 0,
            "vi_v_start/v_video_reg": 0,
            "vi_v_burst_reg": 0,
            "vi_x_scale_reg": 0,
            "vi_y_scale_reg": 0,
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

        if register_name == 'vi_status/control_reg':
            self._registers[register_name] = self._registers[register_name] & 0xFFFF
        if register_name == 'vi_origin/draw_addr_reg':
            self._registers[register_name] = self._registers[register_name] & 0xFFFF_FF
        if register_name == 'vi_width/h_width_reg':
            self._registers[register_name] = self._registers[register_name] & 0xFFF
        if register_name == 'vi_intr/v_width_reg':
            self._registers[register_name] = self._registers[register_name] & 0x3FF       
        if register_name == 'vi_current/current_line_reg':
            self._registers[register_name] = self._registers[register_name] & 0x3FFF_FFFF
        if register_name == 'vi_burst/timing_reg':
            self._registers[register_name] = self._registers[register_name] & 0x3FF 
        if register_name == 'vi_v_sync_reg':
            self._registers[register_name] = self._registers[register_name] & 0x3FF 
        if register_name == 'vi_h_sync_reg':
            self._registers[register_name] = self._registers[register_name] & 0x1FFFFF 
        if register_name == 'vi_leap/h_sync_leap_reg':
            self._registers[register_name] = self._registers[register_name] & 0xFFFFFFF
        if register_name == 'vi_h_start/h_video_reg':
            self._registers[register_name] = self._registers[register_name] & 0x3FFFFFF
        if register_name == 'vi_v_start/v_video_reg':
            self._registers[register_name] = self._registers[register_name] & 0x3FFFFFF
        if register_name == 'vi_v_burst_reg':
            self._registers[register_name] = self._registers[register_name] & 0x3FFFFFF
        if register_name == 'vi_x_scale_reg':
            self._registers[register_name] = self._registers[register_name] & 0xFFFFFFF
        if register_name == 'vi_y_scale_reg':
            self._registers[register_name] = self._registers[register_name] & 0xFFFFFFF


    def get(self, register_name, offset):
        byte1 = (self._registers[register_name] >> 24) & 0xFF
        byte2 = (self._registers[register_name] >> 16) & 0xFF
        byte3 = (self._registers[register_name] >> 8) & 0xFF
        byte4 = self._registers[register_name] & 0xFF  
        if offset == 0:
            return byte1
        if offset == 1:
            return byte2
        if offset == 2:
            return byte3
        if offset == 3:
            return byte4


























