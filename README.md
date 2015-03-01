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

An instruction word in Niu32 is 32 bits long. We will start counting from **bit 0** (most-significant) to **bit 31** (least-significant).

An instruction word can be divided into the following fields:

- **Primary opcode (OP1)**. Signals the processor what instruction to perform, or alternatively signals the processor to check the **secondary opcode** to figure out what instruction to perform.

- **Source register arguments (ARG1, ARG2)**. Specifies which registers to reference. The values stored in these registers will be used in evaluation of the instruction.

- **Destination register (ARGD)**. Specifies which register to store the result of the operation after it has completed.

- **Immediate value (IMM)**. A number used in some types of instructions instead of a secondary register argument. The value given in the instruction will be directly used in the evaluation of the instruction.

- **Secondary opcode (OP2)**. Signals the processor what instruction to perform. Primarily used in non-immediate ALU instructions, where the secondary opcode is used to specify the `ALUop` signal (see below).

An instruction word can take one of two formats. Fields are shown at the top, and the bits they correspond to are shown at the bottom. Bit ranges are *inclusive* (i.e. "bits 4-0" *include both bit 4 and bit 0*)

**Non-immediate**:

| OP1 |ARG1 |ARG2 |ARGD |*empty*| OP2 |
|:---:|:---:|:---:|:---:|:-----:|:---:|
|xxxxx|xxxxx|xxxxx|xxxxx|0000000|xxxxx|
|31-27|26-22|21-17|16-12|  11-5 | 4-0 |
