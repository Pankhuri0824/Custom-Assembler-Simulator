
def binary(a):
	a = int(a)

	a = str(bin(a))

	a = a[2:]
	a = "0"*(7-len(a)) + a

	return a

opcode_table = {
	"add": ("00000", "A"),
	"sub": ("00001", "A"),
	"mov": (("00010", "B"), ("00011", "C")),
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


type_table = {"A" : 2 , "B" : 1 , "C" : 5 , "D" : 1 ,"E" : 4 , "F":11}

reg_table = { "R0" : "000" ,  "R1" : "001",  "R2" : "010",  "R3" : "011",  "R4" : "100",  "R5" : "101", "R6" : "110", "flags" : "111","FLAGS":"111"}

variables= {}

labels={}

count =0
const = 2**16 -1
errro_hai = 0
hlt_there = 0
hlt_error = 0

errors =[ ]
output =[ ]
data = ""


while True:
	try:
		line = input()
		line.strip()
		data += line + "\n"	
	except EOFError:
		break


def binary_code(f):
	global errro_hai , hlt_there , hlt_error,count
	counter =len(variables) 



	for line in f[len(variables):]:
		if line == "\n" or len(line.split()) == 0: continue
		counter+=1

		if hlt_there ==1 and hlt_error == 0:
			errro_hai =1
			errors.append("Error: Instructions after  hlt instruction\n")
			hlt_error =1
			continue

		words = line.split()


		if opcode_table.get(words[0] , 0) == 0 :
			if words[0] == "var" :
				errro_hai=1
				errors.append("Error on line " + str(counter) + " , variable declared in between code\n")
				continue


			if words[0][:-1] in labels :
				counter-=1
				continue

			errro_hai =1
			errors.append("Invalid operation specified on line " + str(counter) +"\n")
			continue

		ans = ""

		mov_check =0

		if words[0] == "mov":
			if len(words )!= 3 :
				errro_hai = 1
				errors.append("Error on line" + str(counter) + ": Invlid number of operands " + "\n")
				continue

			if words[-1][0] == "$":
				typee = "B"
				ans += opcode_table[words[0]][0][0]
			else:
				typee = "C"
				ans += opcode_table[words[0]][1][0]
			mov_check= 1

		if mov_check == 0  :
			typee = opcode_table[words[0]][1]
			ans += opcode_table[words[0]][0]

		if typee == "A":
			if len(words) != 4 :
				errro_hai = 1
				errors.append("Invalid number of operands on line " + str(counter) + "\n")
				continue

			a,b,c = words[1:]
			if a.lower()== "flags" or b.lower() == "flags" or c.lower() == "flags" :
				errro_hai=1
				errors.append("Illegal use of flags register on line " + str(counter) + "\n")
				continue

			if reg_table.get(a,0) == 0 or reg_table.get(b, 0) ==0 or reg_table.get(c,0) == 0:
				errro_hai = 1
				errors.append("Invalid code on line " + str(counter) +" Invalid name of register"+"\n")
				continue



			ans += "0"*type_table[typee]

			ans+= reg_table[a]
			ans+= reg_table[b]
			ans+= reg_table[c]

			output.append(ans)
			

		elif typee == "B":
			if len(words) != 3 :
				errro_hai = 1
				errors.append("Invalid number of operands on line "+ str(counter) + "\n")
				continue

			a,b= words[1:]

			if a.lower() == "flags":
				errro_hai=1
				errors.append("Error on line " + str(counter) + ", illegal use of flags register\n")
				continue
			if reg_table.get(a,0) == 0:
				errro_hai = 1
				errors.append("Invalid code on line " + str(counter) +" ,Invalid register name\n")
				continue


			ans += "0"*type_table[typee]

			ans+= reg_table[a]

			if(b[0] != "$" or not  b[1:].isdigit()):
				errro_hai = 1
				errors.append("Invalid code on line " + str(counter) + " ,invlaid syntax of immmediate value\n")
				continue

			if int(b[1:]) >127 or int(b[1:]) < 0 :
				errro_hai =1
				errors.append("Error on line " + str(counter) + ", overflowing value of immediate\n")
				continue

			ans += binary(int(b[1:]))

			output.append(ans)
			

		elif typee == "C":

			if len(words) != 3 :
				errro_hai = 1
				errors.append("Invalid number of operands on line " + str(counter) + "\n")
				continue

			a,b = words[1:]

			if words[0] == "mov":
				if a.lower() == "flags":
					errro_hai=1
					errors.append("Error on line " + str(counter) + ", illegal use of flags register\n")
					continue
			else :
				if a.lower() == "flags" or b.lower() == "flags":
					errro_hai=1
					errors.append("Error on line " + str(counter) + ", illegal use of flags register\n")
					continue

			if reg_table.get(a,0) == 0 or reg_table.get(b, 0) ==0:
				errro_hai =1
				errors.append("Invalid code on line " + str(counter) +  " , invalidn register names\n")
				continue


			ans += "0"*type_table[typee]

			ans+= reg_table[a]
			ans+= reg_table[b]

			output.append(ans)
			

		elif typee == "D":
			if len(words) != 3 :
				errro_hai = 1
				errors.append("Invalid number of operands on line " + str(counter) + "\n")
				continue

			a,b= words[1:]

			if a.lower() == "flags":
				errro_hai=1
				errors.append("Error on line " + str(counter) + ", illegal use of flags register\n")
				continue

			if reg_table.get(a,0) == 0:
				errro_hai =1
				errors.append("Invalid code on line " + str(counter) + " , invalidn register names\n")
				continue


			ans += "0"*type_table[typee]

			ans+= reg_table[a]

			if(variables.get(b,0) == 0):
				errro_hai =1
				errors.append("Invalid code on line "  + str(counter) + ", variable not defined\n")
				continue

			ans += variables[b][0]

			output.append(ans)

			


		elif typee =="E":

			if len(words) != 2 :
				errro_hai = 1
				errors.append("Invalid number of operands on line "+ str(counter) + "\n")
				continue

			a = words[1:][0]

			if labels.get(a,0) == 0:
				errro_hai = 1
				errors.append("Invalid code on line " + str(counter) +", label not defined\n")
				continue

			ans += "0"*type_table[typee]

			ans += labels[a][0]

			output.append(ans)
			

		elif typee == "F":
			hlt_there =1
			ans += "0"*type_table[typee]
			output.append(ans)
			
def variables_declare(f,c,label,z):
	global errro_hai , count
	c-=z
	initial =  c

	if initial >= 127:
		error_hai = 1
		errors.append("Number of lines excced 127" + "\n")
	
	for line in f:
		if line == "\n"  or len(line.split()) == 0: continue
		c+=1
		words = line.split()

		if words[0] != "var" : break
		if len(words) != 2 :
			errro_hai = 1
			errors.append("Invalid declaration of variables on line : " + str(c -initial) + "\n")
			continue

		a = words[-1]

		if variables.get(a, 0) != 0 :
			errro_hai = 1
			errors.append("same variable declared more than once :" + str(a) + "\n")
		else:
			variables[a] = c



	l = len(variables.values()) + z

	for i in variables:
		j = variables[i]
		variables[i] = [binary(j-l) , 0]




	count  = c - initial
	a = len(variables)  + z

	for k,val in enumerate(label):
		i,j = val

		labels[i] = [binary(j-a-k + 1) , j-a-k + 1]

	binary_code(f)

def labels_declare(f):
	global errro_hai
	c =0
	label =[]
	a =[]
	z=0
	d = f
	
	
	for i in range(len(d)) :
		a.append(d[i])

		if d[i] == ":":
			a.append("\n")
			z+=1
	f="".join(a).split("\n") 
	for line in f:
		if line == "\n"  or len(line.split()) == 0: continue
		c+=1
		words = line.split()
		if words[0][-1] != ":" : continue

		if  words == [":"] or len(words) !=1:
			errro_hai =1
			errors.append("Invalid declaration of label , " + words[0][:-1] + "\n")

		else:
			if words[0][:-1] in label:
				errro_hai = 1
				errors.append("same label declared more than once: " + words[0][:-1] + "\n")
			else:
				label.append([str(words[0][:-1]) ,c])

	variables_declare(f,c+1 , label ,z)

labels_declare(data)


if hlt_there == 0:
	errors.append("Error , no hlt function present in the code\n")

if errro_hai !=0 or hlt_there == 0 :
	for i in errors:
		print(i)
else : 
	for i in output:
		print(i)

 