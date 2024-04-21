v0 = a0 = a1 = t0 = t1 = t2 = s1 = s2 = s3 = s4 = s5 = s6 = s7 = zero = "0"

clk = 0

filename = "dump2.txt"

file = open(filename,"r")

mem = []
t = 0
if(filename == "dump2.txt"): 
  #i = 16

  t0 = "1"  # 1 to encode , 2 to decode
  string = "Hello World"
  a1 = "1100"
  a0 = "0"
  t1 = "0"
  t = 16

  input_ = [ord(i) for i in string]
  for i in  range(len(input_)//4 + 1):
    mem.append(input_[4*i:4*i+4])

  for index,i in enumerate(mem):
      element = ""
      for j in i:
        element += str(hex(j)[2:])
      mem[index] = element

  print("initial memory: ")
  for i in mem :
    print(i)

if (filename == "comgaming.txt"): 
  s2 = "100" # number to compute factorial of
  s1 = "1"
  s4 = "1"
  i = 3


registers = { 
  "00010" : v0, "00100" : a0 , "00101" : a1 , 
  "01000" : t0 , "01001" : t1, "10001" : s1, "10010" :  s2,  
  "01010" : t2, "10011" : s3 , "10100" : s4, "00000" : zero,
  "10111" : s7, "10101" : s5, "10110" : s6
}

# store them 

rf = {"rs" : 0 , "rt" : 0 , "rd" : 0}

def hextobinary(num):
  h = int(num, 16)
  return dectobinary(h)

def binarytohex(n):
    num = int(n, 2)
    hex_num = hex(num)[2:]
    return(hex_num)

def binarytodec(num):
  n = len(num) - 1
  number = 0
  while(n >= 0):
    if (num[len(num)-n-1] == "1"):
      number += 2**n
    n = n - 1
  return number

def dectobinary(num):
  binary_num = ""
  if (num == 0):
    return "0"
  while num>0:
    binary_num = str(num % 2) + binary_num
    num = num // 2
  return binary_num


def r_format(line):
  rf["rs"] = line[6:11]
  rf["rt"] = line[11:16]
  rf["rd"] = line[16:21]
  #global clk

  if(line[26:32] == "000010"): # srl
    shamt = line[21:26]
    shamt = binarytodec(shamt)
    rt = registers[rf["rt"]]
    #clk += 1
    for i in range(shamt): # ALU
      rt = "0" + rt
      rt = rt[:-1]
    rd = rt
    #clk += 1
    registers[rf["rd"]] = rd #WB

  elif(line[26:32] == "000000"): # sll
    shamt = line[21:26]
    shamt = binarytodec(shamt)
    rt = registers[rf["rt"]]
    #clk += 1
    for i in range(shamt): # ALU
      rt = rt + "0"
      rt = rt[1:]
    rd = rt
    #clk += 1
    registers[rf["rd"]] = rd #WB

  elif(line[26:32] == "100001"): # move
    #clk += 1
    rs = binarytodec(registers[rf["rs"]])
    rt = binarytodec(registers[rf["rt"]])
    rd = rs + rt
    rd = dectobinary(rd)
    #clk += 1
    registers[rf["rd"]] = rd


IMem = []


for line in file:
  IMem.append(line[0:32])

#if (filename == "dump.txt"):
  #i = 16
  
i = 0

while (i < len(IMem)):
  line = IMem[i]

  clk += 1

  if(line[0:6] == "000000"):
    #clk += 1
    r_format(line)
  
  elif(line[0:6] == "001000"): # addi
    #clk += 1
    rf["rs"] = line[6:11]
    rf["rt"] = line[11:16]
    imm = line[16:32]
    rs = registers[rf["rs"]] 
    rs = binarytodec(rs)
    imm = binarytodec(imm)
    #clk += 1
    rt = rs + imm
    rt = dectobinary(rt)
    #clk += 1
    registers[rf["rt"]] = rt

  elif(line[0:6] == "001001"): # li
    #clk += 1
    rf["rt"] = line[11:16]
    imm = line[16:32]
    rt = registers[rf["rt"]]
    imm = binarytodec(imm)
    #clk += 1
    rt = imm + 0
    rt = dectobinary(rt)
    #clk += 1
    registers[rf["rt"]] = rt

  
  elif(line[0:6] == "100011"): # lw
    #clk += 1
    rf["rt"] = line[11:16]
    rf["rs"] = line[6:11]
    imm = line[16:32]
    imm = binarytodec(imm)
    rs = registers[rf["rs"]]
    rs = binarytodec(rs)
    #clk += 1
    if((rs+imm)//4 < len(mem)):
      #clk += 1
      rt = mem[(rs + imm)//4]
      rt = hextobinary(rt)
      #clk += 1
      registers[rf["rt"]] = rt  

  elif(line[0:6] == "101011"): # sw
    #clk += 1
    rf["rt"] = line[11:16]
    rf["rs"] = line[6:11]
    rt = registers[rf["rt"]]
    imm = line[16:32]
    rs = registers[rf["rs"]]
    imm = binarytodec(imm)
    rs = binarytodec(rs)
    #clk += 1
    if ((rs+imm)//4 < len(mem)):
      rt = binarytohex(rt)
      #clk += 1
      mem[(imm + rs)//4] = rt

  elif(line[0:6] == "011100"): # mul
    #clk += 1
    rf["rs"] = line[6:11]
    rf["rt"] = line[11:16]
    rf["rd"] = line[16:21]
    rs = registers[rf["rs"]]
    rt = registers[rf["rt"]]
    rs = binarytodec(rs)
    rt = binarytodec(rt)
    #clk += 1
    rd = rs * rt
    rd = dectobinary(rd)
    #clk += 1
    registers[rf["rd"]] = rd

  elif(line[0:6] == "000100"): # beq
    #clk += 1
    rf["rt"] = line[11:16]
    rf["rs"] = line[6:11]
    imm = line[16:32]
    rt = registers[rf["rt"]]
    rs = registers[rf["rs"]]
    rt = binarytodec(rt)
    rs = binarytodec(rs)
    #clk += 1
    if(rt == rs):
      if (imm[0] == "1"):
        imm = binarytodec(imm[1:])
        i = i - imm
      elif (imm[0] == "0"):
        imm = binarytodec(imm[1:])
        i = i + imm
  
  elif(line[0:6] == "000010"): # j
    #clk += 1
    address = line[25:32]
    address = binarytodec(address) - t
    if(i < address):
      i = address 
    else:
      i = address - 1
  
  i = i + 1 

if(filename == "dump2.txt"):
  print()
  print("Final Memory: ")
  for i in mem :
    print(i)

if(filename == "comgaming.txt"):
  print(registers["10001"])

print()
print("Number of cycles", clk*5)