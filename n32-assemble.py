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

def main():
    # Parse command-line arguments
    if (len(argv) < MIN_ARG_SIZE):
        print(ERR_INVALID_ARGS)
        _exit(-1)

# Run assembler on call!
main()