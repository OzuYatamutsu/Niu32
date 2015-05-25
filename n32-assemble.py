from sys import argv
from os import _exit

# Minimum we can work with is "n32-assemble.py <filename>"
MIN_ARG_SIZE = 2

### Command line arguments
OUTPUT_ARG = "-o"
OUTPUT_ARG_LONG = "--output"
VERBOSE_ARG = "-v"
VERBOSE_ARG_LONG = "--verbose"

### ...and their respective flags
OUTPUT_FILENAME = ""
VERBOSE = False

### Symbols
REG_SYM = "$"
PSEUDO_SYM = "."
OUTPUT_EXT = ".mif"
ERROR_HDR = "<error> "
VERBOSE_HDR = "<verbose> "

### Assembler variables
BIT_SIZE = 32 # Bits
INSTR_SIZE = 4 # Bytes
OFFSET_LEN = 17 # Bits

### Error/Warning/Informational messages
ERR_INVALID_ARGS = """Syntax: n32-assemble.py <filename> [args]
    Valid arguments:\n
    -o [filename], --output [filename]: Output filename.
    -v, --verbose: Print verbose output."""
ERR_ALUI = ERROR_HDR + "ALUI cannot be explicitly used as an instruction."
ERR_NUM_ARGS = ERROR_HDR + "Invalid number of arguments.\n"
ERR_ORIG_LOC = ERROR_HDR + "Error at line {arg1}: .ORIG to misaligned location!\n"
ERR_SYNTAX = ERROR_HDR + "Error at line {arg1}: Unexpected op, arg, or label!\n"
VER_MAIN_COMPL = VERBOSE_HDR + """Parsing arguments complete!
    Input file: {arg1}
    Output file: {arg2}
    Verbose mode is on!"""
VER_STG1_START = VERBOSE_HDR + "[Stage 1] Reading input file..."
VER_STG1_END = VERBOSE_HDR + "[Stage 1] File read complete!"
VER_STG2_START = VERBOSE_HDR + "[Stage 2] Starting line-by-line assembly..."
VER_STG2_END = VERBOSE_HDR + "[Stage 2] Assembly complete!"
VER_STG3_START = VERBOSE_HDR + "[Stage 3] Starting label resolution..."
VER_STG3_END = VERBOSE_HDR + "[Stage 3] Label resolution complete!"
VER_STG4_START = VERBOSE_HDR + "[Stage 4] Writing output file..."
VER_STG4_END = VERBOSE_HDR + "[Stage 4] File write complete!"
ASSEMBLY_END = "Assembly complete! Wrote to {arg1}"

### Lookup tables
REGS = {"$zero": "00000", "$a0": "00001", "$a1": "00010", 
        "$a2": "00011", "$a3": "00100", "$t0": "00101", 
        "$t1": "00110", "$t2": "00111", "$t3": "01000", 
        "$t4": "01001", "$t5": "01010", "$t6": "01011", 
        "$t7": "01100", "$s0": "01101", "$s1": "01110",
        "$s2": "01111", "$s3": "10000", "$s4": "10001", 
        "$s5": "10010", "$s6": "10011", "$s7": "10100", 
        "$r0": "10101", "$r1": "10110", "$r2": "10111", 
        "$r3": "11000", "$ra": "11001", "$gp": "11010", 
        "$fp": "11011", "$sp": "11100", "$at": "11101", 
        "$k0": "11110", "$k1": "11111"}

OP1 = {"ALUI": "00000", "ADDI": "00001", "MLTI": "00010", 
       "DIVI": "00011", "ANDI": "00101", "ORI": "00110", 
       "XORI": "00111", "SULI": "01000", "SSLI": "01001", 
       "SURI": "01010", "SSRI": "01011", "LW": "10000", 
       "LB": "10001", "SW": "10011", "SB": "10100", 
       "LUI": "10110", "BEQ": "11000", "BNE": "11001", 
       "BLT": "11010", "BLE": "11011", "JAL": "11111"}

OP2 = {"SUB": "00000", "ADD": "00001", "MLT": "00010", 
       "DIV": "00011", "NOT": "00100", "AND": "00101", 
       "OR": "00110", "XOR": "00111", "SUL": "01000", 
       "SSL": "01001", "SUR": "01010", "SSR": "01010", 
       "EQ": "10000", "NEQ": "10001", "LT": "10010", 
       "LEQ": "10011"}

PSEUDO_OP = ["SUBI", "GT", "GEQ", "NAND", "NOR",
             "NXOR", "CPY", "LA", "LV", "CLR", 
             "BGT", "BGE", "GOTO", "JMP", "RET", 
             "PUSH", "POP"]

TWO_STG_PSEUDO_OP = {"NAND": "NAND.2", "NOR": "NOR.2", "NXOR": "NXOR.2", 
                     "LA": "LA.2", "LV": "LV.2", "PUSH": "PUSH.2", 
                     "POP": "POP.2"}

DIRECTIVES = [".NAME", ".ORIG", ".WORD"]

### Memory symbols
INSTR_PREFIX = "-- @ "
BIN_TAG = "<BIN>"
BIN_CTAG = "</BIN>"
ADDRESS_INSTR_SEP = " : "
INSTR_ARG_SEP = "   "
LINE_INSTR_SEP = " : "
HEX_PREFIX = "0x"
BIN_PREFIX = "0b"
IMEM_PREAMBLE = """WIDTH=""" + str(BIT_SIZE) + """;
DEPTH=2048;
ADDRESS_RADIX=HEX;
DATA_RADIX=HEX;
CONTENT BEGIN"""
IMEM_END = "END;"

def main():
    '''The entry point of the assembler.'''

    # Mark as global to access outside vars
    global OUTPUT_FILENAME
    global VERBOSE

    # Parse command-line arguments
    if (len(argv) < MIN_ARG_SIZE):
        print(ERR_INVALID_ARGS)
        _exit(-1)

    # If an output filename was specified, set it!
    if (OUTPUT_ARG in argv) or (OUTPUT_ARG_LONG in argv):
        if (OUTPUT_ARG in argv):
            OUTPUT_FILENAME = argv[argv.index(OUTPUT_ARG) + 1]
            del argv[argv.index(OUTPUT_ARG) + 1]
            del argv[argv.index(OUTPUT_ARG)]
        else:
            OUTPUT_FILENAME = argv[argv.index(OUTPUT_ARG_LONG) + 1]
            del argv[argv.index(OUTPUT_ARG_LONG) + 1]
            del argv[argv.index(OUTPUT_ARG_LONG)]

    # If verbose argument was specified, set the flag!
    if (VERBOSE_ARG in argv) or (VERBOSE_ARG_LONG in argv):
        VERBOSE = True

        if (VERBOSE_ARG in argv): 
            del argv[argv.index(VERBOSE_ARG)]
        else:
            del argv[argv.index(VERBOSE_ARG_LONG)]

    # At this point, we should only have two arguments:
    # argv[0] = Python module
    # argv[1] = Input filename
    
    # Sanity check for above!
    if (len(argv) != 2):
        print(ERR_NUM_ARGS)
        _exit(-1)

    # If an output filename was not specified, use the input filename
    if (OUTPUT_FILENAME == ""): 
        OUTPUT_FILENAME = argv[1].split(".")
        OUTPUT_FILENAME = OUTPUT_FILENAME[0:len(OUTPUT_FILENAME) - 1]
        OUTPUT_FILENAME = ".".join(OUTPUT_FILENAME) + OUTPUT_EXT

    # Debug output - end of command-line arg parsing
    if VERBOSE: 
        print(VER_MAIN_COMPL.replace("{arg1}", argv[1])
              .replace("{arg2}", OUTPUT_FILENAME))

    ## Stage 1: File read

    # Debug output - start reading file
    if VERBOSE: print(VER_STG1_START)

    input = read_input(argv[1])

    # Debug output - end reading file
    if VERBOSE: print(VER_STG1_END)

    ## Stage 2: Assembly

    # Debug output - start assemble
    if VERBOSE: print(VER_STG2_START)

    output, labels, unresolved = assemble(input)

    # Debug output - end assemble
    if VERBOSE: print(VER_STG2_END)

    ## Stage 3: Label resolution

    # Debug output - start label resolution
    if VERBOSE: print(VER_STG3_START)

    output = resolve_all(output, labels, unresolved)

    # Debug output - end label resolution
    if VERBOSE: print(VER_STG3_START)

    ## Stage 4: Write to file

    # Debug output - start file write
    if VERBOSE: print(VER_STG4_START)

    output_file(output)

    # Debug output - end file write
    if VERBOSE: print(VER_STG4_END)

    # Assembly complete!
    print(ASSEMBLY_END.replace("{arg1}", OUTPUT_FILENAME))

def assemble(inputAsm):
    '''Performs a line-by-line assembly of the input assembly program 
    and returns an output, incomplete assembled program, along with 
    a dict of labels and a dict of unresolved uses of those labels.'''

    # Output program, as a line-by-line list
    outputAsm = {}

    # Line number in the input file
    lineNum = 0

    # Instruction number of current instruction
    instrNum = 0

    # Memory location of current instruction
    memLocation = 0

    # Key-value dict of labels to memory locations where declared
    labels = {}

    # Key-value dict of labels to lists of unresolved uses of labels
    unresolved = {}

    for line in inputAsm:
        line = get_instr(line)
        if (is_label(line)):
            # Add this label to our labels table and move on
            labels[line.replace(":", "")] = decimal_to_binary(memLocation, 32)
        elif (is_meaningful(line)):
            op = line[0]
            args = line[1:len(line)]

            # First, check if directive
            if (op in DIRECTIVES):
                try: 
                    labels, memLocation, instrNum, outputAsm = \
                        handle_directive(op, args, labels, 
                                      memLocation, instrNum, outputAsm)
                except ValueError:
                    # Problem resolving .ORIG directive
                    handle_error(ERR_ORIG_LOC, lineNum)

            # Check if this is a dedicated instruction
            elif (op in OP1 or op in OP2 or op in PSEUDO_OP or op in TWO_STG_PSEUDO_OP.values()):
                # Memory location
                outLine = INSTR_PREFIX + HEX_PREFIX
                outLine = outLine + decimal_to_hex(memLocation, BIT_SIZE)

                # Op
                outLine = outLine + ADDRESS_INSTR_SEP + INSTR_ARG_SEP + op
                if (op in TWO_STG_PSEUDO_OP): outLine = outLine + ".1"

                # Args
                outLine = outLine + " " + ",".join(args).upper()

                # Instruction number
                outLine = outLine + "\n" + decimal_to_hex(instrNum, BIT_SIZE)

                if (op in PSEUDO_OP):
                    # Convert/expand to actual instruction
                    op, args = convert_pseudo_op(op, args)
                    
                    if (type(op) is list):
                        # If converted to multiple instructions, this is two-stage pseudo-op
                        # Process second stage next
                        inputAsm.insert(lineNum + 1, op[1])
                        op = op[0]

                elif (op in TWO_STG_PSEUDO_OP.values()):
                    op, args = convert_two_stg_pseudo_op(op, args)

                # Assemble instruction
                try:
                    instr, unresolved, unresolvedMod = instr_assemble(
                        op, args, instrNum, unresolved)
                except Exception as e:
                    handle_error(e, lineNum)

                if (not unresolvedMod):
                    outLine = outLine + LINE_INSTR_SEP + binary_to_hex_word(instr) + ";"
                else:
                    # Otherwise, we have to convert it after resolving label
                    outLine = outLine + LINE_INSTR_SEP + BIN_TAG + instr + BIN_CTAG + ";"

                # We're done for now - commit to output queue
                outputAsm[instrNum] = outLine

                # Take care of overhead
                instrNum = instrNum + 1
                memLocation = memLocation + INSTR_SIZE
            else: 
                # op was unexpected!
                print(ERR_SYNTAX)
                _exit(-1)
            
        lineNum = lineNum + 1
        # And start the next line...

    # Note: Output is NOT complete! Must resolve labels!
    return outputAsm, labels, unresolved

def get_instr(line):
    '''Returns an instruction from an input line as a list 
    containing the opcode/pseudo-op/directive and any arguments 
    provided, stripped of any extra characters. If the input is a 
    label, returns the label in UPPERCASE.'''

    line = line.split("!")[0].replace("\n", "")

    # If entire line is a comment, no useful code
    if (len(line) == 0):
        return ""
    op = ""
    result = []
    pointChar = 0

    while line[pointChar] == " " or line[pointChar] == "\t":
        pointChar = pointChar + 1
    
    while pointChar < len(line) and line[pointChar] != " " and line[pointChar] != "\t":
        op = op + line[pointChar]
        pointChar = pointChar + 1
    
    if (op in DIRECTIVES):
        line = line.replace(op, "", 1).replace("\t", "").strip()
        result = line.split(" ")
    else:
        line = line.replace(op, "", 1).replace(" ", "").replace("\t", "")
        result = line.split(",")
    result.insert(0, op.upper())

    if (":" in op):
        return op.upper()

    return result

def is_label(line):
    '''Checks if the given line is a memory label.'''

    return type(line) is not list and ((":" in line) 
        or ((not is_hex(line)) and (not is_binary(line))  
        and (not is_decimal(line))))

def is_hex(numString):
    '''Checks if the given number is a hex number.'''

    try: return '0x' in numString
    except TypeError: return False

def is_binary(numString):
    '''Checks if the given number is a binary number.'''

    try: return '0b' in numString and '0x' not in numString
    except TypeError: return False

def is_decimal(numString):
    '''Checks if the given number is a decimal number.'''

    try:
        numString = int(numString)
    except ValueError:
        return False
    return True

def num_to_binary(numString, binLength):
    '''Converts the given number to a binary string of given bit-length.
    Detects whether a decimal-binary conversion or a hex-binary conversion 
    is needed first. The input number will be treated as a signed integer.'''

    if (is_binary(numString)):
        return numString.replace("0b", "")
    elif (is_decimal(numString)):
        return decimal_to_binary(int(numString), binLength)
    elif (is_hex(numString)):
        return hex_to_binary(numString, binLength)

def num_to_num(numString):
    '''Converts the given hexidecimal or binary number to an integer.'''

    if (is_binary(numString)):
        return int(numString, 2)
    if (is_hex(numString)):
        return int(numString, 16)
    return int(numString)

def decimal_to_binary(num, binLength):
    '''Converts the given decimal number to a binary string of given bit-length.
    Treats the input number as a signed integer.'''

    # 2's complement negation
    if num < 0: num = int(bin(num & int('0b' + '1' * binLength, 2)), 2)
    output = bin(num).replace("0b", "")
    if len(output) < binLength:
        # Left-padding
        output = (binLength - len(output)) * '0' + output
    return output

def decimal_to_hex(num, hexLength):
    '''Converts the given decimal number to a hexidecimal string of given bit-length.
    Treats the input number as a signed integer.'''

    # Length in bits to length of string
    hexLength = int(hexLength / 4)

    # 2's complement negation
    if num < 0: num = int(bin(num & int('0b' + '1' * WIDTH, 2)), 2)
    output = hex(num).replace("0x", "")
    if len(output) < hexLength:
        # Left-padding
        output = (hexLength - len(output)) * '0' + output
    return output

def hex_to_binary(hexString, numBits):
    '''Converts the given hexidecimal number to a binary string of given bit-length.
    Treats the input number as a signed integer.'''

    output = bin(int(hexString, 16)).replace("0b", "")
    if len(output) < numBits:
        output = (numBits - len(output)) * '0' + output
    return output

def binary_to_hex_word(binString):
    '''Converts the given binary number to a hex string.'''

    binString = binString.replace("0b", "")
    hexLength = int(BIT_SIZE / 4)
    output = hex(int(binString, 2)).replace("0x", "")
    if len(output) < hexLength:
        # Left-padding
        output = (hexLength - len(output)) * '0' + output
    return output


def is_meaningful(line):
    '''Checks if the given line has any meaningful instruction.'''

    return (line != "")

def handle_directive(op, args, labelTable, addressNum, instrNum, outputAsm):
    '''Evaluates a given assembler directive, given the assembler 
    label table, current address number, current instruction number, 
    and assembler output queue. Returns the updated label table, 
    address number, instruction number, and assembler output queue.'''

    if (op == ".NAME"):
        labelTable[args[0].upper()] = num_to_binary(args[1], BIT_SIZE)
    elif (op == ".ORIG"):
        memoryDelta = addressNum 
        instrDelta = instrNum
        if is_binary(args[0]): 
            addressNum = int(args[0], 2)
        elif is_hex(args[0]):
            addressNum = int(args[0], 16)
        else: # It's a decimal
            addressNum = int(args[0])
        memoryDelta = addressNum - memoryDelta
        if memoryDelta != 0:
            # Throw an error if we'd be jumping to misaligned memory!
            if (addressNum % INSTR_SIZE != 0):
                raise ValueError(ERR_ORIG_LOC)

            instrNum = instrNum + int(memoryDelta / INSTR_SIZE)
    elif (op == ".WORD"):
        args[0] = args[0].lower()
        outputLine = INSTR_PREFIX + HEX_PREFIX 
        outputLine = outputLine + decimal_to_hex(addressNum, BIT_SIZE)
        outputLine = outputLine + ADDRESS_INSTR_SEP + INSTR_ARG_SEP + op
        outputLine = outputLine + " " + ",".join(args).upper()
        outputLine = outputLine + "\n" + decimal_to_hex(instrNum, BIT_SIZE)
        outputLine = outputLine + LINE_INSTR_SEP + hex_word_zero_pad(args[0]) + ";"
        outputAsm[instrNum] = outputLine

        instrNum = instrNum + 1
        addressNum = addressNum + INSTR_SIZE

    return labelTable, addressNum, instrNum, outputAsm

def hex_word_zero_pad(hex_string):
    '''Zero-pads an input hex string to BIT_SIZE length.'''

    global BIT_SIZE

    hex_string = hex_string.replace("0x", "")
    return ('0' * (int(BIT_SIZE / 4) - len(hex_string))) + hex_string

def convert_pseudo_op(op, args):
    '''Converts a pseudo-op to valid Niu32 assembly code.'''

    # Check if the op is two-stage
    if (op in TWO_STG_PSEUDO_OP):
        # Process stage 1 here
        if (op == "NAND"):
            # NAND arg1, arg2, arg3 is

            # AND arg1, arg2, arg3
            # NOT arg1, arg1
            
            op = ["AND", TWO_STG_PSEUDO_OP[op] + " " + ", ".join(args)]
        elif (op == "NOR"):
            # NOR arg1, arg2, arg3 is

            # OR arg1, arg2, arg3
            # NOT arg1, arg1

            op = ["OR", TWO_STG_PSEUDO_OP[op] + " " + ", ".join(args)]
        elif (op == "NXOR"):
            # NXOR arg1, arg2, arg3 is

            # XOR arg1, arg2, arg3
            # NOT arg1, arg1
            
            op = ["NXOR", TWO_STG_PSEUDO_OP[op] + " " + ", ".join(args)]
        elif (op == "LA"):
            # LA arg1, memloc_imm is

            # LUI $at, memloc_imm
            # ORI arg1, $at, memloc_imm
            
            op = ["LUI", TWO_STG_PSEUDO_OP[op] + " " + ", ".join(args)]
            args = ["$at", args[1]]
        elif (op == "LV"):
            # LV arg1, imm is

            # LUI $at, imm
            # ORI arg1, $at, imm
            
            op = ["LUI", TWO_STG_PSEUDO_OP[op] + " " + ", ".join(args)]
            args = ["$at", args[1]]
        elif (op == "PUSH"):
            # PUSH arg1 is

            # SW arg1, $sp, 0
            # ADDI $sp, $sp, -1
            
            op = ["SW", TWO_STG_PSEUDO_OP[op] + " " + ", ".join(args)]
            args.append("$sp")
            args.append("0")
        elif (op == "POP"):
            # POP arg1 is

            # LW arg1, $sp, 0
            # ADDI $sp, $sp, 1
            op = ["LW", TWO_STG_PSEUDO_OP[op] + " " + ", ".join(args)]
            args.append("$sp")
            args.append("0")
    elif (op == "SUBI"):
        op = "ADDI"
        # Negate imm
        args[2] = "0b" + num_to_binary(-1 * num_to_num(args[2]), OFFSET_LEN)
    elif (op == "GT"):
        op = "LT"
        # Swap args[1] and args[2]
        args[1], args[2] = args[2], args[1]
    elif (op == "GEQ"):
        op = "LEQ"
        # Swap args[1] and args[2]
        args[1], args[2] = args[2], args[1]
    elif (op == "CPY"):
        op = "ADD"
        # op1 + zero = op1
        args.append("$zero")
    elif (op == "CLR"):
        op = "ADD"
        # 0 + 0 => op0
        args.append("$zero")
        args.append("$zero")
    elif (op == "BGT"):
        op = "BLT"
        # Swap args[1] and args[2]
        args[1], args[2] = args[2], args[1]
    elif (op == "BGE"):
        op = "BLE"
        # Swap args[2] and args[1]
        args[1], args[2] = args[2], args[1]
    elif (op == "GOTO"):
        op = "BEQ"
        # Unconditional branch (0 == 0)
        args.insert(0, "$zero")
        args.insert(0, "$zero")
    elif (op == "JMP"):
        op = "JAL"
        # Simple alias
        args.insert(0, "$ra")
    elif (op == "RET"):
        op = "JAL"
        # Simple alias, we don't care about return location
        args.append("$zero")
        args.append("$ra")

    return op, args

def convert_two_stg_pseudo_op(op, args):
    '''Converts a second-stage pseudo-op to valid Niu32 assembly code.'''

    if (op == "NAND.2"):
        # NAND arg1, arg2, arg3 is

        # AND arg1, arg2, arg3
        # NOT arg1, arg1
        
        op = "NOT"
        args = [args[0], args[0]]
    elif (op == "NOR.2"):
        # NOR arg1, arg2, arg3 is

        # OR arg1, arg2, arg3
        # NOT arg1, arg1

        op = "NOT"
        args = [args[0], args[0]]
    elif (op == "NXOR.2"):
        # NXOR arg1, arg2, arg3 is

        # XOR arg1, arg2, arg3
        # NOT arg1, arg1
            
        op = "NOT"
        args = [args[0], args[0]]
    elif (op == "LA.2"):
        # LA arg1, memloc_imm is

        # LUI $at, memloc_imm
        # ORI arg1, $at, memloc_imm
        
        op = "ORI"
        args = [args[0], "$at", args[1]]
    elif (op == "LV.2"):
        # LV arg1, imm is

        # LUI $at, imm
        # ORI arg1, $at, imm

        op = "ORI"
        args = [args[0], "$at", args[1]]
    elif (op == "PUSH.2"):
        # PUSH arg1 is

        # SW arg1, $sp, 0
        # ADDI $sp, $sp, -1
        op = "ADDI"
        args = ["$sp", "$sp", "-1"]
    elif (op == "POP.2"):
        # POP arg1 is

        # LW arg1, $sp, 0
        # ADDI $sp, $sp, 1

        op = "ADDI"
        args = ["$sp", "$sp", "-1"]

    return op, args

def instr_assemble(op, args, instrNum, unresolvedLabels):
    '''Assembles a Niu32 assembly instruction to hex code.'''
    instr = ""
    unresolvedMod = False

    if (op in OP1):
        if (is_label(args[len(args) - 1])):
            # Add to unresolvedLabels
            unresolvedLabels[args[len(args) - 1]] = instrNum

            # ...and flag that we must resolve label later
            unresolvedMod = True
        if (op == "ALUI"):
            raise AssertionError(ERR_ALUI)
        elif (op == "LUI"):
            # arg1 = $zero
            args.insert(1, "$zero")
        elif (op == "JAL"):
            pass

        # Convert op
        instr = instr + OP1[op]

        # Convert arg1
        instr = instr + REGS[args[1]]

        # Convert argd
        instr = instr + REGS[args[0]]

        if (not unresolvedMod):
            # Convert imm
            instr = instr + num_to_binary(args[2], OFFSET_LEN)
        else:
            # Put a placeholder instead for imm
            instr = instr + args[len(args) - 1]
    elif (op in OP2):
        # OP1 is ALUI
        instr = instr + OP1["ALUI"]

        # Convert arg1
        instr = instr + REGS[args[1]]

        # Convert arg2
        instr = instr + REGS[args[2]]

        # Convert argd
        instr = instr + REGS[args[0]]

        # 7'b0 blank field
        instr = instr + '0000000'

        # Convert op as op2
        instr = instr + OP2[op]
    else: raise AssertionError(ERR_SYNTAX)

    return instr, unresolvedLabels, unresolvedMod

def resolve_all(asm, labels, uses):
    '''Resolves all uses of labels to their memory locations in the input 
    incomplete assembled program (as a list).'''

    for use in uses:
        # Resolve offset
        asm[uses[use]] = asm[uses[use]].replace(
            use,
            trim(
                resolve(
                    hex_to_binary(find_asm_mem_loc(asm[uses[use]]), 32),
                    labels[use.upper()]
                ), OFFSET_LEN)
        )

        # Now assemble instruction to hex
        hex_out = get_between(BIN_TAG, BIN_CTAG, asm[uses[use]])
        hex_out = binary_to_hex_word(hex_out)

        # And commit back
        asm[uses[use]] = replace_between(BIN_TAG, BIN_CTAG, 
                                         hex_out, asm[uses[use]]) + ";"

    return asm

def resolve(current, remote):
    '''Outputs an offset difference between the remote and current location, 
    as a hexidecimal number.'''

    offset = int(((int(remote, 2) - int(current, 2)) / INSTR_SIZE) - 1)
    length = len(current) if len(current) > len(remote) else len(remote)
    if offset < 0: return bin(offset & int('0b' + '1' * length, 2)).replace("0b", "")
    else: return bin(offset).replace("0b", "")

def find_asm_mem_loc(line):
    '''Returns the memory location of an assembled instruction.'''

    return line[5:15]

def get_between(startTag, endTag, input):
    '''Gets the text between two tags.'''

    strSplit = [input.split(startTag)[0]]
    strSplit = strSplit + input.split(startTag)[1].split(endTag)
    
    return strSplit[1]

def replace_between(start_tag, end_tag, new_text, input):
    '''Replaces the text between two tags.'''

    return input.replace(
        input.split(start_tag)[1], new_text
    ).replace(start_tag, "")

def binary_to_signed_decimal(binString):
    '''Converts a binary string to a signed decimal number.'''

    binString = binString.replace("0b", "")
    if binString[0] != '1': return int(binString, 2)
    else: return -1 * ((int(binString, 2) ^ int('0b' + '1' * len(binString), 2)) + 1)

def trim(binString, numBits):
    '''Trims leading 0s so that binString is length numBits.'''

    binString = binString.replace("0b", "")

    if len(binString) < numBits:
        binString = (numBits - len(binString)) * '0' + binString

    decValue = binary_to_signed_decimal(binString)
    if decValue > (2**numBits - 1): 
        raise Exception("Target address is too far away!")

    if decValue < 0: binString = bin(decValue & int('0b' + '1' * numBits, 2))
    else: binString = bin(decValue)
    binString = binString.replace("0b", "")

    # And check again
    if len(binString) < numBits:
        binString = (numBits - len(binString)) * '0' + binString

    return binString

def output_file(output):
    '''Outputs an assembled program into an output file (OUTPUT_FILENAME).'''

    with open(OUTPUT_FILENAME, "w") as f:
        f.write(IMEM_PREAMBLE + "\n")
        for line in list(output.values()):
            f.write(line + "\n")
        f.write(IMEM_END)

def read_input(filename):
    '''Reads the input assembly program into a list.'''

    f = open(filename, 'r')
    input = f.readlines()
    f.close()

    return input

def handle_error(err, lineNum):
    '''Outputs an error and gives the line of failure before exiting.'''

    print(str(err).replace("{arg1}", str(lineNum)))
    _exit(-1)

# Run assembler on call!
main()