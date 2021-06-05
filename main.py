







from PyN64 import cpu
from PyN64.cpu import CPU
from PyN64.cpu import Memory
from PyN64.rom import ROM
from PyN64.instruction import ADD

import sys




def run():
    memory = Memory()
    
    cpu.program_counter = 0x40
    
    b = b""
    print("[INFO] Reading addresses")
    for i in range(0x0000, 0x00EF):
        b += bytes([memory.read(i)])
    print(b)
    header = ROM.parse(b)
    print(cpu.program_counter)
    ADD.execute()

def main():
    args = sys.argv
    if len(args) < 2:
        filename_arg = f"Super Mario 64 (USA).n64"
    elif len(args) == 2:
        filename_arg = args[1]
    with open(filename_arg, "rb") as file:
        cartridge_data = list(file.read())
        
        print(f"Loaded game ROM ({len(cartridge_data)} bytes)")
    run()
    try:
        while 0 < 1:
            None
    except Exception as e:
        raise e
    



if __name__ == "__main__":
    main()






















