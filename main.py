







from PyN64 import cpu
from PyN64.cpu import CPU
from PyN64.cpu import Memory
from PyN64.rom import ROM
from PyN64.instruction import ADD
from PyN64.instruction_decoding import FetchAndDecode

import sys




def run(data):
    memory = Memory()
    
    
    
    b = b""
    print("[INFO] Reading addresses")
#    for i in range(0x0000, 0x00EF):
#        b += bytes([memory.read(i)])
    #print(b)
    

    
    

def main():
    memory = Memory()
    args = sys.argv
    if len(args) < 2:
        filename_arg = f"64ddipl.bin"
    elif len(args) == 2:
        filename_arg = args[1]
    with open(filename_arg, "rb") as file:
        cartridge_data = bytes(file.read())
        
        print(f"Loaded game ROM ({len(cartridge_data)} bytes)")
        for byte in cartridge_data:
            #print(byte)
            #print(hex(byte))
            
            memory.read(byte)
            FetchAndDecode(byte)
    run(bytes(cartridge_data))
#    try:
#        while 0 < 1:
#            None
#    except Exception as e:
#        raise e
    



if __name__ == "__main__":
    main()






















