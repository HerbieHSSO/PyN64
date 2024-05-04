
import pandas as pd
from PIL import Image,ImageTk



from PyN64.RDP import display
import tkinter as tk

class VideoInterface:
    def __init__(self):

        self.registers = Registers()



        self.screen_width = 640
        self.screen_height = 480
        
        self.buffer32bpp = [0] * (self.screen_width * self.screen_height * 4)

        self.numHalflines = 240
        self.cyclesPerHalfline = 1000
        self.currentHalflines = 0
        # Output resolution
        self.outWidth = 640
        self.outHeight = 480

        # Input resulution
        self.inPitch = 320
        self.inWidth = 320
        self.inHeight = 240

        self.interlaced = False
        self.field = 0
       
        self.xSubpixel = 0
        self.ySubpixel = 0
        self.xScale = 0x200
        self.yScale = 0x400

  
        self.sx0 = 0
        self.sy0 = 0

    
        self.dx0 = 0
        self.dy0 = 0

        self.hScanMin = 108
        self.hScanMax = self.hScanMin + self.screen_width

        self.vScanMin = 34
        self.vScanMax = self.vScanMin + self.screen_height




        self.draw = False


    def render(self, memory):
        self.xSubpixel = self.registers._registers['vi_x_scale_reg'] >> 16 & 4095
        self.ySubpixel = self.registers._registers['vi_y_scale_reg'] >> 16 & 4095
        self.xScale = 1024
        self.yScale = 2048

        hStart = self.registers._registers['vi_h_start/h_video_reg'] >> 16 & 1023
        hEnd = self.registers._registers['vi_h_start/h_video_reg'] & 1023

        x0 = max(hStart, self.hScanMin)
        x1 = max(hEnd, self.hScanMax)

        vStart = (self.registers._registers['vi_v_start/v_video_reg'] >> 16) & 0x03FF
        vEnd = self.registers._registers['vi_v_start/v_video_reg'] & 0x03FF

        y0 = max(vStart, self.vScanMin)
        if vEnd < vStart:
            y1 = self.vScanMax
        else:
            y1 = min(vEnd, self.vScanMax)

        if x0 >= self.hScanMin:
            x0 += 8
        if x1 < self.hScanMax:
            x1 -= 7
        
        if self.registers._registers['vi_ctrl'] & 0x40  != 0:
            self.interlaced = True
        else:
            self.interlaced = False


        self.xSubpixel = (self.registers._registers['vi_x_scale_reg'] >> 16) & 0xFFF
        self.ySubpixel = (self.registers._registers['vi_y_scale_reg'] >> 16) & 0xFFF

        self.xScale = self.registers._registers['vi_x_scale_reg'] & 0xFFF
        self.yScale = self.registers._registers['vi_y_scale_reg'] & 0xFFF

        self.sx0 = x0 - hStart
        self.sy0 = y0 - vStart


        self.dx0 = x0 - self.hScanMin
        self.dy0 = y0 - self.vScanMin

        self.outWidth = x1 - x0
        self.outHeight = y1 - y0

        self.inPitch = self.registers._registers['vi_width/h_width_reg'] 

        sEndX = ((self.sx0 + self.outWidth) * self.xScale) >> 10
        sEndY = ((self.sy0 + self.outHeight) * self.yScale) >> 11

        if (self.inPitch > 0x300 | self.inPitch >= (sEndX * 2)):
            vFudge = 2
        else:
            vFudge = 1


        self.inWidth = sEndX
        self.inHeight = sEndY * vFudge

        self.field ^= (1 if self.interlaced else 0)

        if (self.registers._registers["vi_ctrl"] & 0x3) == 0b00:
            # blank data
            return 
        
        if (self.registers._registers["vi_ctrl"] & 0x3) == 0b11:
            # 8/8/8/8 (32 bit color)

       

            bufferAddr = self.registers._registers["vi_origin/draw_addr_reg"] & 0xFF_FFFE
            buffer = self.buffer32bpp

            dstPitch = -self.screen_width

            dstRow = (self.screen_height - 1 - self.dy0) * self.screen_width

            alpha = 0xff

            sy = self.sy0 * self.yScale + self.ySubpixel; 

        
            for y in range(0, self.outHeight):
                if (not self.interlaced or ((self.dy0 + y) & 1) != self.field):

                    sourceOff = bufferAddr + ((sy >> 11) * self.inPitch * 4)
            
                    dstOff = dstRow + self.dx0
                    sx = self.sx0 * self.xScale + self.xSubpixel

        
                    for x in range(0, self.outWidth):
                    
                        #  pixel = memory.read(0x80000000 + sourceOff + (sx >> 10) * 4) | memory.read(0x80000000 + sourceOff + (sx >> 10) * 4 + 1) | memory.read(0x80000000 + sourceOff + (sx >> 10) * 4 + 2) | memory.read(0x80000000 + sourceOff + (sx >> 10) * 4 + 3)
            
                        pixel = (memory.read(0x80000000 + sourceOff + (sx >> 10) * 4) << 24)  | (memory.read(0x80000000 + 1 + sourceOff + (sx >> 10) * 4) << 16) | (memory.read(0x80000000 + 2 + sourceOff + (sx >> 10) * 4) << 8)| memory.read(0x80000000 + 3 + sourceOff + (sx >> 10) * 4)
                        
                        
                        buffer[dstOff * 4 + 0] = (pixel >> 24) & 0xFF
                        buffer[dstOff * 4 + 1] = (pixel >> 16) & 0xFF
                        buffer[dstOff * 4 + 2] = (pixel >> 8) & 0xFF
                        buffer[dstOff * 4 + 3] = alpha

                        dstOff += 1
                        sx += self.xScale
                sy += self.yScale
                dstRow += dstPitch
            #self.buffer32bpp = buffer
            pixels = [(buffer[i], buffer[i+1], buffer[i+2], buffer[i+3]) for i in range(0, len(buffer), 4)]
            #pixels = [value for rgba in self.buffer32bpp for value in self.buffer32bpp]
            img = Image.new('RGBA', (640, 480))
            img.putdata(pixels)
          
            img.save("saved_image.png")
            
            with open("buffer.txt", 'w') as f:
                for i in range(0, len(self.buffer32bpp)):
                    
                    f.write(f'{i}: {self.buffer32bpp[i]}\n')

            return img.transpose(Image.FLIP_TOP_BOTTOM)
            #self.display_image(img.transpose(Image.FLIP_TOP_BOTTOM))
            #display.main(pixels)

    def display_image(self, image):
        window = tk.Tk()
        window.title("PyN64")
  


      
        tk_image = ImageTk.PhotoImage(image)

     
        label = tk.Label(window, image=tk_image)
        label.pack()

  
        window.mainloop()        

          
    def get_framebuffer(self):
            return self.buffer32bpp

    
class Registers:
    def __init__(self):


        
        self._registers = {
            "vi_ctrl": 0,
            "vi_origin/draw_addr_reg": 0,
            "vi_width/h_width_reg": 0,
            "vi_v_intr": 0,
            "vi_v_current_reg": 0,
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

        if register_name == 'vi_ctrl':
            self._registers[register_name] = self._registers[register_name] & 0xFFFF
        if register_name == 'vi_origin/draw_addr_reg':
            self._registers[register_name] = self._registers[register_name] & 0xFFFF_FF
        if register_name == 'vi_width/h_width_reg':
            self._registers[register_name] = self._registers[register_name] & 0xFFF
        if register_name == 'vi_v_intr':
            self._registers[register_name] = self._registers[register_name] & 0x3FF       
        if register_name == 'vi_v_current_reg':
            self._registers[register_name] = self._registers[register_name] & 0x3FF
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

























