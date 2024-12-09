
# 0 - загрузка из памяти - число в квадратных скобках
# 1 - загрузка числа - число без квадратных скобок
# 2 - загрузка значения из регистра - название регистра без квадратных скобок
# 3 - загрузка из памяти по значению из регистра - название регистра в квадратных скобках

text = open('output.txt', 'r').read()

instruction_set_r = {
  0x00: "HLT",
  0x01: "MOV",
  0x02: "ADD",
  0x03: "ADC",
  0x04: "DEC",
  0x05: "JNZ",
}

reg_set = {
  0x00: "A",
  0x01: "B",
  0x02: "C",
  0x03: "D",
  0x04: "E",
}

adr_type = {0: "[num]", 1: "num", 2: "reg", 3: "[reg]"}


def main():
  pc = 0
  mem_inst = [0] * 256
  mem_data = [0] * 256
  cf = False
  regs = [0] * 5
  data_part, inst_part = text.split("\n\n")
  for line in data_part.split("\n"):
    if line == "":
      continue
    parts = line.split()
    mem_data[int(parts[0], 2)] = int(parts[1], 2)
  for line in inst_part.split("\n"):
    if line == "":
      continue
    parts = line.split()
    mem_inst[int(parts[0], 2)] = "".join(parts[1:]).zfill(24)
  while True:
    inst = mem_inst[pc]
    cmd_str = inst[:4] # 4
    adr1_str = inst[4:6] # 2
    op1_str = inst[6:14] # 8
    adr2_str = inst[14:16] # 2
    op2_str = inst[16:24] # 8

    cmd = int(cmd_str, 2)
    adr1 = int(adr1_str, 2)
    op1 = int(op1_str, 2)
    adr2 = int(adr2_str, 2)
    op2 = int(op2_str, 2)
    instName = instruction_set_r[int(cmd_str, 2)]
    adr1Type = adr_type[adr1]
    adr2Type = adr_type[adr2]

    if adr1Type == "reg":
      op1_str = reg_set[op1]
    else:
      op1_str = str(op1)
    if adr2Type == "reg":
      op2_str = reg_set[op2]
    else:
      op2_str = str(op2)

    print(f"PC:{pc}\tCMD:{instName}\t\tADR1:{adr1Type}\tOP1:{op1_str}\tADR2:{adr2Type}\tOP2:{op2_str}\tCF:{cf}\tREGS:{regs}")

    var1 = 0
    var2 = 0
    res = None

    if adr2Type == "num":
      var2 = op2
    elif adr2Type == "[num]":
      var2 = mem_data[op2]
    elif adr2Type == "reg":
      var2 = regs[op2]
    elif adr2Type == "[reg]":
      var2 = mem_data[regs[op2]]
    else:
      sys.exit("An error occurred")

    if instName != "HLT":
      if adr1Type == "num":
        sys.exit("An error occurred")
      elif adr1Type == "[num]":
        var1 = mem_data[op1]
      elif adr1Type == "reg":
        var1 = regs[op1]
      elif adr1Type == "[reg]":
        var1 = mem_data[regs[op1]]
      else:
        sys.exit("An error occurred")

    if instName == "HLT":
      break
    elif instName == "MOV":
      res = var2
    elif instName == "ADD":
      res = (var1 + var2) & 0xFF
      cf = (var1 + var2) > 0xFF
    elif instName == "ADC":
      res = (var1 + var2 + cf) & 0xFF
    elif instName == "DEC":
      res = var1 - 1
    elif instName == "JNZ":
      if var1 != 0:
        pc = var2
        continue

    if res is not None:
      if adr1Type == "num":
        sys.exit("An error occurred")
      elif adr1Type == "[num]":
        mem_data[op1] = res
      elif adr1Type == "reg":
        regs[op1] = res
      elif adr1Type == "[reg]":
        mem_data[regs[op1]] = res
      else:
        sys.exit("An error occurred")

    pc += 1


import sys
if __name__ == "__main__":
  main()
