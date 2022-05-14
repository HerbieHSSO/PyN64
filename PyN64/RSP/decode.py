

VREG_NAMES = [
    "v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10", "v11", "v12", "v13", "v14", "v15",
    "v16", "v17", "v18", "v19", "v20", "v21", "v22", "v23", "v24", "v25", "v26", "v27", "v28", "v29",
    "v30", "v31",
];

REG_NAMES = [
    "zr", "at", "v0", "v1", "a0", "a1", "a2", "a3", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
    "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t8", "t9", "k0", "k1", "gp", "sp", "fp", "ra",
    "hi", "lo",
];




def analysis(value):
    value = hex(value)

    val = str(value).replace('0x','')
    if len(val) == 1:
        value = f'0x0{val}'
    return str(value).replace('0x', '')




def FetchAndDecodeRSP(instruction):

    instruction = int(instruction, 16)

    opcode = (instruction & 0b11111100000000000000000000000000) >> 26
    func = opcode & 0x3F
    e = (opcode >> 21) & 0xF
    rsx = (opcode >> 11) & 0x1f
    rdx = (opcode >> 6) & 0x1f

    grt = REG_NAMES[(opcode >> 16) & 0x1f]
    
    vrs = VREG_NAMES[(opcode >> 11) & 0x1f]
    vrt = VREG_NAMES[(opcode >> 16) & 0x1f]
    vrd = VREG_NAMES[(opcode >> 6) & 0x1f]
    

    if opcode == 0x12:
        if opcode & (1 << 25) != 0:
            if func == 0x00:
                print(f'vmulf {vrd} {vrs} {vrt}')
            if func == 0x01:
                print(f'vmulu {vrd} {vrs} {vrt}')
            if func == 0x02:
                print(f'vmudl {vrd} {vrs} {vrt}')
            if func == 0x03:
                print(f'vmudm {vrd} {vrs} {vrt}')







    


