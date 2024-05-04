from PyN64.CPU import cpu

import numpy as np
from functools import lru_cache




def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)



def signToUnsign(value, bits):
    if value < 0:
        value = value+(1 << bits)
    return value


def LoSigned(n):
    n = n & 0xffffffff
    return n | (-(n & 0x80000000))





def SLL(rd, rt, sa):
    """ SLL """
    
    rd = sign_extend((rt & 0xFFFF_FFFF) << sa,32)

    return rd

def SRL(rd, rt, sa):
    """ SRL """
    
    rd = sign_extend((rt & 0xFFFF_FFFF) >> sa, 32) 
    
    return rd

def SRA(rd, rt, sa):
    """ SRA """
    
    rd = (rt & 0xFFFF_FFFF) >> sa

    
    return sign_extend(rd,32)

def SLLV(rd, rt, rs):
    """ SLLV """
    

    rd = (rt & 0xFFFF_FFFF) << (rs & 0X1F)
    
    return sign_extend(rd, 32)

def SRLV(rd, rt, rs):
    """ SRLV """
    
    rd = (rt & 0xFFFFFFFF) >> (rs & 0b11111)
    
    return sign_extend(rd,32)

def SRAV(rd, rt, rs):
    """ SRAV """
    
    sa = rs & 0x1F

    rd = (rt & 0xFFFF_FFFF) >> sa

    
    
    return sign_extend(rd,32)

def JR(rs):
    """ JR """
     
    return rs & 0xFFFF_FFFF

def JALR(rs, pc):
    """ JALR """
  

    
    return rs & 0xFFFF_FFFF

def MFHI(rd, hi):
    """ MFHI """
  
    
    rd = hi 


    
    return rd
def MTHI(rs, hi):
    """ MTHI """
  
    
    rd = hi 


    
    return rd
def MFLO(rd, lo):
    """ MFLO """
  
    
    rd = lo 
   

    
    return rd

def MTLO(rs, lo):
    """ MTLO """
  
    
    rd = lo 


    
    return rd

def DSLLV(rd, rt, rs):
    """ DSLLV """
    
    rd = rt << rs
    
    return rd

def DSRLV(rd, rt, rs):
    """ DSRLV """
    
    rd = rt >> rs
    
    return rd

def DSRAV(rd, rt, rs):
    """ DSRAV """
    
    rd = rt >> rs
    
    return rd

def MULT(rs, rt):
    """ MULT """
    
    prod = rs * rt

    LO = sign_extend(prod & 0xFFFFFFFF, 32)
    HI = sign_extend((prod & 0xFFFFFFFF00000000) >> 32, 32)
    return [LO, HI]


def MULTU(rs, rt):
    """ MULTU """
    
    prod = rs * rt

    LO = sign_extend(prod & 0xFFFFFFFF, 32)
    HI = sign_extend((prod & 0xFFFFFFFF00000000) >> 32, 32)
 
    return [LO, HI]

def DIV(rs, rt):
    """ DIV """
    
    rd = rs/rt
    
    LO = sign_extend(rs//rt & 0xFFFF_FFFF, 64)
    HI = sign_extend((rs%rt & 0xFFFF_FFFF) >> 64, 64)
 
    return [LO, HI]

def DIVU(rs, rt):
    """ DIVU """
    
    rd = rs/rt
    
    return rd

def DMULT(rs, rt):
    """ DMULT """
    
    rd = rs * rt
    
    return rd

def DMULTU(rs, rt):
    """ MULTU """
    
    prod = rs * rt

    LO = sign_extend(prod & 0xFFFFFFFFFFFFFFFF, 64)
    HI = sign_extend((prod & 0xFFFFFFFFFFFFFFFF) >> 64, 64)
 
    return [LO, HI]

def DDIV(rs, rt):
    """ DDIV """
    
    print(rs, rt)
    LO = sign_extend(int(rs/rt),64)
    HI = sign_extend(int(rs%rt),64)
    
    return [LO, HI]

def DDIVU(rs, rt):
    """ DDIVU """
    rs = rs & 0xFFFF_FFFF_FFFF_FFFF
    rt = rt & 0xFFFF_FFFF_FFFF_FFFF
    LO = int(rs/rt)
    HI = int(rs%rt)
    
    return [LO, HI]

def ADD(rd, rs, rt):
    """ ADD """
    rd = (rs & 0xFFFF_FFFF) + (rt & 0xFFFF_FFFF)
    return sign_extend(rd,32)

def ADDU(rd, rs, rt):
    """ ADDU """

    rd = (rs & 0xFFFF_FFFF) + (rt & 0xFFFF_FFFF)

    return sign_extend(rd, 32)

def SUB(rd, rs, rt):
    """ SUB """
    
    rd = sign_extend((rs & 0xFFFF_FFFF) - (rt & 0xFFFF_FFFF),32)
    
    return rd

def SUBU(rd, rs, rt):
    """ SUBU """
    
    rd = sign_extend((rs & 0xFFFF_FFFF) - (rt & 0xFFFF_FFFF),32)
    
    return rd

def AND(rd, rs, rt):
    """ AND """
    
    rd = rs & rt

    return rd

def OR(rd, rs, rt):
    """ OR """
    
    rd = rs | rt

    return rd

def XOR(rd, rs, rt):
    """ XOR """
    print(rs, rt)
    print(rs ^ rt)
    rd = rs ^ rt
    print(rd)
    return rd

def NOR(rd, rs, rt):
    """ NOR """
    
    rd = ~(rs | rt)
    
    return rd

def SLT(rd, rs, rt):
    """ SLT """



    if sign_extend(rs,64) < sign_extend(rt,64):
        return 1
    else:
        return 0

def SLTU(rd, rs, rt):
    """ SLTU """
    
    if (rs & 0xFFFF_FFFF_FFFF_FFFF) < (rt & 0xFFFF_FFFF_FFFF_FFFF):
        return 1
    else:
        return 0

   

def DADD(rd, rs, rt):
    """ DADD """
    
    rd = sign_extend(rs,64) + sign_extend(rt,64)
    
    return rd & 0xFFFF_FFFF_FFFF_FFFF

def DADDU(rd, rs, rt):
    """ DADDU """
    
    rd = sign_extend(rs,64) + sign_extend(rt,64)
    
    return rd & 0xFFFF_FFFF_FFFF_FFFF

def DSUB(rd, rs, rt):
    """ DSUB """
    
    rd = sign_extend(rs,64) - sign_extend(rt,64)
    
    return rd & 0xFFFF_FFFF_FFFF_FFFF

def DSUBU(rd, rs, rt):
    """ DSUBU """
    
    rd = sign_extend(rs,64) - sign_extend(rt,64)
    
    return rd & 0xFFFF_FFFF_FFFF_FFFF

def TEQ(rs, rt):
    """ TEQ """
    
    if rs == rt:
        return 'Exception'
    
    return None

def DSLL(rd, rt, sa):
    """ DSLL """
    
    rd = rt << sa
    
    return rd

def DSLL32(rd, rt, sa):
    """ DSLL32 """
    
    rd = rt << (32+sa)
    
    return rd

def DSRL32(rd, rt, sa):
    """ DSRL32 """
    
    rd = rt >> (32+sa)
    
    return rd

def DSRA32(rd, rt, sa):
    """ DSRL32 """
    
    rd = rt >> (32+sa)
    
    return rd

def DSRL(rd, rt, sa):
    """ DSRL """
    
    rd = (rt & 0xFFFF_FFFF_FFFF_FFFF) >> sa
    
    return rd

def DSRA(rd, rt, sa):
    """ DSRA """
    
    rd = rt >> sa
    
    return rd



def BLTZ(rs, offset, pc):
    """ BLTZ """
    target = sign_extend(target << 2, 18)
    if sign_extend(rs,64) < 0:
        pc = pc + target
        return pc
    else:
        return pc + 4

def BGEZ(rs, offset, pc):
    """ BGEZ """
    target = sign_extend(target << 2, 18)

    if sign_extend(rs,64) >= 0:
        pc = pc + target
        return pc
    else:
        return pc + 4

def BGEZAL(rs, target, pc):
    """ BGEZAL """
    target = sign_extend(target << 2, 18)
    #pc = pc + 8
    pc = pc + 8

    if rs >= 0:
        pc = pc + target
              
    return pc    

def J(target, pc):
    """ J """
    
    pc = (pc & 0xf0000000) | (target * 4)
    return pc

def JAL(target, pc):
    """ JAL """
 
    #pc = 0x80245000 | (target << 2) & 0xFFFF
 
    pc = (pc & 0xf0000000) | (target * 4)
   
    return int(pc) 

def BEQ(rs, rt, target, pc):
    """ BEQ """

    target = sign_extend(target << 2, 18)

    if (rs & 0xFFFF_FFFF_FFFF_FFFF) == (rt & 0xFFFF_FFFF_FFFF_FFFF):
        
        pc = pc + target
        return pc
    else:
        return pc + 4 

def BEQL(rs, rt, target, pc):
    """ BEQL """
    target = sign_extend(target << 2, 18)
    if (rs & 0xFFFF_FFFF_FFFF_FFFF) == (rt & 0xFFFF_FFFF_FFFF_FFFF):
        
        pc = pc + target
        return pc 
    else:
        return pc + 8


def BNE(rs, rt, target, pc):
    """ BNE """

    target = sign_extend(target << 2, 18)
    
#    if ((rs >> 32) & 0xFFFF_FFFF) != ((rt >> 32) & 0xFFFF_FFFF) | (rs & 0xFFFF_FFFF) != (rt & 0xFFFF_FFFF):
    #if (rs & 0xFFFF_FFFF) == (rt & 0xFFFF_FFFF) or (rs == rt):
    if (rs& 0xFFFF_FFFF_FFFF_FFFF) != (rt & 0xFFFF_FFFF_FFFF_FFFF):
        pc = pc + target
        return pc 
        
        
       
        
        
    else:
        return pc + 4
        
        

def BNEL(rs, rt, target, pc):
    """ BNEL """
 
    if (rs & 0xFFFF_FFFF_FFFF_FFFF) != (rt & 0xFFFF_FFFF_FFFF_FFFF):
        
        pc = pc + target
        return pc
    else:
        return pc + 8 
    
def BLEZ(rs, rt, target, pc):
    """ BLEZ """

    target = sign_extend(target << 2, 18)
    
    if (rs & 0xFFFF_FFFF_FFFF_FFFF) <= 0:
        pc = pc + target
        return pc 
        
        
    else:
        return pc + 4
    

def BGTZ(rs, target, pc):
    """ BGTZ """
    target = sign_extend(target << 2, 18)

    if (rs & 0xFFFF_FFFF_FFFF_FFFF)  > 0:
        pc = pc + target
        return pc
    else:
        return pc + 4


def ADDI(rt, rs, imm):
    """ ADDI """    

    rt = (rs & 0xFFFF_FFFF) + (sign_extend(imm & 0xFFFF,16))

    return sign_extend(rt ,32)


def ADDIU(rt, rs, imm):
    """ ADDIU """
    #print(f'{rs} + {imm}')
    #print(f'{rs + sign_extend(imm, 16)}')

    rt = (rs & 0xFFFF_FFFF) + (sign_extend(imm & 0xFFFF,16))
    return sign_extend(rt,32)


def SLTI(rt, rs, imm):
    """ SLTI """
    
    if sign_extend(rs,64) < sign_extend(imm,16):
        rt = 1
    else:
        rt = 0
    
    return rt

def SLTIU(rt, rs, imm):
    """ SLTIU """
    
    if (rs & 0xFFFF_FFFF_FFFF_FFFF) < (sign_extend(imm,16) & 0xFFFF_FFFF_FFFF_FFFF):
        rt = 1
    else:
        rt = 0
    
    return rt

def ANDI(rt, rs, imm):
    """ ANDI """
    
    rt = rs & (imm & 0xFFFF)

    return rt



def ORI(rt, rs, imm):
    """ ORI """
    
    rt = (rs) | (imm)
    
    return rt

def XORI(rt, rs, imm):
    """ XORI """
    
    rt = (rs) ^ (imm & 0xFFFF) 
    
    return rt

def LUI(rt, imm):
    """ LUI """
    #print(imm << 16)
    return sign_extend((imm << 16),32)

def DADDI(rt, rs, imm):
    """ DADDI """
    rt = sign_extend(rs,64) + imm
    return rt & 0xFFFF_FFFF_FFFF_FFFF

def DADDIU(rt, rs, imm):
    """ DADDIU """
    rt = rs + imm
    return rt

def LDL(rt, base, target):
    """ LDL """
    rt = target + base
    return rt

def LDR(rt, base, target):
    """ LDR """
    rt = target + base
    return rt

def LB(rt, base, target):
    """ LB """
    rt = base + sign_extend(target,16)
    return rt

def LH(rt, base, target):
    """ LH """
    rt = base + sign_extend(target,16)
    return rt

def LWL(rt, base, target):
    """ LWL """
    rt = (base & 0xFFFF_FFFF) + sign_extend(target, 16)
    return rt


def LW(rt, base, target):
    """ LW """
   
    rt = sign_extend(target, 16) + base
   
    return rt

def LD(rt, base, target):
    """ LD """
   
    rt = sign_extend(target, 16) + base

    return rt


def LBU(rt, base, target):
    """ LBU """
    rt = base + sign_extend(target,16)
  
    return rt

def LHU(rt, base, target):
    """ LHU """
    rt = base + sign_extend(target,16)
    print(rt)
    print(base + target)
    return rt

def LWR(rt, base, target):
    """ LWR """

    rt = (base & 0xFFFF_FFFF) + sign_extend(target,16)
    
    return rt

def LWU(rt, base, target):
    """ LWU """
    rt = base + sign_extend(target,16)
    return rt

def SB(rt, base, target):
    """ SB """
    addr = base + target
    
    return addr

def SH(rt, base, target):
    """ SH """
    addr = base + sign_extend(target,16)
    
    return addr

def SWL(rt, base, target):
    """ SWL """
    addr = base + target
    
    return addr

def SW(rt, base, target):
    """ SW """
    
    addr = base + sign_extend(target, 16)
    #print(f'addr: {addr}, base: {base}, target: {target}')
    if addr == 2150848944:
        None
    return addr

def SD(rt, base, target):
    """ SD """
    
    addr = base + sign_extend(target, 16)

    return addr


def SDL(rt, base, target):
    """ SDL """
    addr = base + target
    
    return addr


# =========== CP0 ===========



def CACHE(base, op, offset):
    """ CACHE """
    cache = op & 0x3
    act = (op >> 2) & 0x7

def MTC0(rt, rd):
    """ MTC0 """
    result = rd = rt
    return result








    


