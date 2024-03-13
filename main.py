import sys
import re

# check for input error
if len(sys.argv) != 2:
	print("Requires only the file name")
	sys.exit(1)

# converting output file from .asm to .hack
input_filename = sys.argv[1]
output_filename = input_filename.split('.')[0] + '.hack'
print(output_filename)

# strip away comment and whitespaces
with open(input_filename, 'r') as input_file:
	with open(output_filename, 'w') as output_file:
		for line in input_file:
			stripped_line = line.strip()
			if stripped_line and not stripped_line.startswith("//"):
				output_file.write(stripped_line + '\n')

with open(output_filename, 'r+') as output_file:
	output_file.seek(0)

	for line in output_file:
		tokens = re.findall(r"[;@=+-]|[^\s@=;+-]+", line.strip())
		print(tokens)