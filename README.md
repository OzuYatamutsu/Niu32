# Niu32

<div align="center">
    <img src="https://raw.githubusercontent.com/OzuYatamutsu/Niu32/master/Niu.png" /><br />
</div>

## What is this?

Niu32 is a **RISC** 32-bit instruction set that aims to be as simple as possible to understand, well-documented, and easy to write for. A Python 3 assembler will be provided in near future after the specification is complete.

## Before we start...

In Niu32, ops are listed in **UPPERCASE**, labels in **lowercase**, and numbers are prefixed by `0x` for **hexidecimal** values, `0b` for **binary** values, or listed without a prefix for **decimal** values.

Registers are prefixed with a `$`, and line comments are prefixed with a `!`.

Although not a valid register in our instruction set, we will refer to instruction arguments involving registers with the designations `$arg1`, `$arg2`, and `$argD` for source and destination registers, respectively. We will use the value `0xBEEF` for numerical arguments.

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

## Memory

Niu32's memory is **byte** and **word-addressable**. The size of a memory word is **32 bits (4 bytes)**, so any implementation of a Niu32 ISA must reserve the least-significant 2 bits to select a single byte at a given memory location.

|Selection bits|Select|
|:------------:|:----:|
|00|Byte 1|
|01|Byte 2|
|10|Byte 3|
|11|Byte 4|

For example, a memory can look like the following (with 15 bits of addressability + 2 bits byte selector):

|Location|Byte 1 (+0)|Byte 2 (+1)|Byte 3 (+2)|Byte 4 (+3)|
|:------:|:----:|:----:|:----:|:----:|
|0x0000|0xDE|0xAD|0xBE|0xEF|
|0x0004|0xAB|0xBC|0xCD|0xDE|
|0x0008|0xB0|0x0B|0x55|0x66|
|...|...|...|...|...|
|0x7FFF|0xFF|0xCC|0xBB|0xAA|

**Word at 0x0000**: `0xDEADBEEF` (32 bits)
**Byte at 0x0000**: `0xDE` (8 bits)

## Opcodes

#### Primary

The opcode table below summarizes the binary instruction corresponding to each opcode.
Most significant bits are to the left, while least significant are to the top.

|xx|000 |001 |010 |011 |100 |101 |110 |111 |
|:-:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|00|[ALUI](#ALUI)|[ADDI](#ADDI)|[MLTI](#MLTI)|[DIVI](#DIVI)|[ANDI](#ANDI)|[ORI](#ORI)|
|01|SUL |SSL |SUR |SSR |
|10|LW  |LB  |SW  |SB  |LUI |
|11|BEQ |BNE |BLT |BLE |    |    |    |JAL |

##### ALUI
Signals the processor to check **OP2** for operation to perform. This instruction and encoding of the secondary opcode will be handled by the assembler according to the instruction written in the program (i.e. there should be no difference to the programmer as to how to write an instruction that uses the primary vs. secondary opcode).
This *should not be written directly in an assembly program*, and the assembler will throw an error if encountered!

##### ADDI
`ADDI $argD, $arg1, imm`        <br>
**$argD <- $arg1 + imm**        <br>
Adds `imm` to `$arg1`, and stores the result in `$argD`.

##### MLTI
`MLTI $argD, $arg1, imm`        <br>
**$argD <- $arg1 / imm**        <br>
Multiplies `$arg1` by `imm` and stores the result in `$argD`.

##### DIVI
`DIVI $argD, $arg1, imm`        <br>
**$argD <- $arg1 / imm**        <br>
Divides `$arg1` by `imm` and stores the result in `$argD`.

##### ANDI
`ANDI $argD, $arg1, imm`        <br>
**$argD <- $arg1 & imm**        <br>
Performs an AND on `$arg1` and `imm` and stores the result in `$argD`.

##### ORI
`ORI $argD, $arg1, imm`        <br>
**$argD <- $arg1 & imm**        <br>
Performs an OR on `$arg1` and `imm` and stores the result in `$argD`.

##### SUL
`SUL $argD, $arg1, imm`        <br>
**$argD <- $arg1 << imm**        <br>
Unsigned left-shifts `$arg1` by `imm` and stores the result in `$argD`.

##### SSL
`SSL $argD, $arg1, imm`        <br>
**$argD <- $arg1 <<< imm**        <br>
Signed left-shifts `$arg1` by `imm` and stores the result in `$argD`.

##### SUR
`SUR $argD, $arg1, imm`        <br>
**$argD <- $arg1 >> imm**        <br>
Unsigned right-shifts `$arg1` by `imm` and stores the result in `$argD`.

##### SSR
`SSR $argD, $arg1, imm`        <br>
**$argD <- $arg1 >>> imm**        <br>
Signed right-shifts `$arg1` by `imm` and stores the result in `$argD`.

##### LW
`LW $argD, $arg1, imm`          <br>
**$argD <- Mem[$arg1 + 4*imm]**       <br>
Loads the word at the memory location computed by adding `$arg1` and `imm` into `$argD`.

##### LB
`LB $argD, $arg1, imm`      <br>
**$argD <- Mem[$arg1 + imm]**       <br>
Loads the byte at the memory location computed by adding `$arg1` and `imm` into `$argD`. Note that the byte will be sign-extended to 32 bits before being stored in `$argD`.

##### SW
`LW $arg1, $arg2, imm`          <br>
**Mem[$arg2 + 4*imm] <- $arg1**       <br>
Stores the word in `$arg1` at the memory location computed by adding `$arg1` and `imm` into `$argD`.

##### SB
`SB $argD, $arg1, imm`      <br>
**Mem[$arg2 + imm] <- $arg1**       <br>
Stores the byte at the memory location computed by adding `$arg1` and `imm` into `$argD`. The value in `$arg1` will be shrunk into an 8-bit value before being stored in memory, which may result in undefined behavior if the value does not fit into 8 bits.

##### LUI
`LUI $argD, imm`        <br>
**$argD <- imm[16:1]**      <br>
Loads the **most-significant 16 bits** of `imm` into `$argD`. Can be combined with `ORI` to load a 32-bit immediate value into a register.

##### BEQ
`BEQ $arg1, $arg2, imm`        <br>
**$arg1 == $arg2 ? PC <- 4*imm : PC <- (PC + 4)**        <br>
Branches to `imm` if `$arg1` is **equal to** `$arg2`; otherwise, advances to the next instruction.

##### BLT
`BLT $arg1, $arg2, imm`        <br>
**$arg1 < $arg2 ? PC <- 4*imm : PC <- (PC + 4)**        <br>
Branches to `imm` if `$arg1` is **less than** `$arg2`; otherwise, advances to the next instruction.

##### BLE
`BLE $arg1, $arg2, imm`        <br>
**$arg1 <= $arg2 ? PC <- 4*imm : PC <- (PC + 4)**        <br>
Branches to `imm` if `$arg1` is **less than or equal to** `$arg2`; otherwise, advances to the next instruction.

##### BNE
`BNE $arg1, $arg2, imm`        <br>
**$arg1 != $arg2 ? PC <- 4*imm : PC <- (PC + 4)**        <br>
Branches to `imm` if `$arg1` is **not equal to** `$arg2`; else, advances to the next instruction.

##### JAL
`JAL $argD, $arg1`        <br>
**$argD <- (PC + 4), PC <- $arg1**        <br>
Jumps to the address of the subroutine stored in `$arg1` and stores the previous next instruction as the return address in `$argD`.

#### Secondary

These instructions are encoded in the **OP2** instruction word field (see above). 
They will be executed if the **OP1** instruction word field is set to **ALUI** (`00000`).

##### ADD
`ADD $argD, $arg1, $arg2`       <br>
**$argD <- $arg1 + $arg2**    <br>
Adds `$arg1` to `$arg2`, and stores the result in `$argD`.

##### SUB
`SUB $argD, $arg1, $arg2`       <br>
**$argD <- $arg1 - $arg2**    <br>
Subtracts `$arg1` from `$arg2`, and stores the result in `$argD`.

##### MLT
`MLT $argD, $arg1, $arg2`        <br>
**$argD <- $arg1 * $arg2**        <br>
Multiplies `$arg1` by `$arg2` and stores the result in `$argD`.

##### DIV
`DIV $argD, $arg1, $arg2`        <br>
**$argD <- $arg1 / $arg2**        <br>
Divides `$arg1` by `$arg2` and stores the result in `$argD`.

##### EQ
`EQ $argD, $arg1, $arg2`       <br>
**$argD <- ($arg1 == $arg2) ? 1 : 0**    <br>
Stores a value of **1** in `$argD` if `$arg1` is **equal to** `$arg2`; otherwise stores a **0**.

##### LT
`LT $argD, $arg1, $arg2`       <br>
**$argD <- ($arg1 < $arg2) ? 1 : 0**    <br>
Stores a value of **1** in `$argD` if `$arg1` is **less than** `$arg2`; otherwise stores a **0**.

##### LEQ
`LEQ $argD, $arg1, $arg2`       <br>
**$argD <- ($arg1 <= $arg2) ? 1 : 0**    <br>
Stores a value of **1** in `$argD` if `$arg1` is **less than or equal to** `$arg2`; otherwise stores a **0**.

##### AND
`AND $argD, $arg1, $arg2`       <br>
**$argD <- $arg1 & $arg2**    <br>
Performs a bitwise AND on `$arg1` and `$arg2`, and stores the result in `$argD`.

##### OR
`OR $argD, $arg1, $arg2`       <br>
**$argD <- $arg1 | $arg2**    <br>
Performs a bitwise OR on `$arg1` and `$arg2`, and stores the result in `$argD`.

##### NOT
`NOT $argD, $arg1, $arg2`       <br>
**$argD <- $arg1 ~ $arg2**    <br>
Performs a bitwise NOT on `$arg1` and `$arg2`, and stores the result in `$argD`.

##### XOR
`XOR $argD, $arg1, $arg2`       <br>
**$argD <- $arg1 ^ $arg2**    <br>
Performs a bitwise XOR on `$arg1` and `$arg2`, and stores the result in `$argD`.

## Assembler

#### Pseudo-ops

##### SUBI
`SUBI $argD, $arg1, imm`        <br>
**$argD <- $arg1 - imm**      <br>
Subtracts `imm` from `$arg1`, and stores the result in `$argD`. <br>
The assembler will negate `imm` and transform this into an `ADDI` instruction.

##### GT
`GT $argD, $arg1, $arg2`       <br>
**$argD <- ($arg1 > $arg2) ? 1 : 0**    <br>
Stores a value of **1** in `$argD` if `$arg1` is **greater than** `$arg2`; otherwise stores a **0**. <br>
The assembler will swap the order of `$arg1` and `$arg2` and transform this into a `LT` instruction.

##### GEQ
`GEQ $argD, $arg1, $arg2`       <br>
**$argD <- ($arg1 >= $arg2) ? 1 : 0**    <br>
Stores a value of **1** in `$argD` if `$arg1` is **greater than or equal to** `$arg2`; otherwise stores a **0**. <br>
The assembler will swap the order of `$arg1` and `$arg2` and transform this into a `LEQ` instruction.

##### NAND
`NAND $argD, $arg1, $arg2`       <br>
**$argD <- ~($arg1 & $arg2)**    <br>
Performs a NAND on `$arg1` and `$arg2` and stores the result in `$argD`.<br>
The assembler will expand this into two seperate `AND` and `NOT` instructions.

##### NOR
`NOR $argD, $arg1, $arg2`       <br>
**$argD <- ~($arg1 | $arg2)**    <br>
Performs a NOR on `$arg1` and `$arg2` and stores the result in `$argD`.<br>
The assembler will expand this into two seperate `OR` and `NOT` instructions.

##### NXOR
`NXOR $argD, $arg1, $arg2`       <br>
**$argD <- ~($arg1 ^ $arg2)**    <br>
Performs a NXOR on `$arg1` and `$arg2` and stores the result in `$argD`.<br>
The assembler will expand this into two seperate `XOR` and `NOT` instructions.

##### CPY
`CPY $argD, $arg1`       <br>
**$argD <- $arg1**    <br>
Copies the value stored in `$arg1` into `$argD`.<br>
The assembler will transform this into an `ADD` instruction.

##### LA
`LA $argD, imm`      <br>
**$argD <- MemLoc(imm)**        <br>
Stores the memory location of `imm` into `$argD`.<br>
The assembler will expand this into `LUI` and `ORI` instructions.

##### LV
`LV $argD, imm`
**$argD <- imm**        <br>
Stores the value of `imm` into `$argD`.<br>
The assembler will expand this into `LUI` and `ORI` instructions.

##### CLR
`CLR $argD`       <br>
**$argD <- $zero**    <br>
Clears (zeroes-out) the contents of `$argD`.<br>
The assembler will transform this into an `ADD` instruction.

##### BGT
`BGT $arg1, $arg2, imm`        <br>
**$arg1 > $arg2 ? PC <- 4*imm : PC <- (PC + 4)**        <br>
Branches to `imm` if `$arg1` is **greater than** `$arg2`; otherwise, advances to the next instruction. <br>
The assembler will swap the order of `$arg1` and `$arg2` and transform this into a `BLT` instruction.

##### BGE
`BGE $arg1, $arg2, imm`        <br>
**$arg1 >= $arg2 ? PC <- 4*imm : PC <- (PC + 4)**        <br>
Branches to `imm` if `$arg1` is **greater than or equal to** `$arg2`; otherwise, advances to the next instruction. <br>
The assembler will swap the order of `$arg1` and `$arg2` and transform this into a `BLE` instruction.

##### GOTO
`GOTO imm`        <br>
**PC <- 4*imm**        <br>
Unconditionally branches to `imm`. <br>
The assembler will transform this into a `BEQ` instruction.

##### JMP
`JMP $argD`        <br>
**$ra <- (PC + 4), PC <- $argD** <br>
Jumps to the address of the subroutine stored in `$arg1` and stores the previous next instruction as the return address in `$ra`. <br>
The assembler will transform this into a `JAL` instruction.

##### RET
`RET`   <br>
**PC <- $ra**   <br>
Returns the PC to the memory location stored in the `$ra` (return address) register. <br>
The assembler will transform this into a `JAL` instruction.

##### PUSH
`PUSH $arg1`    <br>
**Mem[$sp] <- $arg1, $sp - WORD_SIZE**  <br>
Pushes the word value of `$arg1` onto the stack, and grows the stack pointer (moves up in memory). <br>
The assembler will expand this into `SW` and `ADDI` instructions.

##### POP
`POP $argD` <br>
**$sp + WORD_SIZE, $arg1 <- Mem[$sp]**  <br>
Shrinks the stack pointer (moves down in memory) and pops the word value at the stack pointer into `$argD`. <br>
The assembler will expand this into `LW` and `ADDI` instructions.

#### Directives

Assembler directives are prefixed with a `.`, and are not mapped to machine instructions.

##### .NAME
`.NAME label 0xBEEF`    <br>
Instructs the assembler to track a new variable in memory with the name (`label`) and value (`0xBEEF`) specified.

##### .ORIG
`.ORIG 0xBEEF`  <br>
Instructs the assembler to start the following instructions at the given memory location (`0xBEEF`).
