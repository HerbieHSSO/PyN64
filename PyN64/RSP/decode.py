from PyN64.RSP.instruction import *
VREG_NAMES = [
    "v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10", "v11", "v12", "v13", "v14", "v15",
    "v16", "v17", "v18", "v19", "v20", "v21", "v22", "v23", "v24", "v25", "v26", "v27", "v28", "v29",
    "v30", "v31",
];

REG_NAMES = [
    "zr", "at", "v0", "v1", "a0", "a1", "a2", "a3", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
    "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t8", "t9", "k0", "k1", "gp", "sp", "fp", "ra",
];

CP0_REG_NAMES = [
    "SP_BASE_REG", "SP_MEM_ADDR_REG", "SP_DRAM_ADDR_REG", "SP_RD_LEN_REG","SP_WR_LEN_REG","SP_STATUS_REG","SP_DMA_FULL_REG",
    "SP_DMA_BUSY_REG","SP_SEMAPHORE_REG","SP_PC_REG","SP_IBIST_REG",
]

def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)


def analysis(value):
    value = hex(value)

    val = str(value).replace('0x','')
    if len(val) == 1:
        value = f'0x0{val}'
    return str(value).replace('0x', '')




def FetchAndDecodeRSP(rsp, instruction):

    pc = rsp.get_pc() 
    print(pc)
    instruction = int(instruction, 16)

    opcode = (instruction & 0b11111100000000000000000000000000) >> 26
    special = (instruction & 0b11111100000000000000000000000000) & 0x3f
    imm = instruction & 0xFFFF
    func = opcode & 0x3F
    e = (opcode >> 21) & 0xF
    rsx = (opcode >> 11) & 0x1f
    rdx = (opcode >> 6) & 0x1f

    sa = (instruction >> 6) & 0x1f

    grt = REG_NAMES[(opcode >> 16) & 0x1f]
    
    rs = REG_NAMES[(instruction >> 21) & 0x1f]
    rt = REG_NAMES[(instruction >> 16) & 0x1f]
    rd = REG_NAMES[(instruction >> 11) & 0x1f]



    vrs = VREG_NAMES[(opcode >> 11) & 0x1f]
    vrt = VREG_NAMES[(opcode >> 16) & 0x1f]
    vrd = VREG_NAMES[(opcode >> 6) & 0x1f]
    
    target = instruction & 0b0000_0011_1111_1111_1111_1111_1111_1111

        
        
    if instruction == 0x00000000:
        #print('NOP')
        return
    


    if opcode == 0x00:
            
        if special == 0x00:
                if func == 0x0:
                    #print(f'sll {rd} {rt} {hex(sa)}')
                    return rsp.registers.set(rd, SLL(rsp.registers.get(rd), rsp.registers.get(rt), sa))
                if func == 0x2:
                    #print(f'srl {rd} {rt} {hex(sa)}')
                    return rsp.registers.set(rd, SRL(rsp.registers.get(rd), rsp.registers.get(rt), sa))
        if special == 0x02:
                #print(f'srl {rd} {rt} {hex(sa)}')
                return rsp.registers.set(rd, SRL(rsp.registers.get(rd), rsp.registers.get(rt), sa))
        if special == 0x00:
                if func == 0x03: 
                    #print(f'sra {rd} {rt} {hex(sa)}')
                    return rsp.registers.set(rd, SRA(rsp.registers.get(rd), rsp.registers.get(rt), sa))
        if special == 0x00:
                if func == 0x04:
                    #print(f'sllv {rd} {rt} {rs}')
                    return rsp.registers.set(rd, SLLV(rsp.registers.get(rd), rsp.registers.get(rt), rsp.registers.get(rs)))
        if special == 0x00:
                if func == 0x06:
                    #print(f'srlv {rd} {rt} {rs}')
                    return rsp.registers.set(rd, SRLV(rsp.registers.get(rd), rsp.registers.get(rt), rsp.registers.get(rs)))
        if special == 0x07:
               # print(f'srav {rd} {rt} {rs}')
                return rsp.registers.set(rd, SRAV(rsp.registers.get(rd), rsp.registers.get(rt), rsp.registers.get(rs)))

        if special == 0x00:
                if func == 0x08:
                    #print(f'jr {rs}')
                    return (FetchAndDecodeRSP(rsp, rsp.execute_next_instruction(rsp, pc)), rsp.set_pc(JR(rsp.registers.get(rs))))
               
        if special == 0x00:
            if func == 0x09:
                #print(f'jalr {rd} {rs}')
                #return (rsp.registers.set(rd, JALR(rsp.registers.get(rs))), rsp.get_pc())
                return (FetchAndDecodeRSP(rsp, rsp.execute_next_instruction(rsp, pc)), rsp.registers.set(rs, sign_extend(pc+4,32)), rsp.set_pc(JAL(target, pc)))
                
        if special == 0x0D:
                print(f'break')
        if special == 0x0F:
                print(f'sync')





        if special == 0x00:
                if func == 0x18:
                    #print(f'mult {rt} {rs}')
                    return (rsp.registers.set('LO', MULT(rsp.registers.get(rs), rsp.registers.get(rt))[0]), rsp.registers.set('HI', MULT(rsp.registers.get(rs), rsp.registers.get(rt))[1]))

        if special == 0x00:
                if func == 0x19:
                    #print(f'multu {rt} {rs}')
                    return (rsp.registers.set('LO', MULTU(rsp.registers.get(rs), rsp.registers.get(rt))[0]), rsp.registers.set('HI', MULTU(rsp.registers.get(rs), rsp.registers.get(rt))[1]))
        
        if special == 0x00:
            if func == 0x1A:
                    #print(f'div')
                    #return rsp.registers.set('LO', DIV(rsp.registers.get(rs), rsp.registers.get(rt)))
                    return (rsp.registers.set('LO', DIV(rsp.registers.get(rs), rsp.registers.get(rt))[0]), rsp.registers.set('HI', DIV(rsp.registers.get(rs), rsp.registers.get(rt))[1]))



        if special == 0x00:
                if func == 0x20:
                    #print(f'add {rd} {rs} {rt}')
                    return rsp.registers.set(rd, ADD(rsp.registers.get(rd), rsp.registers.get(rs), rsp.registers.get(rt)))
        if special == 0x00:
                if func == 0x21:
                    #print(f'addu {rd} {rs} {rt}')
                    return rsp.registers.set(rd, ADDU(rsp.registers.get(rd), rsp.registers.get(rs), rsp.registers.get(rt)))

        if special == 0x22:
                #print(f'sub {rd} {rs} {rt}')
                return rsp.registers.set(rd, SUB(rsp.registers.get(rd), rsp.registers.get(rs), rsp.registers.get(rt)))

        if special == 0x00:
                if func == 0x23:
                    #print(f'subu {rd} {rs} {rt}')
                    return rsp.registers.set(rd, SUBU(rsp.registers.get(rd), signToUnsign(rsp.registers.get(rs), 32), signToUnsign(rsp.registers.get(rt), 32)))

        if special == 0x00:
                if func == 0x24:
                    #print(f'and {rd} {rs} {rt}')
                    return rsp.registers.set(rd, AND(rsp.registers.get(rd), rsp.registers.get(rs), rsp.registers.get(rt)))

        if special == 0x00:
                if func == 0x25:
                    #print(f'or {rd} {rs} {rt}')
                    return rsp.registers.set(rd, OR(rsp.registers.get(rd), rsp.registers.get(rs), rsp.registers.get(rt)))
        if special == 0x00:
                if func == 0x26:
                    #print(f'xor {rd} {rs} {rt}')
                    return rsp.registers.set(rd, XOR(rsp.registers.get(rd), rsp.registers.get(rs), rsp.registers.get(rt)))

        if special == 0x27:
                #print(f'nor {rd} {rs} {rt}')
                return rsp.registers.set(rd, NOR(rsp.registers.get(rd), rsp.registers.get(rs), rsp.registers.get(rt)))

        if special == 0x00:
            if func == 0x2A:
                #print(f'slt {rd} {rs} {rt}')
                return rsp.registers.set(rd, SLT(rsp.registers.get(rd), rsp.registers.get(rs), rsp.registers.get(rt)))

        if special == 0x00:
                if func == 0x2B:
                    #print(f'sltu {rd} {rs} {rt}')
                    return rsp.registers.set(rd, SLTU(rsp.registers.get(rd), rsp.registers.get(rs), rsp.registers.get(rt)))





    


        

    if opcode == 0x01:
         
        if vrt == 0x00:
            #print(f'bltz {rs} {imm} {pc}')
            return rsp.set_pc(BLTZ(rsp.registers.get(rd), imm, pc))
        if vrt == 0x01:
            #print(f'bgez {rs} {imm} {pc}')
            return rsp.set_pc(BGEZ(rsp.registers.get(rd), imm, pc))

 
        if vrt == 0x10:
            print(f'bltzal {rs} {imm} {pc}')
        if vrt == 0x11:
            #print(f'bgezal {rs} {imm} {pc}')
            rs = rsp.registers.get(rs)
            rt = rsp.registers.get(rt)
            
       
            return (FetchAndDecodeRSP(rsp, rsp.execute_next_instruction(rsp, pc)), rsp.registers.set('ra', pc+4), rsp.set_pc(BGEZAL(rs, imm, pc)))

         


    if opcode == 0x02:
        #print(f'j {hex(target)}')
        return (FetchAndDecodeRSP(rsp, rsp.execute_next_instruction(rsp, pc)), rsp.set_pc(J(target, pc)))
    if opcode == 0x03:
        #print(f'jal {hex(target)}')
        return (FetchAndDecodeRSP(rsp, rsp.execute_next_instruction(rsp, pc)), rsp.registers.set('ra', sign_extend(pc+4,32)), rsp.set_pc(JAL(target, pc)))
    if opcode == 0x04:
        rs = rsp.registers.get(rs)
        rt = rsp.registers.get(rt)
        beq = BEQ(rs, rt, imm, pc)
        #print(f'beq {rs} {rt} {hex(pc + sign_extend(imm << 2,18) + 4)}')
        return (FetchAndDecodeRSP(rsp, rsp.execute_next_instruction(rsp, pc)), rsp.set_pc(BEQ(rs, rt, imm, pc)))
    if opcode == 0x05:
        rs = rsp.registers.get(rs)
        rt = rsp.registers.get(rt)
        bne = BNE(rs, rt, imm, pc)
        #print(f'bne {rs} {rt} {hex(pc + sign_extend(imm << 2,18) + 4)}')
        return (FetchAndDecodeRSP(rsp, rsp.execute_next_instruction(rsp, pc)), rsp.set_pc(BNE(rs, rt, imm, pc)))
    if opcode == 0x06:
        rs = rsp.registers.get(rs)
        rt = rsp.registers.get(rt)
        blez = BLEZ(rs, rt, imm, pc)
        #print(f'bne {rs} {rt} {hex(pc + sign_extend(imm << 2,18) + 4)}')
        return (FetchAndDecodeRSP(rsp, rsp.execute_next_instruction(rsp, pc)), rsp.set_pc(BLEZ(rs, rt, imm, pc)))
 
    if opcode == 0x07:
        #print(f'bgtz {rs} {imm}')
        return rsp.set_pc(BGTZ(rsp.registers.get(rs),imm, pc))
    
    if opcode == 0x08:
        #print(f'addi {rt} {rs} {sign_extend(imm,16)}')
        return rsp.registers.set(rt, ADDI(rsp.registers.get(rt), rsp.registers.get(rs), sign_extend(imm, 16)))
    if opcode == 0x09:
        #print(f'addiu {rt} {rs} {sign_extend(imm,16)}')        
        return rsp.registers.set(rt, ADDIU(rsp.registers.get(rt), rsp.registers.get(rs), imm))
    if opcode == 0x0A:
        #print(f'slti {rt} {rs} {sign_extend(imm,16)}')
        return rsp.registers.set(rt, SLTI(rsp.registers.get(rt), rsp.registers.get(rs), sign_extend(imm, 16)))
    if opcode == 0x0B:
        #print(f'sltiu {rt} {rs} {imm}')
        return rsp.registers.set(rt, SLTIU(rsp.registers.get(rt), rsp.registers.get(rs), imm))
    if opcode == 0x0C:
        #print(f'andi {rt} {rs} {imm}')
        return rsp.registers.set(rt, ANDI(rsp.registers.get(rt), rsp.registers.get(rs), imm))
    if opcode == 0x0D:
        #print(f'ori {rt} {rs} {hex(imm)}')
        return rsp.registers.set(rt, ORI(rsp.registers.get(rt), rsp.registers.get(rs), imm))
    if opcode == 0x0E:
        #print(f'xori {rt} {rs} {imm}')
        return rsp.registers.set(rt, XORI(rsp.registers.get(rt), rsp.registers.get(rs), imm))
    if opcode == 0x0F:
        #print(f'lui {rt} {imm}')
        return rsp.registers.set(rt, LUI(rsp.registers.get(rt), imm))
        






    if opcode == 0x20:
        print(f'lb {rt} {rs} {imm}')
        return rsp.registers.set(rt, rsp.load_s8(LB(rsp.registers.get(rt), rsp.registers.get(rs), imm)))
    if opcode == 0x21:
        print(f'lh {rt} {rs} {imm}')
        return rsp.registers.set(rt, rsp.load_s16(LH(rsp.registers.get(rt), rsp.registers.get(rs), imm)))
    if opcode == 0x23:
        #print(f'lw {rt} {rs} {imm}')

        return rsp.registers.set(rt, rsp.load(LW(rsp.registers.get(rt), rsp.registers.get(rs), imm)))
    if opcode == 0x24:
        print(f'lbu {rt} {rs} {imm}')
      
        return rsp.registers.set(rt, rsp.load_u8(LBU(rsp.registers.get(rt), rsp.registers.get(rs), imm)))
    if opcode == 0x25:
        print(f'lhu {rt} {rs} {imm}')
        return rsp.registers.set(rt, rsp.load_u16(LHU(rsp.registers.get(rt), rsp.registers.get(rs), imm)))
    if opcode == 0x28:
        print(f'sb {rt} {rs} {imm}')
        return rsp.store_u8(SB(rsp.registers.get(rt), rsp.registers.get(rs), imm), (rsp.registers.get(rt)))
    if opcode == 0x29:
        print(f'sh {rt} {rs} {imm}')
        return rsp.store_u16(SH(rsp.registers.get(rt), rsp.registers.get(rs), imm), (rsp.registers.get(rt)))

    if opcode == 0x2B:
        print(f'sw {rt} {rs} {imm}')
        return rsp.store(SW(rsp.registers.get(rt), rsp.registers.get(rs), imm), rsp.registers.get(rt))









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







    

    if opcode == 0x10:
        rs_cp0 = CP0_REG_NAMES[(instruction >> 21) & 0x1f]
        rt_cp0 = CP0_REG_NAMES[(instruction >> 16) & 0x1f]
        rd_cp0 = CP0_REG_NAMES[(instruction >> 11) & 0x1f]

        M = (instruction >> 21) & 0x1f
        eret = instruction & 0b0000_0000_0000_0000_0000_0000_0111_1111
        if M == 0x04:
            " MTC0 "
           
            if rd_cp0 == 'status':

                return cpu.cp0.registers.set(rd_cp0, cpu.registers.get(rt) & 0xFFF7_FFFF)
            return cpu.cp0.registers.set(rd_cp0, cpu.registers.get(rt))
        if M == 0x00:
            " MFC0 "
            return cpu.registers.set(rt, cpu.cp0.registers.get(rd_cp0))
