"""
@author Alejandro Velez

Build a Modern Computer from First Principles Pt 1
by Hebrew University of Jerusalem

Project 6: The Assembler

Taken through Coursera
"""

class HackAssembler:
	# WARNING: main goal of this assembler for the hack computer is clarity and ease-of-use rather than being very performant
	# the intermediate results are being deleted after use, but commenting out those deletions can be very useful for debugging

	# hard-coded map of the binary codes for the different ALU operations
	_COMP_MAP = {
		"0": '101010',
		"1": '111111',
		"-1": '111010',
		"D": '001100',
		"A": '110000',
		"M": '110000',
		"!D": '001100',
		"!A": '110001',
		"!M": '110001',
		"-D": '001111',
		"-A": '110011',
		"-M": '110011',
		"D+1": '011111',
		"A+1": '110111',
		"M+1": '110111',
		"D-1": '001110',
		"A-1": '110010',
		"M-1": '110010',
		"D+A": '000010',
		"D+M": '000010',
		"D-A": '010011',
		"D-M": '010011',
		"A-D": '000111',
		"M-D": '000111',
		"D&A": '000000',
		"D&M": '000000',
		"D|A": '010101',
		"D|M": '010101'
	}

	# hard-coded map of the binary codes for different assignment destinations
	_DEST_MAP = {
		None: "000",
		"M": "001",
		"D": "010",
		"MD": "011",
		"A": "100",
		"AM": "101",
		"AD": "110",
		"AMD": "111"
	}

	# hard-coded map of the binary codes for different jump codes
	_JMP_MAP = {
		None: "000",
		"JGT": "001",
		"JEQ": "010",
		"JGE": "011",
		"JLT": "100",
		"JNE": "101",
		"JLE": "110",
		"JMP": "111"
	}

	def __init__(self, list_of_file_lines):
		self.symbol_table = {"R"+str(x):x for x in range(16)}
		self.symbol_table.update({str(x):x for x in range(16)})
		self.symbol_table.update({
			"SCREEN": 16384,
			"KBD": 24576,
			"SP": 0,
			"LCL": 1,
			"ARG":2,
			"THIS":3,
			"THAT":4
			})
		self.tokenized_instructions = []
		self.raw_input = list_of_file_lines
		self.pre_processed_input = []
		self.machine_language_output = []

	def parse_file_lines(self):
		"""
		preprocessing of the input file lines: remove whitespace and only retain lines with commands in them (`0th pass`)
		"""
		for line in self.raw_input:
			# remove lines containing no commands
			instruction = line.split("//")[0]
			instruction = instruction.replace(" ","")
			instruction = instruction.strip("\n") #EOL
			if not instruction:
				continue
			self.pre_processed_input.append(instruction)
		del self.raw_input  # free up memory

	def tokenize_file_lines(self):
		"""
		In addition to tokenizing for ease of future processing, we perform the functions of the first pass described in lecture. 
		We update the symbol table with the label symbols. (1st pass)
		"""
		num_labels = 0
		for number,instruction in enumerate(self.pre_processed_input):
			if instruction[0]=="(":
				# this is a label
				label = instruction[1:-1]
				address = number - num_labels
				self.symbol_table[label]=address # assign symbol to the current line number
				num_labels+=1
				continue
			else: # either A or C instruction, nothing to do in first pass, we simply tokenize for future convenience
				token = None
				if instruction[0]=="@":
					# A instruction
					token = ["A", instruction[1:]]
				else:
					# C instruction (dest = comp ; jump)
					dest = None  # use None when a field is not provided
					tmp = instruction # track instruction right of = sign
					if "=" in instruction:
						dest, tmp = instruction.split("=") # split into dest = ...
					comp = tmp
					jump = None
					if ";" in tmp:
						comp, jump = tmp.split(";")
					token = ["C", dest, comp, jump]
				self.tokenized_instructions.append(token)
		del self.pre_processed_input

	def second_pass(self):
		"""
		add variables to the symbol table (2nd pass)
		"""
		ct = 16 # first register a new var can point to
		for line_number, token in enumerate(self.tokenized_instructions):
			if token[0]=="A":
				# only A instructions can have var symbols
				arg = token[1]
				if not arg.isdigit():
					# it is a symbol
					symbol = arg
					if symbol not in self.symbol_table:
						self.symbol_table[symbol]=ct
						ct+=1
					token[1] = int(self.symbol_table[symbol])

	def convert_tokens_to_machine_language(self):
		"""
		final step: convert everything to machine language
		"""
		for instruction in self.tokenized_instructions:
			op_code = instruction[0]
			if op_code == "A":
				address_integer = int(instruction[1])
				binary_address = '{0:015b}'.format(address_integer)
				machine_language_instruction = "0"+binary_address
				self.machine_language_output.append(machine_language_instruction)
			else:
				dest, comp, jump = instruction[1:]
				a = "1" if "M" in comp else "0"
				if comp not in self._COMP_MAP or dest not in self._DEST_MAP or jump not in self._JMP_MAP:
					raise Exception("Instruction not mappable, the C instruction was: %s=%s;%s\n" % (dest, comp, jump))
				machine_language_instruction = "111"+a+self._COMP_MAP[comp]+self._DEST_MAP[dest]+self._JMP_MAP[jump]
				self.machine_language_output.append(machine_language_instruction)

		del self.tokenized_instructions

	def generate(self):
		# print("raw input is: \n%s" % self.raw_input)
		self.parse_file_lines()
		# print("parsed input is: \n%s" % self.pre_processed_input)
		self.tokenize_file_lines()
		# print("tokenized input is: \n%s" % self.tokenized_instructions)
		self.second_pass()
		# print("input after second pass is: \n%s" % self.tokenized_instructions)
		self.convert_tokens_to_machine_language()
		# print("machine language output is: \n%s" % self.machine_language_output)


if __name__ == "__main__":
	# read file and generate machine code using this assembler, save to xxx.hack file
	import sys

	args = sys.argv
	if len(args)!=2:
		raise Exception("Exactly one argument required. Please include file name to assemble. Args were: %s" % str(args))

	file_name = args[1]

	# read file into a line list
	with open(file_name) as f:
		list_of_file_lines = f.readlines()

	assembler = HackAssembler(list_of_file_lines) # feed raw lines to assembler

	# generate list of machine code lines
	assembler.generate()

	# obtain string output
	string_output = "\n".join(assembler.machine_language_output)

	# write to new file
	new_file_name = file_name.split(".")[0]
	with open(new_file_name+".hack", "w") as machine_code_file:
		machine_code_file.write(string_output)


