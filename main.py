import sys
import re
import fileinput

# check for input error
if len(sys.argv) != 2:
	print("Requires only the file name")
	sys.exit(1)

# converting output file from .asm to .hack
input_filename = sys.argv[1]
output_filename = input_filename.split('.')[0] + '.hack'

# initialize symbol table
symbols = {
	"R0": 0,
	"R1": 1,
	"R2": 2,
	"R3": 3,
	"R4": 4,
	"R5": 5,
	"R6": 6,
	"R7": 7,
	"R8": 8,
	"R9": 9,
	"R10": 10,
	"R11": 11,
	"R12": 12,
	"R13": 13,
	"R14": 14,
	"R15": 15,
	"SP": 0,
	"LCL": 1,
	"ARG": 2,
	"THIS": 3,
	"THAT": 4,
	"SCREEN": 16384,
	"KBD": 24576,
}
symbol_count = 16
line_number = 1

comp = {
	"0": "101010",
	"1": "111111",
	"-1": "111010",
	"D": "001100",
	"A": "110000",
	"M": "110000",
	"!D": "001101",
	"!A": "110001",
	"!M": "110001",
	"-D": "001111",
	"-A": "110011",
	"-M": "110011",
	"D+1": "011111",
	"A+1": "110111",
	"M+1": "110111",
	"D-1": "001110",
	"A-1": "110111",
	"M+1": "110111",
	"D-1": "001110",
	"A-1": "110010",
	"M-1": "110010",
	"D+A": "000010",
	"D+M": "000010",
	"D-A": "010011",
	"D-M": "010011",
	"A-D": "000111",
	"M-D": "000111",
	"D&A": "000000",
	"D&M": "000000",
	"D|A": "010101",
	"D|M": "010101"
}

dest = {
	None: "000",
	"M": "001",
	"D": "010",
	"MD": "011",
	"A": "100",
	"AM": "101",
	"AD": "110",
	"AMD": "111"
}

jump = {
	None: "000",
	"JGT": "001",
	"JEQ": "010",
	"JGE": "011",
	"JLT": "100",
	"JNE": "101",
	"JLE": "110",
	"JMP": "111"
}

def handleLInstruction(command):
	global line_number, symbols
	storage = command[0].strip("()")
	number = symbols.get(storage)
	if number is None:
		next_line = line_number - 1
		symbols[storage] = next_line
		number = next_line

# strip away comment and whitespaces, and add labels to symbol table
with open(input_filename, 'r') as input_file:
	with open(output_filename, 'w') as output_file:
		for line in input_file:
			stripped_line = line.strip().replace(" ", "")
			no_comment_stripped_line = stripped_line.split("//")[0].strip()
			if no_comment_stripped_line and not no_comment_stripped_line.startswith("//"):
				tokens = re.findall(r"[;@=]|[^\s@=;]+", line.strip())
				if tokens[0].startswith("(") and tokens[0].endswith(")"):
					handleLInstruction(tokens)
				else:
					output_file.write(no_comment_stripped_line + '\n')
					line_number += 1

def handleAInstruction(command):
	global symbol_count, symbols
	storage = command[1]
	if (storage.isnumeric()):
		number = int(storage)
	else:
		number = symbols.get(storage)
		if number is None:
			symbols[storage] = symbol_count
			number = symbol_count
			symbol_count += 1

	return format(number, '016b')

def handleCInstruction(command):
	global symbol_count, symbols, comp, dest, jump
	line = "111"

	if "=" in command and len(command) == 3:
		computation = command[2]
		if "M" in computation:
			line += "1"
		else:
			line += "0"
		line += comp.get(computation)

		destination = command[0]
		line += dest.get(destination)
		line += "000"
	elif ";" in command and len(command) == 3:
		computation = command[0]
		if "M" in computation:
			line += "1"
		else:
			line += "0"
		line += comp.get(computation)
		line += "000"
		jmp = command[2]
		line += jump.get(jmp)
	else:
		computation = command[2]
		if "M" in computation:
			line += "1"
		else:
			line += "0"
		line += comp.get(computation)
		destination = command[0]
		line += dest.get(destination)
		jmp = command[4]
		line += jump.get(jmp)

	return line

# second run
with fileinput.FileInput(output_filename, inplace=True) as output_file:
    for line in output_file:
        tokens = re.findall(r"[;@=]|[^\s@=;]+", line.strip())
        if tokens[0] == '@':
            print(handleAInstruction(tokens))
        else:
            print(handleCInstruction(tokens))

input_file.close()
output_file.close()