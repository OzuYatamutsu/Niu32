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

An instruction word in Niu32 is 32 bits long.
