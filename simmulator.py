def binary(a,n):
	a = int(a)

	a = str(bin(a))

	a = a[2:]
	a = "0"*(n-len(a)) + a

	return a

opcode_table = {
	"add": ("00000", "A"),
	"sub": ("00001", "A"),
	"ld": ("00100", "D"),
	"st": ("00101", "D"),
	"mul": ("00110", "A"),
	"div": ("00111", "C"),
	"rs": ("01000", "B"),
	"ls": ("01001", "B"),
	"xor": ("01010", "A"),
	"or": ("01011", "A"),
	"and": ("01100", "A"),
	"not": ("01101", "C"),
	"cmp": ("01110", "C"),
	"jmp": ("01111", "E"),
	"jlt": ("11100", "E"),
	"jgt": ("11101", "E"),
	"je": ("11111", "E"),
	"hlt": ("11010", "F")
	}

opcode_table = {opcode_table[k][0]:(k , opcode_table[k][1]) for k in opcode_table}
opcode_table["00010"] = ("mov" , "B")
opcode_table["00011" ]= ("mov" , "C")


type_table = {"A" : 2 , "B" : 1 , "C" : 5 , "D" : 1 ,"E" : 4 , "F":11}

reg_table = { "R0" : "000" ,  "R1" : "001",  "R2" : "010",  "R3" : "011",  "R4" : "100",  "R5" : "101", "R6" : "110", "flags" : "111",}
reg_data = {k:0 for k in reg_table} 
reg_table = {reg_table[k]:k for k in reg_table}


variables= {}

labels={}

count =0
const = 2**16 -1
pc =0
data = ""
k=1
temp =0 
f=0

def typee_A(op ,a,b,c):
	if op == "add" :
		reg_data[a] = reg_data[b] + reg_data[c]
		reg_data["flags"] = 0
		if reg_data[a] >const or reg_data[a] < 0:
			reg_data[a] =0
			reg_data["flags"] |= 8

	elif op == "mul" :
		reg_data[a] = reg_data[b] * reg_data[c]
		reg_data["flags"] = 0
		if reg_data[a] >const or reg_data[a] < 0:
			reg_data[a] =0
			reg_data["flags"] |= 8

	elif op == "sub" :
		reg_data[a] = reg_data[b] - reg_data[c]
		reg_data["flags"] = 0
		if reg_data[a] >const or reg_data[a] < 0:
			reg_data[a] =0
			reg_data["flags"] |= 8

	elif op == "xor" :
		reg_data["flags"] = 0
		reg_data[a] = reg_data[b] ^ reg_data[c]
	elif op == "or" :
		reg_data["flags"] = 0
		reg_data[a] = reg_data[b] | reg_data[c]
	elif op == "and" :
		reg_data["flags"] = 0
		reg_data[a] = reg_data[b] & reg_data[c]

def typee_B(op ,a , val):
	
	if op == "mov":
		if val > 127 or val < 0:
			reg_data[a] =0
		else : reg_data[a] =val

	elif op == "rs":
		reg_data[a] //= 2**val
	elif op == "ls":
		reg_data[a] *= 2**val
		reg_data[a] =   int(str(bin(reg_data[a]))[2:][:7],2)
	reg_data["flags"] = 0

def typee_C(op,a,b):
	if op == "mov":
		reg_data[a] = reg_data[b]
		reg_data["flags"] = 0
	elif op == "div":
		reg_data["flags"] = 0
		if reg_data[b] ==0 :
			reg_data["flags"] |= 8
			reg_data["R0"] = 0
			reg_data["R1"] = 0
		else:
			reg_data["flags"] = 0
			reg_data["R0"] = reg_data[a] // reg_data[b]
			reg_data["R1"] = reg_data[a] % reg_data[b]
	elif op == "not":
		reg_data["flags"] = 0
		reg_data[a] = ~ reg_data[b]
	elif op == "cmp":
		reg_data["flags"] = 0
		if reg_data[a] == reg_data[b]:
			reg_data["flags"] |= 1
		elif reg_data[a] > reg_data[b]:
			reg_data["flags"] |= 2
		elif reg_data[a] < reg_data[b]:
			reg_data["flags"] |= 4

def typee_D(op , a, val):
	reg_data["flags"] = 0
	if op == "ld":
		reg_data[a] = variables.get(val,0)
	elif op == "st":
		variables[val] = reg_data[a]

def typee_E(op,val):
	global temp,f
	if op == "jmp":
		temp = val-1
	elif op == "jlt":
		if reg_data["flags"] & 4 == 4:
			temp = val-1
		else : 
			f=1
	elif op == "jgt":
		if reg_data["flags"] & 2 == 2:
			temp = val -1
		else : 
			f=1
	elif op == "je":
		if reg_data["flags"] & 1 == 1:
			temp = val-1
		else : 
			f=1
	else : 
		f=1
	reg_data["flags"] = 0

# automatic testing
while True:
	try:
		line = input()
		if line =="exit" : break
		line.strip()
		data += line + "\n"	
	except EOFError:
		break

data = data.split("\n")[:-1]


while(k):
	line = data[pc]	
	opcode = line[:5]
	typee = opcode_table[opcode][1]
	op = opcode_table[opcode][0]
	filler = type_table[typee]

	if typee == "A":
		a = reg_table[line[5+filler:8+filler]]
		b = reg_table[line[5+filler+3:8+filler+3]]
		c = reg_table[line[5+filler+6:8+filler+6]]

		typee_A(op,a,b,c)

	elif typee == "B":
		a = reg_table[line[5+filler:8+filler]]
		val=int(line[-7:],2)

		typee_B(op,a,val)

	elif typee == "C":
		a = reg_table[line[5+filler:8+filler]]
		b = reg_table[line[8+filler:11+filler]]
		typee_C(op,a,b)

	elif typee == "D":
		a = reg_table[line[5+filler:8+filler]]
		val=int(line[-7:],2)

		typee_D(op,a,val)

	elif typee =="E":

		val=int(line[-7:],2)
		typee_E(op,val)
		# exit()
		
	else : k=0

	print(binary(pc,7) + "       " , end="")
	for i in reg_data:
		print(" "+binary(reg_data[i], 16) , end="")
	print()
	if typee == "E" and f!=1:
		pc = temp
	pc +=1
	

for i in data:
	print(i.strip())
for i in variables:
	print(binary(variables[i] , 16))

for i in range(128 - len(data) - len(variables)):
	print("0"*16)




	



