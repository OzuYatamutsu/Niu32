# Niu32

<div align="center">
    <img src="https://raw.githubusercontent.com/OzuYatamutsu/Niu32/master/Niu.png" /><br />
</div>

## What is this?

Niu32 is a **RISC** 32-bit instruction set that aims to be as simple as possible to understand, well-documented, and easy to write for. A Python 3 assembler will be provided in near future after the specification is complete.

## Before we start...

In Niu32, ops are listed in **UPPERCASE**, labels in **lowercase**, and numbers are prefixed by `0x` for **hexidecimal** values, `0b` for **binary** values, or listed without a prefix for **decimal** values.

Registers are prefixed with a `$`, and line comments are prefixed with a `!`.

Although not a valid register in our instruction set, we will refer to instruction arguments involving registers with the designations `$arg1`, `$arg2`, and `$argD` for source and destination registers, respectively.

## Instruction word format

An instruction word in Niu32 is 32 bits long. We will start counting from **bit 31** (most-significant) to **bit 0** (least-significant).

An instruction word can be divided into the following fields:

- **Primary opcode (OP1)**. *5 bits*. Signals the processor what instruction to perform, or alternatively signals the processor to check the **secondary opcode** to figure out what instruction to perform.

- **Source register arguments (ARG1, ARG2)**. *5 bits each*.  Specifies which registers to reference. The values stored in these registers will be used in evaluation of the instruction.

- **Destination register (ARGD)**. *5 bits*. Specifies which register to store the result of the operation after it has completed.

- **Immediate value (IMM)**. *17 bits*. A number used in some types of instructions instead of a secondary register argument. The value given in the instruction will be directly used in the evaluation of the instruction.

- **Secondary opcode (OP2)**. *5 bits*. Signals the processor what instruction to perform. Primarily used in non-immediate ALU instructions, where the secondary opcode is used to specify the `ALUop` signal (see below).

An instruction word can take one of two formats. Fields are shown at the top, and the bits they correspond to are shown at the bottom. Bit ranges are *inclusive* (i.e. "bits 4-0" *include both bit 4 and bit 0*).

#### Non-immediate

| OP1 |ARG1 |ARG2 |ARGD |*empty*| OP2 |
|:---:|:---:|:---:|:---:|:-----:|:---:|
|xxxxx|xxxxx|xxxxx|xxxxx|0000000|xxxxx|
|31-27|26-22|21-17|16-12|  11-5 | 4-0 |

These are used for **instructions which require the use of two argument registers** and/or **instructions which require a secondary opcode**.

#### Immediate

| OP1 |ARG1 |ARGD |       IMM       | 
|:---:|:---:|:---:|:---------------:|
|xxxxx|xxxxx|xxxxx|xxxxxxxxxxxxxxxxx|
|31-27|26-22|21-17|       16-0      |

These are used for **instructions which require the use of an immediate value**.

## Registers

Niu32 has **32** addressable registers. 

| Number | Name | Binary | Description | 
|:------:|:----:|:------:|:---------------:|
|R0|$zero|00000|A read-only register that will only hold a value of **0**.
|R1|$a0|00001|**Argument register 0**. *Caller pushed*. Used for passing arguments to subroutines in an assembly program.
|R2|$a1|00010|**Argument register 1**. *Caller pushed*. Used for passing arguments to subroutines in an assembly program.
|R3|$a2|00011|**Argument register 2**. *Caller pushed*. Used for passing arguments to subroutines in an assembly program.
|R4|$a3|00100|**Argument register 3**. *Caller pushed*. Used for passing arguments to subroutines in an assembly program.
|R5|$t0|00101|**Temporary register 0**. *Caller saved*. Used to hold a temporary value.
|R6|$t1|00110|**Temporary register 1**. *Caller saved*. Used to hold a temporary value.
|R7|$t2|00111|**Temporary register 2**. *Caller saved*. Used to hold a temporary value.
|R8|$t3|01000|**Temporary register 3**. *Caller saved*. Used to hold a temporary value.
|R9|$t4|01001|**Temporary register 4**. *Caller saved*. Used to hold a temporary value.
|R10|$t5|01010|**Temporary register 5**. *Caller saved*. Used to hold a temporary value.
|R11|$t6|01011|**Temporary register 6**. *Caller saved*. Used to hold a temporary value.
|R12|$t7|01100|**Temporary register 7**. *Caller saved*. Used to hold a temporary value.
|R13|$s0|01101|**Saved register 0**. *Callee saved*. Used to hold a temporary/saved value.
|R14|$s1|01110|**Saved register 1**. *Callee saved*. Used to hold a temporary/saved value.
|R15|$s2|01111|**Saved register 2**. *Callee saved*. Used to hold a temporary/saved value.
|R16|$s3|10000|**Saved register 3**. *Callee saved*. Used to hold a temporary/saved value.
|R17|$s4|10001|**Saved register 4**. *Callee saved*. Used to hold a temporary/saved value.
|R18|$s5|10010|**Saved register 5**. *Callee saved*. Used to hold a temporary/saved value.
|R19|$s6|10011|**Saved register 6**. *Callee saved*. Used to hold a temporary/saved value.
|R20|$s7|10100|**Saved register 7**. *Callee saved*. Used to hold a temporary/saved value.
|R21|$r0|10101|**Return value 0**. Used to hold a single return value from a subroutine (instead of pushing onto the stack).
|R22|$r1|10110|**Return value 1**. Used to hold a single return value from a subroutine (instead of pushing onto the stack).
|R23|$r2|10111|**Return value 2**. Used to hold a single return value from a subroutine (instead of pushing onto the stack).
|R24|$r3|11000|**Return value 3**. Used to hold a single return value from a subroutine (instead of pushing onto the stack).
|R25|$ra|11001|**Return address**. *Callee saved*. Used to hold the return address of the calling routine.
|R26|$gp|11010|**Global pointer**. Used to point to global variables.
|R27|$fp|11011|**Frame pointer**. *Callee saved*. Used to hold the memory location of the current stack frame.
|R28|$sp|11100|**Stack pointer**. *Callee saved*. Used to hold the memory location of the next empty position on the stack.
|R29|$at|11101|**Assembler temporary**. Reserved for assembler use (for example, when evaluating pseudo-ops)
|R30|$k0|11110|**Kernel register 0**. Reserved for kernel use (for example, during interrupt handling).
|R31|$k1|11111|**Kernel register 1**. Reserved for kernel use (for example, during interrupt handling).

## Opcodes

#### Primary

`ADD $argD, $arg1, $arg2`       <br>
**$argD <- $arg1 + $arg2**    <br>
Adds `$arg1` to `$arg2`, and stores the result in `$argD`.

`SUB $argD, $arg1, $arg2`       <br>
**$argD <- $arg1 - $arg2**    <br>
Subtracts `$arg1` from `$arg2`, and stores the result in `$argD`.

#### Secondary



## Assembler

#### Pseudo-ops

`SUBI $argD, $arg1, imm`        <br>
**$argD <- $arg1 - imm**      <br>
Subtracts `imm` from `$arg1`, and stores the result in `$argD`.
The assembler will negate `imm` and transform this into an `ADDI` instruction.
