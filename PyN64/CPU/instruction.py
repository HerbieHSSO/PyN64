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
    
    rd = sign_extend(rt << sa,32)
    
    return rd

def SRL(rd, rt, sa):
    """ SRL """
    
    rd = rt >> sa
    
    return rd

def SRA(rd, rt, sa):
    """ SRA """
    
    rd = rt >> sa
    
    return rd

def SLLV(rd, rt, rs):
    """ SLLV """
    
    rd = sign_extend(rt << (rs & 0x1f),32)

    return rd

def SRLV(rd, rt, rs):
    """ SRLV """
    
    rd = sign_extend(rt >> (rs & 0x1f),32)
    
    return rd

def SRAV(rd, rt, rs):
    """ SRAV """
    
    rd = rt >> rs
    
    return rd

def JR(rs):
    """ JR """
    
    pc = rs
    if pc < 0:
        pc = abs(pc)
 
    return pc 

def JALR(rs, pc):
    """ JALR """
  
    
    ra = pc + 8 

    pc = rs
    
    return ra

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
    
    return rd

def DIVU(rs, rt):
    """ DIVU """
    
    rd = rs/rt
    
    return rd

def DMULT(rs, rt):
    """ DMULT """
    
    rd = rs * rt
    
    return rd

def DMULTU(rs, rt):
    """ DMULTU """
    
    rd = rs * rt
    
    return rd

def DDIV(rs, rt):
    """ DDIV """
    
    rd = rs/rt
    
    return rd

def DDIVU(rs, rt):
    """ DDIVU """
    
    rd = rs/rt
    
    return rd

def ADD(rd, rs, rt):
    """ ADD """
    
    return rs + rt

def ADDU(rd, rs, rt):
    """ ADDU """



    return LoSigned(LoSigned(rs & 0xffffffff) + LoSigned(rt & 0xffffffff) & 0xffffffff)

def SUB(rd, rs, rt):
    """ SUB """
    
    rd = rs - rt
    
    return rd

def SUBU(rd, rs, rt):
    """ SUBU """
    
    rd = rs - rt
    
    return rd

def AND(rd, rs, rt):
    """ AND """
    
    rd = rs & rt

    return rd

def OR(rd, rs, rt):
    """ OR """
    
    rd = sign_extend(rs | rt, 32)

    return rd

def XOR(rd, rs, rt):
    """ XOR """
    print(rs, rt)
    print(rs ^ rt)
    rd = sign_extend(sign_extend(rs & 0xffffffff,32) ^ sign_extend(rt & 0xffffffff,32) & 0xffffffff,32)

    return rd

def NOR(rd, rs, rt):
    """ NOR """
    
    rd = ~(rs | rt)
    
    return rd

def SLT(rd, rs, rt):
    """ SLT """
    
    if rs < rt:
        rd = 1
    else:
        rd = 0
    
    return rd

def SLTU(rd, rs, rt):
    """ SLTU """
    
    if signToUnsign(rs, 32) < signToUnsign(rt, 32):
        return 1
    else:
        return 0

   

def DADD(rd, rs, rt):
    """ DADD """
    
    rd = rs + rt
    
    return rd

def DADDU(rd, rs, rt):
    """ DADDU """
    
    rd = rs + rt
    
    return rd

def DSUB(rd, rs, rt):
    """ DSUB """
    
    rd = rs - rt
    
    return rd

def DSUBU(rd, rs, rt):
    """ DSUBU """
    
    rd = rs - rt
    
    return rd

def TEQ(rs, rt):
    """ TEQ """
    
    if rs == rt:
        return 'Exception'
    
    return None

def DSLL(rd, rt, sa):
    """ DSLL """
    
    rd = rt << sa
    
    return rd

def DSRL(rd, rt, sa):
    """ DSRL """
    
    rd = rt >> sa
    
    return rd

def DSRA(rd, rt, sa):
    """ DSRA """
    
    rd = rt >> sa
    
    return rd



def BLTZ(rd, offset, pc):
    """ BLTZ """
    offset = str(offset) + '00'
    if rd < 0:
        pc = pc + int(offset, 2)
    return pc

def BGEZ(rd, offset, pc):
    """ BGEZ """
    offset = str(offset) + '00'
    if rd >= 0:
        pc = pc + int(offset, 2)
    return pc + 4

def BGEZAL(rs, target, pc):
    """ BGEZAL """
    target = sign_extend(target << 2, 18)
    #pc = pc + 8
    if rs <= 0:
        pc = pc + target
        return pc
        

    else:
        return pc + 4
        

def J(target, pc):
    """ J """
    pc = target * 4
    return pc

def JAL(target, pc):
    """ JAL """
 
    #pc = 0x80245000 | (target << 2) & 0xFFFF
 
    pc = 0x80000000 + (target << 2) 
   
    return int(pc) 

def BEQ(rs, rt, target, pc):
    """ BEQ """

    target = sign_extend(target << 2, 18)

    if rs == rt:
        
        pc = pc + target
        return pc
    else:
        return pc + 4

def BEQL(rs, rt, target, pc):
    """ BEQL """
    if rs != rt:
        
        pc = pc + target
        return pc + 4
    else:
        return pc + 8


def BNE(rs, rt, target, pc):
    """ BNE """

    target = sign_extend(target << 2, 18)
    
    if (rs & 0xFFFF_FFFF) == (rt & 0xFFFF_FFFF) or (rs == rt):
        return pc + 4
        
    else:
        pc = pc + target
        return pc 
        

def BNEL(rs, rt, target, pc):
    """ BNEL """
 
    if rs != rt:
        
        pc = pc + target
        return pc
    else:
        return pc + 4 
    
def BLEZ(rs, target, pc):
    """ BLEZ """

    target = sign_extend(target << 2, 18)
    
    if (rs & 0xFFFF_FFFF) >= 0 or (rs >= 0):
        return pc + 4
        
    else:
        pc = pc + target
        return pc

@lru_cache(maxsize=128)
def BGTZ(rs, target, pc):
    """ BGTZ """
    if rs > 0:
        pc = pc + target
    return pc


def ADDI(rt, rs, imm):
    """ ADDI """    
    return rs + imm


def ADDIU(rt, rs, imm):
    """ ADDIU """
    #print(f'{rs} + {imm}')
    #print(f'{rs + sign_extend(imm, 16)}')

       
    return (rs + sign_extend(imm, 16))

@lru_cache(maxsize=1024)
def SLTI(rt, rs, imm):
    """ SLTI """
    
    if rs < imm:
        rt = 1
    else:
        rt = 0
    
    return rt
@lru_cache(maxsize=1024)
def SLTIU(rt, rs, imm):
    """ SLTIU """
    
    if rs < imm:
        rt = 1
    else:
        rt = 0
    
    return rt
@lru_cache(maxsize=128)
def ANDI(rt, rs, imm):
    """ ANDI """
    
    rt = rs & imm

    return rt


@lru_cache(maxsize=1024)
def ORI(rt, rs, imm):
    """ ORI """
    
    rt = rs | imm
    
    return rt

def XORI(rt, rs, imm):
    """ XORI """
    
    rt = rs ^ imm
    
    return rt

def LUI(rt, imm):
    """ LUI """
    #print(imm << 16)
    return imm << 16

def DADDI(rt, rs, imm):
    """ DADDI """
    rt = rs + imm
    return rt

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
    rt = base + target
    return rt

def LH(rt, base, target):
    """ LH """
    rt = base + target
    return rt

def LWL(rt, base, target):
    """ LWL """
    rt = (base & 0xFFFF_FFFF) + sign_extend(target, 16)
    return rt


def LW(rt, base, target):
    """ LW """
   
    rt = sign_extend(target, 16) + base
   
    return rt

def LBU(rt, base, target):
    """ LBU """
    rt = sign_extend(base + target,16)
  
    return rt

def LHU(rt, base, target):
    """ LHU """
    rt = base + target
    return rt

def LWR(rt, base, target):
    """ LWR """
    rt = base + target
    return rt

def LWU(rt, base, target):
    """ LWU """
    rt = base + target
    return rt

def SB(rt, base, target):
    """ SB """
    addr = base + target
    
    return addr

def SH(rt, base, target):
    """ SH """
    addr = base + target
    
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

def SDL(rt, base, target):
    """ SDL """
    addr = base + target
    
    return addr


# =========== CP0 ===========


@lru_cache(maxsize=128)
def CACHE(base, op, offset):
    """ CACHE """
    cache = op & 0x3
    act = (op >> 2) & 0x7

def MTC0(rt, rd):
    """ MTC0 """
    result = rd = rt
    return result







    



