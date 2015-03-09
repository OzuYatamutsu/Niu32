from sys import argv
from os import _exit

# Minimum we can work with is "n32-assemble.py <filename>"
MIN_ARG_SIZE = 2

### Command line arguments
OUTPUT_ARG = "-o"
OUTPUT_ARG_LONG = "--output"
VERBOSE_ARG_SHORT = "-v"
VERBOSE_ARG_LONG = "--verbose"

### Error/Warning/Informational messages
ERR_INVALID_ARGS = """Syntax: n32-assemble.py <filename> [args]
    Valid arguments:\n
    -o [filename], --output [filename]: Output filename.
    -v, --verbose: Print verbose output."""

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

def main():
    # Parse command-line arguments
    if (len(argv) < MIN_ARG_SIZE):
        print(ERR_INVALID_ARGS)
        _exit(-1)

# Run assembler on call!
main()