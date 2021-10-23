#!/usr/bin/env python3
# c-basic-offset: 4; tab-width: 8; indent-tabs-mode: nil
# vi: set shiftwidth=4 tabstop=8 expandtab:
# :indentSize=4:tabSize=8:noTabs=true:
#
# SPDX-License-Identifier: GPL-3.0-or-later
#     
#----Miguel Benavides---- Rolando Araujo-----
import re

opcode = {'add': '0000','addi':'0001', 'and':'0010', 'andi':'0011', 'beq':'0100',
          'bne':'0101', 'j':'0110', 'jal':'0111', 'jr':'1010', 'lb':'1011',
          'or':'1100', 'sb':'1101', 'sll':'1110', 'srl':'1111' }

tags = {'MAIN':'00000001', 'EXIT':'00001111', 'FUNC':'00001000','INC':'00000100', 'DEC':'00001001'}

reg = {'x0':'000', 'x1':'001', 'x2':'010',
        'x3':'011','x4':'100','x5':'101','x6':'110','x7':'111'}

label = {'MAIN': 1, 'EXIT':15,  'INC':4,  'DEC':9,  'FUNC':8}

regex = re.compile(r"(?P<label>[A-Z]*)?\:?\t?\s*(?P<nem>[^,]*),\s*(?P<item1>[^,]*),\s*(?P<item2>[^,]*),\s*(?P<item3>[^,]*)\n?")

def check_str(text):
    text = text.replace('\t','').strip()
    regex_match = regex.match(text)
    if not regex_match:
        raise Exception("Entered text '%s' is not valid"%(text))
    return regex_match.groupdict()

def strto(cad):
    
    if "x" in cad:
        aux = int(cad,16)
        return aux
    else:
        return int(cad)


def convert(x):
    if x < 0:
        return bin(x & (2**8-1))[2:].zfill(8)
        
    else:
        return (format(x,'08b'))


fname = input("Ingrese el nombre del archivo: ")
newfile = input("Ingrese el nombre del archivo a generar: ")

f = open(fname,"r")
f2 = open(newfile,"w")
lines = f.readlines()
count = 0
for lines in lines:
    
    result = lines.replace(':','')
    ele = check_str(result)

   #count+=1
    
    if  (ele['nem'] == 'addi'):
        num = strto(ele['item3'])
        content = opcode['addi'] + reg[ele['item2']] + reg[ele['item1']] + convert(num)
        f2.write(content)
        f2.write("\n")
    elif  (ele['nem'] == 'add'):
        content = opcode['add'] + reg[ele['item2']] + reg[ele['item3']] + reg[ele['item1']] + '00000'
        f2.write(content)
        f2.write("\n")
    elif  (ele['nem'] == 'andi'):
        num = strto(ele['item3'])
        content = opcode['andi'] + reg[ele['item2']] + reg[ele['item1']] + convert(num)
        f2.write(content)
        f2.write("\n")    
    elif  (ele['nem'] == 'and'):
        content = opcode['and'] + reg[ele['item2']] + reg[ele['item3']] + reg[ele['item1']] + '00000'
        f2.write(content)
        f2.write("\n")
    elif  (ele['nem'] == 'or'):
        content = opcode['or'] + reg[ele['item2']] + reg[ele['item3']] + reg[ele['item1']] + '00000'
        f2.write(content)
        f2.write("\n")
    elif  (ele['nem'] == 'sll'):
        content = opcode['sll'] + reg[ele['item2']] + reg[ele['item3']] + reg[ele['item1']] + '00000'
        f2.write(content)
        f2.write("\n")
    elif  (ele['nem'] == 'srl'):
        content = opcode['srl'] + reg[ele['item2']] + reg[ele['item3']] + reg[ele['item1']] + '00000'
        f2.write(content)
        f2.write("\n") 
    elif  (ele['nem'] == 'beq'):
        num = label[ele['item3']] - count
        content = opcode['beq'] + reg[ele['item1']] + reg[ele['item2']] +convert(num)
        f2.write(content)
        f2.write("\n")   
    elif  (ele['nem'] == 'bne'):
        num = label[ele['item3']] - count
        content = opcode['bne'] + reg[ele['item1']] + reg[ele['item2']] + convert(num)
        f2.write(content)
        f2.write("\n")      
    elif  (ele['nem'] == 'lb'):
        num = strto(ele['item2'])
        content = opcode['lb'] + reg[ele['item3']] + reg[ele['item1']] + convert(num) 
        f2.write(content)
        f2.write("\n")   
    elif  (ele['nem'] == 'sb'):
        num = strto(ele['item2'])
        content = opcode['sb'] + reg[ele['item3']] + reg[ele['item1']] + convert(num)
        f2.write(content)
        f2.write("\n")   
    elif  (ele['nem'] == 'j'):
        content = opcode['j'] + '000000' + tags[ele['nem']] 
        f2.write(content)
        f2.write("\n")  
    elif  (ele['nem'] == 'jal'):
        content = opcode['jal'] +'000000'+ tags[ele['nem']]
        f2.write(content)
        f2.write("\n")  
    elif  (ele['nem'] == 'jr'):
        content = opcode['jr'] + reg[ele['item1']]+'00000000000'
        f2.write(content)
        f2.write("\n")
    count = count + 1
f.close()

