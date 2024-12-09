instruction_set = {
    "HLT": 0x00,
    "MOV": 0x01,
    "ADD": 0x02,
    "ADC": 0x03,
    "DEC": 0x04,
    "JNZ": 0x05,
}

register_set = {
    "EAX": 0x00,
    "EBX": 0x01,
    "ECX": 0x02,
    "EDX": 0x03,
    "EEX": 0x04,
}


def main():
    raw_code = open('example.txt', 'r')
    output = open('output.txt', 'w')
    is_data = False
    instruction_count=0
    data_count=0
    section_dict={}
    for line in raw_code:
        line = line.strip()
        if "section" in line:
                if ".data" in line:
                    is_data = True
                    continue
                else:
                    is_data = False
                    section_dict.update({line.split(".")[1]: instruction_count} )
                    continue
                                    
        if is_data == True:
            number = line.split()
            for i in range (int(number[0])+1):
                output.write(bin(i)[2:].zfill(8) + ' ' + bin(int(number[i]))[2:].zfill(8) + '\n')
        elif is_data == False: 
            if line != "":
                instruction_count+=1
        is_data = False
    print(section_dict)
    instruction_count=0
    output.write('\n')
    raw_code.close()
    raw_code = open('example.txt', 'r')
    counter=0
    for line in raw_code:
        opr_1=bin(0)[2:].zfill(8)
        adr_1=bin(1)[2:].zfill(2)
        opr_2=bin(0)[2:].zfill(8)
        adr_2=bin(1)[2:].zfill(2)
        line = line.strip()
        if line == "":
            continue
        if "section" in line:
            is_data = False
            if "section .data"  in  line:
                is_data = True
            continue
        if  is_data == True:
            continue
        com_line=line.split()
        com_len=len(com_line)
        print(com_line)
        num=bin(counter)[2:].zfill(8)
        command=bin(instruction_set[com_line[0]])[2:].zfill(4)
        if com_len > 1:
            if com_line[1].strip("[]") in register_set:
                opr_1=bin(register_set[com_line[1].strip("[]")])[2:].zfill(8)
                if "[" in com_line[1]:
                    adr_1=bin(3)[2:].zfill(2)
                else:
                    adr_1=bin(2)[2:].zfill(2)
            else:
                opr_1=bin(int(com_line[1].strip("[]")))[2:].zfill(8)
                if "[" in com_line[1]:
                    adr_1=bin(0)[2:].zfill(2)
                else:
                    adr_1=bin(1)[2:].zfill(2)
        if com_len > 2:
            if com_line[2].strip("[]") in register_set:
                opr_2=bin(register_set[com_line[2].strip("[]")])[2:].zfill(8)
                if "[" in com_line[2]:
                    adr_2=bin(3)[2:].zfill(2)
                else:
                    adr_2=bin(2)[2:].zfill(2)
            elif com_line[2] in section_dict:
                adr_2=bin(1)[2:].zfill(2)
                opr_2=bin(section_dict[com_line[2]])[2:].zfill(8)
            else:
                opr_2=bin(int(com_line[2].strip("[]")))[2:].zfill(8)
                if "[" in com_line[2]:
                    adr_2=bin(0)[2:].zfill(2)
                else:
                    adr_2=bin(1)[2:].zfill(2)
        counter=counter + 1 
        print(num, command, adr_1, opr_1, adr_2, opr_2)
        output.write(num + ' ' + command + ' ' + adr_1 + ' ' + opr_1 + ' ' + adr_2 + ' ' + opr_2 +  '\n')

import sys
if __name__ == "__main__":
  main()

    

            
      
                 
    
            
                 
