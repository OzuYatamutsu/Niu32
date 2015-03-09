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

### Error/Warning/Informational messages
ERR_INVALID_ARGS = """Syntax: n32-assemble.py <filename> [args]
    Valid arguments:\n
    -o [filename], --output [filename]: Output filename.
    -v, --verbose: Print verbose output."""
ERR_NUM_ARGS = ERROR_HDR + "Invalid number of arguments.\n"
VER_MAIN_COMPL = VERBOSE_HDR + """Parsing arguments complete!
    Input file: {arg1}
    Output file: {arg2}
    Verbose mode is on!"""

### Lookup tables
REGS = {"zero": "00000", "a0": "00001", "a1": "00010", 
        "a2": "00011", "a3": "00100", "t0": "00101", 
        "t1": "00110", "t2": "00111", "t3": "01000", 
        "t4": "01001", "t5": "01010", "t6": "01011", 
        "t7": "01100", "s0": "01101", "s1": "01110",
        "s2": "01111", "s3": "10000", "s4": "10001", 
        "s5": "10010", "s6": "10011", "s7": "10100", 
        "r0": "10101", "r1": "10110", "r2": "10111", 
        "r3": "11000", "ra": "11001", "gp": "11010", 
        "fp": "11011", "sp": "11100", "at": "11101", 
        "k0": "11110", "k1": "11111"}

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

DIRECTIVES = ["NAME", "ORIG"]

def main():
    '''The entry point of the assembler.'''

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

# Run assembler on call!
main()