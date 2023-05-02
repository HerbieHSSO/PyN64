





from PyN64.CPU.instruction import (
    ADD,
    SLL,
    SRL,
    SRA,
    OR,
    ORI,
    SLLV,
    SRLV,
    SRAV,
    JR,
    JALR,
    MFHI,
    MTHI,
    MFLO,
    MTLO,
    DSLLV,
    DSRLV,
    DSRAV,
    MULT,
    MULTU,
    DIV,
    DIVU,
    DMULT,
    DMULTU,
    DDIV,
    DDIVU,
    ADD,
    ADDU,
    SUB,
    SUBU,
    AND,
    OR,
    XOR,
    NOR,
    SLT,
    SLTU,
    DADD,
    DADDU,
    DSUB,
    DSUBU,
    TEQ,
    DSLL,
    DSRL,
    DSRA,
    BLTZ,
    BGEZ,
    BGEZAL,
    J,
    JAL,
    BEQ,
    BEQL,
    BNE,
    BNEL,
    BLEZ,
    BGTZ,
    ADDI,
    ADDIU,
    SLTI,
    SLTIU,
    ANDI,
    ORI,
    XORI,
    LUI,
    DADDI,
    DADDIU,
    LDL,
    LDR,
    LB,
    LH,
    LWL,
    LW,
    LBU,
    LHU,
    LWR,
    LWU,
    SB,
    SH,
    SWL,
    SW,
    SDL,
    )


import multiprocessing as mp



REG_NAMES = [
    "zr", "at", "v0", "v1", "a0", "a1", "a2", "a3", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
    "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t8", "t9", "k0", "k1", "gp", "sp", "fp", "ra",
    "hi", "lo",
];
CP0_REG_NAMES = [
    "index", "random", "entrylo0", "entrylo1", "context", "pagemask", "wired", "entryhi", "hwrena", "badvaddr", "count", "compare", "status", "cause", "epc", "prid",
    "config", "lladdr", "watchlo", "watchhi", "?20?", "?21?", "?22?", "debug", "depc", "perfctl", "ecc", "cacheerr", "taglo", "taghi", "errorepc", "desave",
];
CP1_REG_NAMES = [
    "f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13", "f14", "f15",
    "f16", "f17", "f18", "f19", "f20", "f21", "f22", "f23", "f24", "f25", "f26", "f27", "f28", "f29", "f30", "f31",
];
def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

def signToUnsign(value, bits):
    if value < 0:
        value = value+(1 << bits)
    return value




def FetchAndDecode(cpu, instruction):
    
    pc = cpu.get_pc() 
    instruction = int(instruction,16)



    print(f'pc: {hex(pc)}, {hex(instruction)}')

 
    cpu.increase_op()
   
    
    
 
    opcode = (instruction & 0b11111100000000000000000000000000) >> 26
    special = (instruction & 0b11111100000000000000000000000000) & 0x3f
    
    sa = (instruction >> 6) & 0x1f
    vrt = (instruction >> 16) & 0x1f


    rs = REG_NAMES[(instruction >> 21) & 0x1f]
    rt = REG_NAMES[(instruction >> 16) & 0x1f]
    rd = REG_NAMES[(instruction >> 11) & 0x1f]

    func = instruction & 0x3f
   
    #base = (instruction & 0x3e00000) >> 21
    
    imm = instruction & 0xFFFF
    

    target = instruction & 0b0000_0011_1111_1111_1111_1111_1111_1111

        
        
    if instruction == 0x00000000:
        #print('NOP')
        return


    if opcode == 0x00:
            
        if special == 0x00:
                if func == 0x0:
                    #print(f'sll {rd} {rt} {hex(sa)}')
                    return cpu.registers.set(rd, SLL(cpu.registers.get(rd), cpu.registers.get(rt), sa))
        if special == 0x02:
                #print(f'srl {rd} {rt} {hex(sa)}')
                return cpu.registers.set(rd, SRL(cpu.registers.get(rd), cpu.registers.get(rt), sa))
        if special == 0x03:
                #print(f'sra {rd} {rt} {hex(sa)}')
                return cpu.registers.set(rd, SRA(cpu.registers.get(rd), cpu.registers.get(rt), sa))
        if special == 0x00:
                if func == 0x04:
                    #print(f'sllv {rd} {rt} {rs}')
                    return cpu.registers.set(rd, SLLV(cpu.registers.get(rd), cpu.registers.get(rt), cpu.registers.get(rs)))
        if special == 0x00:
                if func == 0x06:
                    #print(f'srlv {rd} {rt} {rs}')
                    return cpu.registers.set(rd, SRLV(cpu.registers.get(rd), cpu.registers.get(rt), cpu.registers.get(rs)))
        if special == 0x07:
               # print(f'srav {rd} {rt} {rs}')
                return cpu.registers.set(rd, SRAV(cpu.registers.get(rd), cpu.registers.get(rt), cpu.registers.get(rs)))

        if special == 0x00:
                if func == 0x08:
                    #print(f'jr {rs}')
                    return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(JR(cpu.registers.get(rs))))
               
        if special == 0x09:
                #print(f'jalr {rs}')
                return (cpu.registers.set(ra, JALR(cpu.registers.get(rs))), cpu.get_pc())

        if special == 0x0D:
                print(f'break')
        if special == 0x0F:
                print(f'sync')

        if special == 0x00:
                if func == 0x10:
                    #print(f'mfhi {rd}')
                    return cpu.registers.set(rd, MFHI(cpu.registers.get(rd), cpu.registers.get('HI')))

        if special == 0x00:
                if func == 0x11:
                    #print(f'mthi {rs}')
                    return cpu.registers.set(rd, MFHI(cpu.registers.get(rs), cpu.registers.get('HI')))
                
        if special == 0x00:
                if func == 0x12:
                    #print(f'mflo {rd}')
                    return cpu.registers.set(rd, MFLO(cpu.registers.get(rd), cpu.registers.get('LO')))

        if special == 0x00:
                if func == 0x13:
                    #print(f'mtlo {rs}')
                    return cpu.registers.set(rd, MFLO(cpu.registers.get(rs), cpu.registers.get('LO')))

        if special == 0x14:
                #print(f'dsllv {rd} {rt} {rs}')
                return cpu.registers.set(rd, DSLLV(cpu.registers.get(rd), cpu.registers.get(rt), cpu.registers.get(rs)))
        if special == 0x16:
                #print(f'dsrlv {rd} {rt} {rs}')
                return cpu.registers.set(rd, DSRLV(cpu.registers.get(rd), cpu.registers.get(rt), cpu.registers.get(rs)))
        if special == 0x17:
                #print(f'dsrav {rd} {rt} {rs}')
                return cpu.registers.set(rd, DSRAV(cpu.registers.get(rd), cpu.registers.get(rt), cpu.registers.get(rs)))

        if special == 0x00:
                if func == 0x18:
                    #print(f'mult {rt} {rs}')
                    return (cpu.registers.set('LO', MULT(cpu.registers.get(rs), cpu.registers.get(rt))[0]), cpu.registers.set('HI', MULT(cpu.registers.get(rs), cpu.registers.get(rt))[1]))

        if special == 0x00:
                if func == 0x19:
                    #print(f'multu {rt} {rs}')
                    return (cpu.registers.set('LO', MULTU(cpu.registers.get(rs), cpu.registers.get(rt))[0]), cpu.registers.set('HI', MULTU(cpu.registers.get(rs), cpu.registers.get(rt))[1]))

        if special == 0x1A:
                #print(f'div')
                return cpu.registers.set(LO, DIV(cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x1B:
                #print(f'divu ')
                return cpu.registers.set(LO, DIVU(cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x1C:
                #print(f'dmult ')
                return cpu.registers.set(LO, DMULT(cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x1D:
                #print(f'dmultu ')
                return cpu.registers.set(LO, DMULTU(cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x1E:
                #print(f'ddiv ')
                return cpu.registers.set(LO, DDIV(cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x1F:
                #print(f'ddivu ')
                return cpu.registers.set(LO, DDIVU(cpu.registers.get(rs), cpu.registers.get(rt)))


        if special == 0x00:
                if func == 0x20:
                    #print(f'add {rd} {rs} {rt}')
                    return cpu.registers.set(rd, ADD(cpu.registers.get(rd), cpu.registers.get(rs), cpu.registers.get(rt)))
        if special == 0x00:
                if func == 0x21:
                    #print(f'addu {rd} {rs} {rt}')
                    return cpu.registers.set(rd, ADDU(cpu.registers.get(rd), cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x22:
                #print(f'sub {rd} {rs} {rt}')
                return cpu.registers.set(rd, SUB(cpu.registers.get(rd), cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x00:
                if func == 0x23:
                    #print(f'subu {rd} {rs} {rt}')
                    return cpu.registers.set(rd, SUBU(cpu.registers.get(rd), signToUnsign(cpu.registers.get(rs), 32), signToUnsign(cpu.registers.get(rt), 32)))

        if special == 0x00:
                if func == 0x24:
                    #print(f'and {rd} {rs} {rt}')
                    return cpu.registers.set(rd, AND(cpu.registers.get(rd), cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x00:
                if func == 0x25:
                    #print(f'or {rd} {rs} {rt}')
                    return cpu.registers.set(rd, OR(cpu.registers.get(rd), cpu.registers.get(rs), cpu.registers.get(rt)))
        if special == 0x00:
                if func == 0x26:
                    #print(f'xor {rd} {rs} {rt}')
                    return cpu.registers.set(rd, XOR(cpu.registers.get(rd), cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x27:
                #print(f'nor {rd} {rs} {rt}')
                return cpu.registers.set(rd, NOR(cpu.registers.get(rd), cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x2A:
                #print(f'slt {rd} {rs} {rt}')
                return cpu.registers.set(rd, SLT(cpu.registers.get(rd), cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x00:
                if func == 0x2B:
                    #print(f'sltu {rd} {rs} {rt}')
                    return cpu.registers.set(rd, SLTU(cpu.registers.get(rd), cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x2C:
                #print(f'dadd {rd} {rs} {rt}')
                return cpu.registers.set(rd, DADD(cpu.registers.get(rd), cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x2D:
                #print(f'daddu {rd} {rs} {rt}')
                return cpu.registers.set(rd, DADDU(cpu.registers.get(rd), cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x2E:
                #print(f'dsub {rd} {rs} {rt}')
                return cpu.registers.set(rd, DSUB(cpu.registers.get(rd), cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x2F:
                #print(f'dsubu {rd} {rs} {rt}')
                return cpu.registers.set(rd, DSUBU(cpu.registers.get(rd), cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x34:
                #print(f'teq {rs} {rt}')
                return TEQ(cpu.registers.get(rs), cpu.registers.get(rt))

        if special == 0x38:
                #print(f'dsll {rd} {rt} {sa}')
                return cpu.registers.set(rd, DSLL(cpu.registers.get(rd), cpu.registers.get(rt), sa))

        if special == 0x3A:
                #print(f'dsrl {rd} {rt} {sa}')
                return cpu.registers.set(rd, DSRL(cpu.registers.get(rd), cpu.registers.get(rt), sa))

        if special == 0x3B:
                #print(f'dsra {rd} {rt} {sa}')
                return cpu.registers.set(rd, DSRA(cpu.registers.get(rd), cpu.registers.get(rt), sa))

        if special == 0x3C:
                print(f'dsll32 {rd} {rt} {sa}')
        if special == 0x3E:
                print(f'dsrl32 {rd} {rt} {sa}')
        if special == 0x3F:
                print(f'dsra32 {rd} {rt} {sa}')

    if opcode == 0x01:
         
        if vrt == 0x00:
            #print(f'bltz {rs} {imm} {pc}')
            return cpu.set_pc(BLTZ(cpu.registers.get(rd), imm, pc))
        if vrt == 0x01:
            #print(f'bgez {rs} {imm} {pc}')
            return cpu.set_pc(BGEZ(cpu.registers.get(rd), imm, pc))
        if vrt == 0x02:
            print(f'bltzl {rs} {imm} {pc}')
        if vrt == 0x03:
            print(f'bgezl {rs} {imm} {pc}')
        if vrt == 0x10:
            print(f'bltzal {rs} {imm} {pc}')
        if vrt == 0x11:
            #print(f'bgezal {rs} {imm} {pc}')
            rs = cpu.registers.get(rs)
            rt = cpu.registers.get(rt)
            
       
            return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.registers.set('ra', pc+8), cpu.set_pc(BGEZAL(rs, imm, pc)))

         
        if vrt == 0x12:
            print(f'bltzall {rs} {imm} {pc}')
        if vrt == 0x13:
            print(f'bgezall {rs} {imm} {pc}')


    if opcode == 0x02:
        #print(f'j {hex(target)}')
        return cpu.set_pc(J(target, pc))
    if opcode == 0x03:
        #print(f'jal {hex(target)}')
        return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.registers.set('ra', pc+4), cpu.set_pc(JAL(target, pc)))
    if opcode == 0x04:
        rs = cpu.registers.get(rs)
        rt = cpu.registers.get(rt)
        #print(f'beq {rs} {rt} {hex(pc + sign_extend(imm << 2,18) + 4)}')
        return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(BEQ(rs, rt, imm, pc)))
    if opcode == 0x05:
        rs = cpu.registers.get(rs)
        rt = cpu.registers.get(rt)
        bne = BNE(rs, rt, imm, pc)
        #print(f'bne {rs} {rt} {hex(pc + sign_extend(imm << 2,18) + 4)}')
        return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(BNE(rs, rt, imm, pc)))
    if opcode == 0x06:
        #print(f'blez {rs} {imm}')
        return cpu.set_pc(BLEZ(cpu.registers.get(rs), imm, pc))
    if opcode == 0x07:
        #print(f'bgtz {rs} {imm}')
        return cpu.set_pc(BGTZ(cpu.registers.get(rs),imm, pc))
    
    if opcode == 0x08:
        #print(f'addi {rt} {rs} {sign_extend(imm,16)}')
        return cpu.registers.set(rt, ADDI(cpu.registers.get(rt), cpu.registers.get(rs), sign_extend(imm, 16)))
    if opcode == 0x09:
        #print(f'addiu {rt} {rs} {sign_extend(imm,16)}')        
        return cpu.registers.set(rt, ADDIU(cpu.registers.get(rt), cpu.registers.get(rs), imm))
    if opcode == 0x0A:
        #print(f'slti {rt} {rs} {sign_extend(imm,16)}')
        return cpu.registers.set(rt, SLTI(cpu.registers.get(rt), cpu.registers.get(rs), sign_extend(imm, 16)))
    if opcode == 0x0B:
        #print(f'sltiu {rt} {rs} {imm}')
        return cpu.registers.set(rt, SLTIU(cpu.registers.get(rt), cpu.registers.get(rs), imm))
    if opcode == 0x0C:
        #print(f'andi {rt} {rs} {imm}')
        return cpu.registers.set(rt, ANDI(cpu.registers.get(rt), cpu.registers.get(rs), imm))
    if opcode == 0x0D:
        #print(f'ori {rt} {rs} {hex(imm)}')
        return cpu.registers.set(rt, ORI(cpu.registers.get(rt), cpu.registers.get(rs), imm))
    if opcode == 0x0E:
        #print(f'xori {rt} {rs} {imm}')
        return cpu.registers.set(rt, XORI(cpu.registers.get(rt), cpu.registers.get(rs), imm))
    if opcode == 0x0F:
        #print(f'lui {rt} {imm}')
        return cpu.registers.set(rt, LUI(cpu.registers.get(rt), imm))
        

    if opcode == 0x14:
        #print(f'beql {rs} {rt} {sign_extend(imm << 2, 18) + 4}')
        return cpu.set_pc(BEQL(cpu.registers.get(rs), cpu.registers.get(rt), sign_extend((imm << 2),18), cpu.get_pc()))
    if opcode == 0x15:
        #print(f'bnel {rs} {rt} {sign_extend(imm << 2, 18) + 4}')
        rs = cpu.registers.get(rs)
        rt = cpu.registers.get(rt)
        return cpu.set_pc(BNEL(rs, rt, sign_extend(imm<<2,18), pc))





    if opcode == 0x18:
        #print(f'daddi {rt} {rs} {imm}')
        return cpu.registers.set(rt, DADDI(cpu.registers.get(rt), cpu.registers.get(rs), imm))
    
    if opcode == 0x19:
        #print(f'daddiu {rt} {rs} {imm}')
        return cpu.registers.set(rt, DADDIU(cpu.registers.get(rt), cpu.registers.get(rs), imm))
    if opcode == 0x1A:
        print(f'ldl {rt} {rs} {imm}')
        return cpu.registers.set(rt, cpu.load(LDL(cpu.registers.get(rt), cpu.registers.get(rs), imm)))
    if opcode == 0x1A:
        print(f'ldr {rt} {rs} {imm}')
        return cpu.registers.set(rt, cpu.load(LDR(cpu.registers.get(rt), cpu.registers.get(rs), imm)))
       
    if opcode == 0x20:
        print(f'lb {rt} {rs} {imm}')
        return cpu.registers.set(rt, cpu.load(LB(cpu.registers.get(rt), cpu.registers.get(rs), imm)))
    if opcode == 0x21:
        print(f'lh {rt} {rs} {imm}')
        return cpu.registers.set(rt, cpu.load(LH(cpu.registers.get(rt), cpu.registers.get(rs), imm)))
    if opcode == 0x22:
        print(f'lwl {rt} {rs} {imm}')
        return cpu.registers.set(rt, cpu.load(LWL(cpu.registers.get(rt), cpu.registers.get(rs), imm)))
    if opcode == 0x23:
        #print(f'lw {rt} {rs} {imm}')

        return cpu.registers.set(rt, cpu.load(LW(cpu.registers.get(rt), cpu.registers.get(rs), imm)))
    if opcode == 0x24:
        #print(f'lbu {rt} {rs} {imm}')
        return cpu.registers.set(rt, cpu.load(LBU(cpu.registers.get(rt), cpu.registers.get(rs), sign_extend(imm,16))))
    if opcode == 0x25:
        print(f'lhu {rt} {rs} {imm}')
        return cpu.registers.set(rt, cpu.load(LHU(cpu.registers.get(rt), cpu.registers.get(rs), imm)))
    if opcode == 0x26:
        print(f'lwr {rt} {rs} {imm}')
        return cpu.registers.set(rt, cpu.load(LWR(cpu.registers.get(rt), cpu.registers.get(rs), target)))
    if opcode == 0x27:
        print(f'lwu {rt} {rs} {imm}')
        return cpu.registers.set(rt, cpu.load(LWU(cpu.registers.get(rt), cpu.registers.get(rs), target)))
    if opcode == 0x28:
        print(f'sb {rt} {rs} {imm}')
        return cpu.store(imm, SB(cpu.registers.get(rt), cpu.registers.get(rs), target))
    if opcode == 0x29:
        print(f'sh {rt} {rs} {imm}')
        return cpu.store(SH(cpu.registers.get(rt), cpu.registers.get(rs), imm), cpu.registers.get(rt))
    if opcode == 0x2A:
        print(f'swl {rt} {rs} {imm}')
        return cpu.store(imm, SWL(cpu.registers.get(rt), cpu.registers.get(rs), target))
    if opcode == 0x2B:
        #print(f'sw {rt} {rs} {imm}')
        return cpu.store(SW(cpu.registers.get(rt), cpu.registers.get(rs), imm), cpu.registers.get(rt))
    if opcode == 0x2C:
        print(f'sdl {rt} {rs} {imm}')
        return cpu.store(imm, SDL(cpu.registers.get(rt), cpu.registers.get(rs), target))



    # ----------------> CP0 <----------------
    if opcode == 0x2F:
        #print(f'cache {base} {rt} {imm}')
        None


    if opcode == 0x10:
        rs_cp0 = CP0_REG_NAMES[(instruction >> 21) & 0x1f]
        rt_cp0 = CP0_REG_NAMES[(instruction >> 16) & 0x1f]
        rd_cp0 = CP0_REG_NAMES[(instruction >> 11) & 0x1f]

        M = (instruction >> 21) & 0x1f
        eret = instruction & 0b0000_0000_0000_0000_0000_0000_0111_1111
        if M == 0x04:
            " MTC0 "
            return cpu.cp0.registers.set(rd_cp0, cpu.registers.get(rt))
        if M == 0x00:
            " MFC0 "
            return cpu.registers.set(rt, cpu.cp0.registers.get(rd_cp0))
    

        if instruction == 0x42000018:
            cpu.set_pc(0x80000180)
            cpu.memory.write(2150848944, 2150868784)
    


   




    # ----------------> CP1 <----------------


    if opcode == 0x11:
        # CFC1
        if (instruction >> 21) & 0x1f == 0x02:
            fs = CP1_REG_NAMES[(instruction >> 11) & 0x1f]
            if fs == 'f0' or 'f31':
                cpu.registers.set(rt, cpu.cp1.registers.get_control(fs))

        if (instruction >> 21) & 0x1f == 0x06:
            # CTC1
            t = CP0_REG_NAMES[(instruction >> 16) & 0x1f]
            fs = CP1_REG_NAMES[(instruction >> 11) & 0x1f]

            if fs == 'f31':
                cpu.cp1.registers.set_control(fs, cpu.registers.get(rt))








