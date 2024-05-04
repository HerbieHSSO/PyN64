





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
    LD,
    DSLL32,
    DSRL32,
    DSRA32,
    SD,
    )



import struct
import math
from numba import jit

REG_NAMES = [
    "zr", "at", "v0", "v1", "a0", "a1", "a2", "a3", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
    "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "t8", "t9", "k0", "k1", "gp", "sp", "s8", "ra",
    "hi", "lo",
];
CP0_REG_NAMES = [
    "index", "random", "entrylo0", "entrylo1", "context", "pagemask", "wired", "hwrena", "badvaddr", "count", "entryhi", "compare", "status", "cause", "epc",
    "prid", "config", "lladdr", "watchlo", "watchhi", "?20?", "?21?", "?22?", "debug", "depc", "perfcnt", "errctl", "cacheerr", "taglo", "taghi",
    "errorepc", "desave",
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

def get_bit(value, bit):
    return (value & (1 << bit)) >> bit

def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def ieee754_to_int(f):
    return struct.unpack('!I', struct.pack('!f', f))[0]

def int_to_ieee754(i, p):
    return struct.unpack('!f', (i).to_bytes(p, 'big'))[0]
global i
i = 0

def FetchAndDecode(cpu, instruction):
    
    pc = cpu.get_pc() 
    instruction = int(instruction,16)

    

    print(f'pc: {hex(pc)}, {hex(instruction)}')

 
    cpu.increase_op()

    #cpu.cp0.registers.set('count', cpu.cp0.registers.get('count') + 1)
    
    
 
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
                if func == 0x2:
                    #print(f'srl {rd} {rt} {hex(sa)}')
                    return cpu.registers.set(rd, SRL(cpu.registers.get(rd), cpu.registers.get(rt), sa))
        if special == 0x02:
                #print(f'srl {rd} {rt} {hex(sa)}')
                return cpu.registers.set(rd, SRL(cpu.registers.get(rd), cpu.registers.get(rt), sa))
        if special == 0x00:
                if func == 0x03: 
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
               
        if special == 0x00:
            if func == 0x09:
                #print(f'jalr {rd} {rs}')
                #return (cpu.registers.set(rd, JALR(cpu.registers.get(rs))), cpu.get_pc())
                return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.registers.set(rd, sign_extend(pc+4,32)), cpu.set_pc(JALR(cpu.registers.get(rs), pc)))
                
        if special == 0x00:
            if func == 0x0D:
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
                    return cpu.registers.set("LO", cpu.registers.get(rs))

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
        
        if special == 0x00:
            if func == 0x1A:
                    #print(f'div')
                    #return cpu.registers.set('LO', DIV(cpu.registers.get(rs), cpu.registers.get(rt)))
                    return (cpu.registers.set('LO', DIV(cpu.registers.get(rs), cpu.registers.get(rt))[0]), cpu.registers.set('HI', DIV(cpu.registers.get(rs), cpu.registers.get(rt))[1]))

        if special == 0x1B:
                #print(f'divu ')
                return cpu.registers.set(LO, DIVU(cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x1C:
                #print(f'dmult ')
                return cpu.registers.set(LO, DMULT(cpu.registers.get(rs), cpu.registers.get(rt)))

        if special == 0x00:
                if func == 0x1D:
                    #print(f'dmultu ')
                    return (cpu.registers.set('LO', DMULTU(cpu.registers.get(rs), cpu.registers.get(rt))[0]), cpu.registers.set('HI',DMULTU(cpu.registers.get(rs), cpu.registers.get(rt))[1]))

        if special == 0x1E:
                #print(f'ddiv ')
                    return (cpu.registers.set('LO', DDIV(cpu.registers.get(rs), cpu.registers.get(rt))[0]), cpu.registers.set('HI',DDIV(cpu.registers.get(rs), cpu.registers.get(rt))[1]))

        if special == 0x00:
                if func == 0x1F:
                    #print(f'ddivu ')
                    return (cpu.registers.set('LO', DDIVU(cpu.registers.get(rs), cpu.registers.get(rt))[0]), cpu.registers.set('HI', DDIVU(cpu.registers.get(rs), cpu.registers.get(rt))[1]))



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
                    return cpu.registers.set(rd, SUBU(cpu.registers.get(rd), cpu.registers.get(rs), cpu.registers.get(rt)))

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

        if special == 0x00:
            if func == 0x2A:
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

        if special == 0x00:
                if func == 0x3C:
                    print(f'dsll32 {rd} {rt} {sa}')
                    return cpu.registers.set(rd, DSLL32(cpu.registers.get(rd), cpu.registers.get(rt), sa))
        if special == 0x00:
                if func == 0x3E:
                    print(f'dsrl32 {rd} {rt} {sa}')
                    return cpu.registers.set(rd, DSRL32(cpu.registers.get(rd), cpu.registers.get(rt), sa))
        if special == 0x00:
                if func == 0x3F:
                    print(f'dsra32 {rd} {rt} {sa}')
                    return cpu.registers.set(rd, DSRA32(cpu.registers.get(rd), cpu.registers.get(rt), sa))
        

    if opcode == 0x01:
         
        if vrt == 0x00:
            #print(f'bltz {rs} {imm} {pc}')
            rs = cpu.registers.get(rs)
            rt = cpu.registers.get(rt)
            target = sign_extend(target << 2, 18)
            if (rs & 0xFFFF_FFFF_FFFF_FFFF) < 0:
                return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
            else:
                return cpu.set_pc(pc)
        if vrt == 0x01:
            #print(f'bgez {rs} {imm} {pc}')
            rs = cpu.registers.get(rs)
            rt = cpu.registers.get(rt)
            target = sign_extend(target << 2, 18)
            if (rs & 0xFFFF_FFFF_FFFF_FFFF) >= 0:
                return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
            else:
                return cpu.set_pc(pc)
        if vrt == 0x02:
            #print(f'bltzl {rs} {imm} {pc}')
            rs = cpu.registers.get(rs)
            rt = cpu.registers.get(rt)
            target = sign_extend(target << 2, 18)
            if (rs & 0xFFFF_FFFF_FFFF_FFFF) < 0:
                return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
            else:
                return cpu.set_pc(pc+4)
        if vrt == 0x03:
            print(f'bgezl {rs} {imm} {pc}')
            rs = cpu.registers.get(rs)
            rt = cpu.registers.get(rt)
            target = sign_extend(target << 2, 18)
            if (rs & 0xFFFF_FFFF_FFFF_FFFF) >= 0:
                return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
            else:
                return cpu.set_pc(pc+4)
        if vrt == 0x10:
            #print(f'bltzal {rs} {imm} {pc}')
            rs = cpu.registers.get(rs)
            rt = cpu.registers.get(rt)
            target = sign_extend(target << 2, 18)
            cpu.registers.set("ra", pc+4)
            if (rs & 0xFFFF_FFFF_FFFF_FFFF) < 0:
                return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
            else:
                return cpu.set_pc(pc+4)
        if vrt == 0x11:
            #print(f'bgezal {rs} {imm} {pc}')
            rs = cpu.registers.get(rs)
            rt = cpu.registers.get(rt)
            target = sign_extend(target << 2, 18)
            cpu.registers.set("ra", pc+4)
            if (rs & 0xFFFF_FFFF_FFFF_FFFF) >= 0:
                return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
            else:
                return cpu.set_pc(pc+4)

         
        if vrt == 0x12:
            #print(f'bltzall {rs} {imm} {pc}')
            rs = cpu.registers.get(rs)
            rt = cpu.registers.get(rt)
            target = sign_extend(target << 2, 18)
            cpu.registers.set("ra", pc+4)
            if (rs & 0xFFFF_FFFF_FFFF_FFFF) < 0:
                return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
            else:
                return cpu.set_pc(pc+4)
        if vrt == 0x13:
            print(f'bgezall {rs} {imm} {pc}')


    if opcode == 0x02:
        #print(f'j {hex(target)}')
        return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(J(target, pc)))
    if opcode == 0x03:
        #print(f'jal {hex(target)}')
        return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.registers.set('ra', sign_extend(pc+4,32)), cpu.set_pc(JAL(target, pc)))
    if opcode == 0x04:
        #print(f'beq {rs} {rt} {hex(pc + sign_extend(imm << 2,18) + 4)}')
        rs = cpu.registers.get(rs)
        rt = cpu.registers.get(rt)

        
        target = sign_extend(target << 2, 18)
        

        if (rs & 0xFFFF_FFFF_FFFF_FFFF) == (rt & 0xFFFF_FFFF_FFFF_FFFF):
            return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
            
        else:
            return cpu.set_pc(pc)
    if opcode == 0x05:
        rs = cpu.registers.get(rs)
        rt = cpu.registers.get(rt)
        bne = BNE(rs, rt, imm, pc)
        #print(f'bne {rs} {rt} {hex(pc + sign_extend(imm << 2,18) + 4)}')
        target = sign_extend(target << 2, 18)
        

        if (rs) != (rt):
            return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
            
        else:
            return cpu.set_pc(pc)
       
    if opcode == 0x06:
        rs = cpu.registers.get(rs)
        rt = cpu.registers.get(rt)
        #print(f'blez {rs} {rt} {hex(pc + sign_extend(imm << 2,18) + 4)}')
        target = sign_extend(target << 2, 18)
        
        if (rs) <= 0:
            return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
        else:
            return cpu.set_pc(pc)
 
    if opcode == 0x07:
        #print(f'bgtz {rs} {imm}')
            rs = cpu.registers.get(rs)
            rt = cpu.registers.get(rt)
            target = sign_extend(target << 2, 18)

            if (rs) > 0:
                return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
            else:
                return cpu.set_pc(pc)
    
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
        #print(f'beql {rs} {rt} {hex(pc + sign_extend(imm << 2,18) + 4)}')
        rs = cpu.registers.get(rs)
        rt = cpu.registers.get(rt)

        
        target = sign_extend(target << 2, 18)
        if (rs & 0xFFFF_FFFF_FFFF_FFFF) == (rt & 0xFFFF_FFFF_FFFF_FFFF):
            return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
        else:
            return cpu.set_pc(pc+4)
        
        
    if opcode == 0x15:
        #print(f'bnel {rs} {rt} {sign_extend(imm << 2, 18) + 4}')
        rs = cpu.registers.get(rs)
        rt = cpu.registers.get(rt)
        target = sign_extend(target << 2, 18)
        if (rs & 0xFFFF_FFFF_FFFF_FFFF) != (rt & 0xFFFF_FFFF_FFFF_FFFF):
            return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
        else:
            return cpu.set_pc(pc+4)

    if opcode == 0x16:
        rs = cpu.registers.get(rs)
        rt = cpu.registers.get(rt)

        #print(f'blezl {rs} {rt} {hex(pc + sign_extend(imm << 2,18) + 4)}')
        target = sign_extend(target << 2, 18)
        if (rs & 0xFFFF_FFFF_FFFF_FFFF) <= 0:
            return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
        else:
            return cpu.set_pc(pc+4)

    if opcode == 0x17:
        rs = cpu.registers.get(rs)
        rt = cpu.registers.get(rt)

        #print(f'bgtzl {rs} {rt} {hex(pc + sign_extend(imm << 2,18) + 4)}')
        target = sign_extend(target << 2, 18)
        if (rs & 0xFFFF_FFFF_FFFF_FFFF) > 0:
            return (FetchAndDecode(cpu, cpu.execute_next_instruction(cpu, pc)), cpu.set_pc(pc + target))
        else:
            return cpu.set_pc(pc+4)



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
        return cpu.registers.set(rt, cpu.load_s8(LB(cpu.registers.get(rt), cpu.registers.get(rs), imm)))
    if opcode == 0x21:
        print(f'lh {rt} {rs} {imm}')
        return cpu.registers.set(rt, cpu.load_s16(LH(cpu.registers.get(rt), cpu.registers.get(rs), imm)))
    if opcode == 0x22:
        print(f'lwl {rt} {rs} {imm}')

        addr = (cpu.registers.get(rs) & 0xFFFF_FFFF) + sign_extend(imm, 16)
        data = cpu.registers.get(rt) & 0xFFFF_FFFF
        mem = cpu.load_u((addr & ~3))& 0xFFFF_FFFF

        if (addr & 3) == 0:
            data &= 0
            mem <<= 0
        elif (addr & 3) == 1:
            data &= 0xFF
            mem <<= 8
        elif (addr & 3) == 2:
            data &= 0xFFFF
            mem <<= 16
        elif (addr & 3) == 3:
            data &= 0xFFFF_FF
            mem <<= 24
 
        data |= mem
        cpu.registers.set(rt, sign_extend(data,32))        


    if opcode == 0x23:
        #print(f'lw {rt} {rs} {imm}')

        return cpu.registers.set(rt, cpu.load(LW(cpu.registers.get(rt), cpu.registers.get(rs), imm)))
    if opcode == 0x24:
        print(f'lbu {rt} {rs} {imm}')
      
        return cpu.registers.set(rt, (cpu.load_u8(LBU(cpu.registers.get(rt), cpu.registers.get(rs), imm))))
    if opcode == 0x25:
        print(f'lhu {rt} {rs} {imm}')
        return cpu.registers.set(rt, (cpu.load_u16(LHU(cpu.registers.get(rt), cpu.registers.get(rs), imm))))
    if opcode == 0x26:
        print(f'lwr {rt} {rs} {imm}')
        #return cpu.registers.set(rt, cpu.load(LWR(cpu.registers.get(rt), cpu.registers.get(rs), target)))
        addr = (cpu.registers.get(rs) & 0xFFFF_FFFF) + sign_extend(imm, 16)
        data = cpu.registers.get(rt) & 0xFFFF_FFFF
        mem = cpu.load_u((addr & ~3))& 0xFFFF_FFFF

        match (addr & 3):
             case 0:
                  data &= 0xFFFFFF00
                  mem >>= 24
                  data |= mem
                  cpu.registers.set(rt, sign_extend(data,32))
             case 1:
                  data &= 0xFFFF0000
                  mem >>= 16      
                  data |= mem
                  cpu.registers.set(rt, sign_extend(data,32))
             case 2:
                  data &= 0xFF000000
                  mem >>= 8      
                  data |= mem
                  cpu.registers.set(rt, sign_extend(data,32))     
             case 3:
                  data &= 0x00
                  mem >>= 0 
                  data |= mem
                  cpu.registers.set(rt, sign_extend(data,32))             

        return 
    if opcode == 0x27:
        print(f'lwu {rt} {rs} {imm}')
        return cpu.registers.set(rt, cpu.load_u(LWU(cpu.registers.get(rt), cpu.registers.get(rs), target)))
    if opcode == 0x28:
        print(f'sb {rt} {rs} {imm}')
        return cpu.store_u8(SB(cpu.registers.get(rt), cpu.registers.get(rs), imm), (cpu.registers.get(rt)))
    if opcode == 0x29:
        print(f'sh {rt} {rs} {imm}')
        return cpu.store_u16(SH(cpu.registers.get(rt), cpu.registers.get(rs), imm), (cpu.registers.get(rt)))
    if opcode == 0x2A:
        print(f'swl {rt} {rs} {imm}')
        return cpu.store(imm, SWL(cpu.registers.get(rt), cpu.registers.get(rs), target))
    if opcode == 0x2B:
        print(f'sw {rt} {rs} {imm}')
        return cpu.store(SW(cpu.registers.get(rt), cpu.registers.get(rs), imm), cpu.registers.get(rt))
    if opcode == 0x2C:
        print(f'sdl {rt} {rs} {imm}')
        return cpu.store(imm, SDL(cpu.registers.get(rt), cpu.registers.get(rs), target))




    if opcode == 0x37:
        print(f'ld {rt} {rs} {imm}')

        return cpu.registers.set(rt, cpu.load_u64(LD(cpu.registers.get(rt), cpu.registers.get(rs), imm)))




    if opcode == 0x3F:
        print(f'sd {rt} {rs} {imm}')
        return cpu.store_u64(SD(cpu.registers.get(rt), cpu.registers.get(rs), imm), (cpu.registers.get(rt)))

    # ----------------> CP0 <----------------


    if opcode == 0x10:
         
         if func == 0x18:
            # ERET
            print('eret')

       
                
            if get_bit(cpu.cp0.registers.get("status"), 2) == 1:

        
                  
                    cpu.set_pc(cpu.cp0.registers.get("errorepc") & 0xFFFF_FFFF)
                    cpu.cp0.registers.set("status", clear_bit(cpu.cp0.registers.get("status"),2))
            
                    #cpu.cp0.registers.set("cause", 0x400)
                    #cpu.set_pc(0x80000180)
                
            else:
                print(cpu.cp0.registers.get("epc"))
                cpu.set_pc(cpu.cp0.registers.get("epc") & 0xFFFF_FFFF)
                cpu.cp0.registers.set("status", clear_bit(cpu.cp0.registers.get("status"),1))
            return
            
            """
            if is_set(cpu.cp0.registers.get("status"), 4):
                    cpu.set_pc(cpu.cp0.registers.get("errorepc") & 0xFFFF_FFFF)
                    print(cpu.cp0.registers.get("status"))
                    cpu.cp0.registers.set("status", clear_bit(cpu.cp0.registers.get("status"),4))
                    if (cpu.cp0.registers.get("errorepc") & 0xFFFF_FFFF) == 0xFFFF_FFFF:
                         cpu.set_pc(0x80000180)
                         cpu.cp0.registers.set("status", 0xFF01)
                         cpu.cp0.registers.set("cause", 0x100)
            else:
                cpu.set_pc(cpu.cp0.registers.get("epc") & 0xFFFF_FFFF)
                cpu.cp0.registers.set("status", clear_bit(cpu.cp0.registers.get("status"),2))
            return 
            #cpu.set_pc(cpu.cp0.registers.get("epc") & 0xFFFF_FFFF)
            #cpu.cp0.registers.set("status", clear_bit(cpu.cp0.registers.get("status"),2))            
            #cpu.cp0.registers.set("epc", pc+4)
            #cpu.cp0.registers.set("status", 0)
            #cpu.set_pc(cpu.cp0.registers.get("epc"))
            """
    if opcode == 0x2F:
        #print(f'cache {base} {rt} {imm}')
        None
        return

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
    




   




    # ----------------> CP1 <----------------


                     

    if opcode == 0x11:
        fmt = (instruction >> 21) & 0x1f
        ft = CP0_REG_NAMES[(instruction >> 16) & 0x1f]
        fs = CP1_REG_NAMES[(instruction >> 11) & 0x1f]
        fd = CP0_REG_NAMES[(instruction >> 6) & 0x1f]

        if fmt == 0x00:
             # MFC1
             return cpu.registers.set(rt, sign_extend(ieee754_to_int(cpu.cp1.registers.get(fs)),32))
            


        if fmt == 0x04:
             # MTC1
             return cpu.cp1.registers.set(fd, cpu.registers.get(rt))
        
        if func == 0x02:
             # MUL
             if fmt == 16:
                # MUL.S - SINGLE PRECISION
                cpu.cp1.registers.set(fd, cpu.cp1.registers.get(fs) * cpu.cp1.registers.get(ft))
       
        if (instruction >> 21) & 0x1f == 0x02:
            # CFC1
            if fs == 'f0' or 'f31':
                  return cpu.registers.set(rt, (cpu.cp1.registers.get("fcsr")))

        if (instruction >> 21) & 0x1f == 0x06:
            # CTC1
            if fs == 'f31':
                return cpu.cp1.registers.set("fcsr", (cpu.registers.get(rt) & 0xFFFF_FFFF))
        if func == 0x0D:
             # TRUNC.W
            if cpu.cp1.registers.get_value(fs) == 0:
                 return cpu.cp1.registers.set(math.ceil(cpu.cp1.registers.get(fs)))
            return cpu.cp1.registers.set(math.floor(cpu.cp1.registers.get(fs)))
    return 





