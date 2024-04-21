v0 = a0 = a1 = t0 = t1 = t2 = s1 = s2 = s3 = s4= s5 = s6 = s7= zero = "0"

clk = 0
stalls = False
t = 0
clk = 0

i_i = 0 # //
i_d = 0 # //

filename = "comgaming.txt"

file = open(filename,"r")

mem = []

if(filename == "dump2.txt"): 
  t = 16
  t0 = "1"  # 1 to encode , 2 to decode
  string = "Hello World"
  a1 = "1100"
  a0 = "0"
  t1 = "0"

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
  t = 1
  s2 = "100"  # number to calculate factorial of
  s1 = "1"
  s4 = "1"

registers = { 
  "00010" : v0, "00100" : a0 , "00101" : a1 , 
  "01000" : t0 , "01001" : t1, "10001" : s1, "10010" :  s2,  
  "01010" : t2, "10011" : s3 , "10100" : s4, "00000" : zero,
  "10111" : s7, "10101" : s5, "10110" : s6,
}

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

def check_dependences(rs, rt, rd,i):
  global stalls,i_i,i_d,d
  stalls = False
  line = ""
  for j in range(i - 3,i):
    if(j >= 0 and j < len(if_id)):
        line = if_id[j]["instruction"] # // line = IMem[j]
        if( (rs == line[6:11] or rs == line[11:16] or rs == line[16:21]) and rs != "00000"):
          i_i = j
          stalls = True
          print(rs)
        if((rt == line[6:11] or rt == line[11:16] or rt == line[16:21]) and rt != "00000" ):
          i_i = j
          stalls = True
          print(rt)
        if((rd == line[6:11] or rd == line[11:16] or rd == line[16:21]) and rd != "00000"):
          i_i = j 
          stalls = True
          print(rd)

  if(stalls):
    i_d = i
    # print(line)
    # print(IMem[d])
    # print(d)
    # print("hazard", i_i, i_d)

IMem = []

for index,line in enumerate(file):
  IMem.append(line[0:32])

IComp = [False for i in range(len(IMem))] # //

if_id = []
id_ex = []
ex_m = []
m_wb = []

def IF(line,k):
  global stalls
  #check_dependences(line[6:11],line[11:16],line[16:21],k) # //
  #if (not stalls):  # //
  if_id.append({"instruction" : line , "op_u_stalls" : False})

def ID(dict):
  global stalls
  line = dict["instruction"]
  temp = {
  "opcode" : "" , "shamt" : "", "mr" : 0, "wb" : 1, "mw" : 0, "cs" : 0, "j" : 0, "branch" : 0,  "writeregister" : "", "op1" : "", "op2" : "" ,
    "address" : "", "op_u_stalls" : False
  }

  if(dict["op_u_stalls"]):
    print("skipped")
    return 

  if(stalls):
    dict["op_u_stalls"] = True
  
  temp["opcode"] = line[0:6]

  if(temp["opcode"] == "000000"): # R
    temp["op1"] = registers[line[6:11]] #rs
    temp["op2"] = registers[line[11:16]] #rt
    temp["writeregister"] = line[16:21] #rd
    temp["shamt"] = line[21:26]
    if(line[26:32] == "000010"): # srl
      temp["cs"] = 2
    elif(line[26:32] == "000000"): # sll
      temp["cs"] = 1
    elif(line[26:32] == "100001"): # move
      temp["cs"] = 0

  elif(temp["opcode"] == "001000" or temp["opcode"] == "001001" or temp["opcode"] == "100011" or temp["opcode"] == "101011"): # addi li lw sw 
    temp["op1"] = registers[line[6:11]]
    temp["op2"] = line[16:32]
    temp["writeregister"] = line[11:16]
    temp["cs"] = 0
    if(temp["opcode"] == "100011" ): # lw
      temp["mr"] = 1
    if(temp["opcode"] == "101011"): # sw
      temp["mw"] = 1
      temp["wb"] = 0

  elif(temp["opcode"] == "011100"): # mul
    temp["op1"] = registers[line[16:21]]
    temp["op2"] = registers[line[11:16]]
    temp["writeregister"] = line[6:11]
    temp["cs"] = 4

  elif(temp["opcode"] == "000100"): # beq
    temp["op1"] = registers[line[6:11]]
    temp["op2"] = registers[line[11:16]]
    temp["address"] = line[16:32]
    op1 = binarytodec(temp["op1"])
    op2 = binarytodec(temp["op2"])
    result = op1 - op2
    if(result == 0):
      temp["branch"] = 1
    temp["wb"] = 0

  elif(temp["opcode"] == "000010"): # j
    temp["address"] = line[25:32]
    temp["j"] = 1
    temp["wb"] = 0

  id_ex.append(temp)
  
def EX(dict):
  global stalls
  temp = {
  "mr" : 0, "mw" : 0,"wb" : 1, "branch" : 0, "writeregister" : "" , "result" : "", "op_u_stalls" : False
  }
 
  if(dict["op_u_stalls"]):
    print("skipped")
    return 

  if(stalls):
    dict["op_u_stalls"] = True

  temp["mr"] = dict["mr"]
  temp["mw"] = dict["mw"]
  temp["wb"] = dict["wb"]
  temp["writeregister"] = dict["writeregister"]
  
  op1 = binarytodec(dict["op1"])
  op2 = binarytodec(dict["op2"])
  if(dict["cs"] == 0): # +
    temp["result"] = dectobinary(op1 + op2)

  elif(dict["cs"] == 4): # *
    temp["result"] = dectobinary(op1 * op2)

  elif(dict["cs"] == 2): # srl
    shamt = binarytodec(dict["shamt"])
    rt = dict["op2"]
    for _ in range(shamt): # ALU
      rt = "0" + rt
      rt = rt[:-1]
    temp["result"] = rt
  elif(dict["cs"] == 1): # sll
    shamt = binarytodec(dict["shamt"])
    rt = dict["op2"]
    for _ in range(shamt): # ALU
      rt = rt + "0"
      rt = rt[1:]
    temp["result"] = rt

  ex_m.append(temp)

def M(dict):
  global stalls
  temp = {
  "wb" : 1 , "writeregister" : "", "result" : "", "op_u_stalls" : False
  }

  if(dict["op_u_stalls"]):
    print("skipped")
    return 

  if(stalls):
    dict["op_u_stalls"] = True

  temp["writeregister"] = dict["writeregister"]
  temp["result"] = dict["result"]
  temp["wb"] = dict["wb"]
  if(dict["mw"] == 1): # sw
    if (binarytodec(dict["result"])//4 < len(mem)):
      rt = registers[dict["writeregister"]]
      rt = binarytohex(rt)
      mem[binarytodec(dict["result"])//4] = rt   
  elif(dict["mr"] == 1): # lw
    if (binarytodec(dict["result"])//4 < len(mem)):
      rt = hextobinary(mem[binarytodec(dict["result"])//4])
      temp["result"] = rt
  
  m_wb.append(temp)
  
def WB(dict,k):

  if(dict["op_u_stalls"]):
    print("skipped")
    return 
  
  if(stalls):
    dict["op_u_stalls"] = True

  if(dict["wb"] == 1):
    registers[dict["writeregister"]] = dict["result"]
  if(k<len(IMem)):
    IComp[k] = True # //



k = 0
d = 0

while(d < len(IMem)):

  IF(IMem[d], k)
  #print("fetched", d)
  
  if(k-1>=0):
    ID(if_id[k-1])
    #print("deocoded", k-1)
    if(id_ex[k-1]["j"]):
      d = binarytodec(id_ex[k-1]["address"]) - t
      if_id.pop()
      IF(IMem[d], k-1)

    elif(id_ex[k-1]["branch"]):
      d = d + binarytodec(id_ex[k-1]["address"])

  if(k-2>=0):
    EX(id_ex[k-2])
    #print("executed", k-2)

  if(k-3>=0):
    #print("mem", k-3)
    M(ex_m[k-3])
  
  if(k-4>=0):
    #print("wb", k-4)
    WB(m_wb[k-4],k-4)

  k = k + 1
  d = d + 1
   
if(filename == "dump2.txt"):
  print()
  print("Final Memory: ")
  for i in mem :
    print(i)

if(filename == "comgaming.txt"):
  print(registers["10001"])

print("Number of cycles", k)
