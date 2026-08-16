# Sisyph — Documentation

**Sisyph** is an imperative, line-oriented programming language. A program is a sequence of command lines executed one by one by an interpreter written in Python (`main.py`).

The key feature: Sisyph does not invent its own arithmetic or logic — every expression and variable value is a Python expression. The language is responsible for the structure of the program (labels, jumps, subroutines), while all computation is delegated to the Python interpreter.

## Table of Contents

1. [About the Language](#1-about-the-language)
2. [Running Programs](#2-running-programs)
3. [Syntax](#3-syntax)
4. [Control Commands](#4-control-commands)
5. [The stdlib Library](#5-the-stdlib-library)
6. [The v Library](#6-the-v-library)
7. [The file Library](#7-the-file-library)
8. [The pylib Library](#8-the-pylib-library)
9. [Example Programs](#9-example-programs)
10. [Limitations and Peculiarities](#10-limitations-and-peculiarities)
11. [Error Messages](#11-error-messages)
12. [Ecosystem](#12-ecosystem)
13. [BSYHC — The Compiler](#13-bsyhc--the-compiler)
14. [Language Libraries](#14-language-libraries)

## 1. About the Language

| Property | Value |
|---|---|
| Name | Sisyph |
| File extension | `.syh` |
| Paradigm | imperative, line-oriented |
| Interpreter | `main.py` (Python 3) |
| Expressions | Python (`eval` / `exec`) |
| Typing | dynamic (Python types) |
| Scope | global (single Python namespace) |

## 2. Running Programs

Run a program with the command:

```
python3 main.py program.syh
```

Example:

```
python3 main.py a.syh
```

If the file is not found, the interpreter prints an error message and stops.

The program can also be run through the BSYHC compiler in interpret mode (see [section 13](#13-bsyhc--the-compiler)):

```
python3 bsyhc.py -i program.syh
```

## 3. Syntax

A program consists of lines. Each line contains a single command. Empty lines are ignored.

### Command separator

Several commands can be written on one line, separated by semicolons:

```
goto check; goto back
```

### Labels

A label is the name of a line you can jump to. A label starts with the `@` character and occupies its own line:

```
@main
stdlib.stdout "Hello!"
```

Lines containing labels are skipped during execution.

### Comments

The language has no dedicated comment syntax. Since expressions are processed by Python, you can use the Python comment character `#` inside expressions.

### Case sensitivity

Commands are case-sensitive: `goto` is a command, `GOTO` is not.

### Variables

Variables are created implicitly by the `v.*`, `stdlib.stdin`, `file.*` and `pylib.*` commands. No explicit declaration is needed. Variable names are ordinary Python names.

## 4. Control Commands

### include

Loads a library file or a built-in library:

```
include name
```

If the file `name.syh` exists, its lines are appended to the end of the current program, and the file's labels become available with the prefix `name.label`:

```
include lib
goto lib.start
```

If the file does not exist, `name` is treated as a built-in library. Built-in libraries: `stdlib`, `v`, `file`, `pylib`.

### goto

Unconditional jump to a label:

```
goto label
```

The position of the jump is saved on the call stack, so you can return to it later.

### goto back

Return from a subroutine:

```
goto back
```

Pops the position of the last jump from the call stack and resumes execution there. If the stack is empty, an error message is printed.

Example subroutine:

```
@main
goto work
exit 0

@work
stdlib.stdout "working..."
goto back
```

### exit

Terminates the program:

```
exit
exit 0
exit 5
```

- `exit` / `exit 0` — successful termination, prints `The program has completed successfully.`
- `exit <code>` — termination with a code, prints `The program terminated with code "<code>".`

### if

Single-line conditional execution:

```
if <expression> then <command>
```

If the expression is truthy (converted to `bool` in Python), the command after `then` is executed. There is no `else`.

Example:

```
if x > 10 then goto big
if x <= 10 then goto small
```

## 5. The stdlib Library

Add `include stdlib` to use it.

### stdlib.stdout

Prints the value of an expression:

```
stdlib.stdout <expression>
```

The expression is evaluated by Python; f-strings are supported:

```
stdlib.stdout f"Value: {x}"
```

### stdlib.stdin

Reads a string from the keyboard:

```
stdlib.stdin <variable> <prompt>
```

The result is stored in the variable. The prompt can be a string or an expression:

```
stdlib.stdin name "What is your name? "
```

Read without storing:

```
stdlib.stdin <prompt>
```

## 6. The v Library

Add `include v` to use it.

The library converts the value of an expression to the given type and stores it in a variable:

| Command | Type |
|---|---|
| `v.int` | integer (`int`) |
| `v.str` | string (`str`) |
| `v.float` | floating-point number (`float`) |
| `v.bool` | boolean value (`bool`) |
| `v.list` | list (`list`) |

Syntax:

```
v.int x "42"
v.list l [1, 2, 3]
v.str s l[0]
```

## 7. The file Library

Add `include file` to use it.

| Command | Purpose |
|---|---|
| `file.read <variable> <path>` | reads the whole file into a variable |
| `file.write <path> <expression>` | writes the expression to a file (overwrites) |
| `file.append <path> <expression>` | appends the expression to the end of a file |
| `file.delete <path>` | deletes a file |
| `file.exists <variable> <path>` | stores `True`/`False` on whether the file exists |
| `file.lines <variable> <path>` | stores the list of the file's lines |

Example:

```
file.write "data.txt" f"line: {x}\n"
file.read content "data.txt"
file.exists ok "data.txt"
```

If a file cannot be read or deleted, `Sisyph File Error` is printed with the exception text, and the variable receives a default value (`""` or `[]`).

## 8. The pylib Library

Add `include pylib` to use it.

The library gives direct access to Python.

| Command | Purpose |
|---|---|
| `pylib.exec <code>` | executes arbitrary Python code |
| `pylib.eval <variable> <expression>` | evaluates an expression and stores the result |
| `pylib.import <module>` | imports a Python module |
| `pylib.importas <module> <alias>` | imports a module with an alias |
| `pylib.from <code>` | executes `from <code>` |
| `pylib.get <variable> <python variable>` | copies the value of a Python variable |
| `pylib.set <python variable> <expression>` | assigns a value to a Python variable |
| `pylib.print <expression>` | evaluates an expression and prints the result |

Example:

```
pylib.importas math m
pylib.set x m.sqrt(16)
pylib.print x
```

## 9. Example Programs

### Example 1. Lists and type conversion (`a.syh`)

```
include v
include stdlib

v.list l ["po", 14, 17.3, True, ["object"]]
v.str q l[0]
v.str w l[1]
v.str e l[2]
v.str r l[3]
v.str t l[4]
v.str u l[4][0]
stdlib.stdout f"{q}\n{w}\n{e}\n{r}\n{t}\n{u}\n"
exit 0
```

Output:

```
po
14
17.3
True
["object"]
object
```

### Example 2. Input, jumps and subroutines (`b.syh`)

```
include v
include stdlib

v.str false_o "Ты не угадал("
v.str true_o "Ты угадал!"

@main
stdlib.stdin sa "Введите строку: "
v.str object "НИЧЕГО"
goto check
exit 0

@check
if sa == object then goto true
if sa != object then goto false
goto back

@true
stdlib.stdout true_o
goto back

@false
stdlib.stdout false_o, "\n"
goto main
```

The program asks for a string, compares it with the word «НИЧЕГО» and prints the result. The subroutines `@true` and `@false` return via `goto back`.

## 10. Limitations and Peculiarities

- **No loops.** Repetition is organized solely through `goto`.
- **No functions.** Labels with `goto` / `goto back` serve as subroutines.
- **No local variables.** Everything lives in the global Python namespace.
- **No `else`.** Branching is only possible with `if ... then`.
- **Single-line `if`.** The command after `then` is a single one, though it may contain `;`.
- **Parsing by spaces and dots.** Arguments containing spaces (for example, file paths) are parsed unsafely: `file.write "my file.txt" x` will not work.
- **Shared call stack.** Recursive jumps are allowed but not limited.
- **Expressions are Python.** Any error in an expression is a Python error, not a Sisyph one.
- **`include` inserts code.** The included file is appended to the current program and executed when reached.

## 11. Error Messages

| Message | Situation |
|---|---|
| `Sisyph Error: File '<name>' not found.` | the program file was not found |
| `Sisyph Error: Unknown label '<label>'` | jump to a non-existent label |
| `Sisyph Error: Call stack is empty, nowhere to return` | `goto back` with an empty stack |
| `Sisyph File Error: <exception>` | a file operation error |
| `Sisyph PyLib Error: <type>: <message>` | a Python error in the pylib library |
| `The program has completed successfully.` | successful termination (`exit 0`) |
| `The program terminated with code "<code>"` | termination with a code |

## 12. Ecosystem

- **`.syh` files** — programs and libraries.
- **`include`** — the reuse mechanism: labels of other files are called with the file-name prefix (`name.label`).
- **Built-in libraries** — `stdlib` (input/output), `v` (types), `file` (files), `pylib` (Python).
- **`pylib`** — the extension point: any Python code is reachable from Sisyph without modifying the interpreter.
- **BSYHC** — the compiler: `bsyhc.py` packs `.syh` into a self-contained `.py`, supports decompilation and multi-file building (see [section 13](#13-bsyhc--the-compiler)).
- **Language libraries** — `mathlib`, `strlib`, `listlib`, `randlib`, `timelib`: subroutines for mathematics, strings, lists, randomness and time (see [section 14](#14-language-libraries)).

## 13. BSYHC — The Compiler

**BSYHC** (Base SisYpH Compiler, `bsyhc.py`) is the Sisyph compiler. It packs a `.syh` file into an array in which every new line is a new element of the array, embeds a copy of the interpreter into the output file and then runs the program straight from the array. The compiled `.py` file is self-contained and does not require `main.py` next to it.

### Modes

| Mode | Command |
|---|---|
| Compile | `python3 bsyhc.py -i b.syh -c -o bsyhc-test-b.py` |
| Decompile | `python3 bsyhc.py -i bsyhc-test-b.py -d -o b-de.syh` |
| Interpret | `python3 bsyhc.py -i b.syh` |

If only an input file is given (without `-c` and `-d`), BSYHC simply interprets the program, just like `main.py`.

### Flags

| Flag | Purpose |
|---|---|
| `-i, --input <file>` | input file; may be repeated to compile several files into one output |
| `-o, --output <file>` | output file (default: `<input>.py` / `<input>.syh`) |
| `-c, --compile` | compile `.syh` into a self-contained `.py` |
| `-d, --decompile` | decompile a compiled `.py` back into `.syh` |
| `--merge concat \| include` | how to merge files when compiling (default `concat`) |
| `--split` | on decompilation, restore each source file separately (into the `-o` directory) |

### Compiling several files

`-i` may be repeated — all files are collected into a single output:

```
python3 bsyhc.py -i main.syh -i lib.syh -c -o program.py
```

- `--merge concat` — the lines of the files are simply joined in order.
- `--merge include` — the first file is the entry point, the rest are appended as with `include`: their labels get the prefix `file.label` (for example, `goto lib.start`).

### Decompilation

The compiled file is easy to decompile — the program is restored from the array:

```
python3 bsyhc.py -i bsyhc-test-b.py -d -o b-de.syh
```

By default a single merged `.syh` is produced. With the `--split` flag every source file is restored separately into the directory given via `-o`.

## 14. Language Libraries

The language ships with subroutine libraries — ordinary `.syh` files that are loaded with `include` and called via `goto <library>.<subroutine>`. The files live in the `lib/` directory and are referenced without a path.

### Conventions

- A file is loaded with `include <name>`, a subroutine is called with `goto <name>.<subroutine>` and returns with `goto back`.
- A subroutine reads its input variables (each library has its own prefix) and writes the result into the `<prefix>_result` variable.
- Data is passed through global variables, so they must be reset before every call.
- There are no loops inside subroutines: every `goto` pushes a position onto the call stack, so a loop inside a subroutine would clutter the stack. Repetition is organized in the main program code.
- The BSYHC compiler can embed libraries directly into the compiled file — see section 13, the `--merge include` flag.

### Example

```
include v
include stdlib
include mathlib

v.int ml_x 5
goto mathlib.factorial
stdlib.stdout f"5! = {ml_result}\n"
exit 0
```

### lib/mathlib.syh — mathematics (prefix `ml_`)

| Subroutine | Input | Output | Description |
|---|---|---|---|
| `mathlib.abs` | `ml_x` | `ml_result` | absolute value |
| `mathlib.sign` | `ml_x` | `ml_result` | sign of the number: −1, 0 or 1 |
| `mathlib.min2` | `ml_a`, `ml_b` | `ml_result` | the smaller of two numbers |
| `mathlib.max2` | `ml_a`, `ml_b` | `ml_result` | the greater of two numbers |
| `mathlib.clamp` | `ml_x`, `ml_lo`, `ml_hi` | `ml_result` | value restricted to the bounds |
| `mathlib.pow` | `ml_a`, `ml_b` | `ml_result` | `a` to the power of `b` |
| `mathlib.is_even` | `ml_x` | `ml_result` | whether the number is even |
| `mathlib.is_odd` | `ml_x` | `ml_result` | whether the number is odd |
| `mathlib.factorial` | `ml_x` | `ml_result` | factorial of the number |
| `mathlib.gcd` | `ml_a`, `ml_b` | `ml_result` | greatest common divisor |

### lib/strlib.syh — strings (prefix `sl_`)

| Subroutine | Input | Output | Description |
|---|---|---|---|
| `strlib.upper` | `sl_text` | `sl_result` | string in upper case |
| `strlib.lower` | `sl_text` | `sl_result` | string in lower case |
| `strlib.capitalize` | `sl_text` | `sl_result` | string with a capital first letter |
| `strlib.length` | `sl_text` | `sl_result` | length of the string |
| `strlib.strip` | `sl_text` | `sl_result` | string without edge whitespace |
| `strlib.reverse` | `sl_text` | `sl_result` | reversed string |
| `strlib.contains` | `sl_sub`, `sl_text` | `sl_result` | whether the substring is present |
| `strlib.replace` | `sl_text`, `sl_old`, `sl_new` | `sl_result` | substring replacement |
| `strlib.split` | `sl_text`, `sl_sep` | `sl_result` | split the string into a list |
| `strlib.join` | `sl_list`, `sl_sep` | `sl_result` | join a list into a string |
| `strlib.is_digit` | `sl_text` | `sl_result` | whether the string consists only of digits |

### lib/listlib.syh — lists (prefix `ll_`)

| Subroutine | Input | Output | Description |
|---|---|---|---|
| `listlib.length` | `ll_list` | `ll_result` | number of elements |
| `listlib.sum` | `ll_list` | `ll_result` | sum of elements |
| `listlib.min` | `ll_list` | `ll_result` | minimum element |
| `listlib.max` | `ll_list` | `ll_result` | maximum element |
| `listlib.sort` | `ll_list` | `ll_result` | ascending sort |
| `listlib.reverse` | `ll_list` | `ll_result` | list in reverse order |
| `listlib.unique` | `ll_list` | `ll_result` | list without duplicates |
| `listlib.contains` | `ll_item`, `ll_list` | `ll_result` | whether the list contains the item |
| `listlib.append` | `ll_list`, `ll_item` | `ll_result` | list with the item appended |
| `listlib.range_n` | `ll_n` | `ll_result` | numbers from 0 to `n-1` |

### lib/randlib.syh — randomness (prefix `rl_`)

| Subroutine | Input | Output | Description |
|---|---|---|---|
| `randlib.randint` | `rl_a`, `rl_b` | `rl_result` | random integer within the bounds (inclusive) |
| `randlib.uniform` | `rl_a`, `rl_b` | `rl_result` | random floating-point number |
| `randlib.choice` | `rl_list` | `rl_result` | random element of the list (as a string) |
| `randlib.shuffle` | `rl_list` | `rl_result` | shuffled copy of the list |

### lib/timelib.syh — time (prefix `tl_`)

| Subroutine | Input | Output | Description |
|---|---|---|---|
| `timelib.now` | — | `tl_result` | current timestamp (seconds since the epoch) |
| `timelib.strftime` | `tl_fmt` | `tl_result` | current time by format (e.g. `"%Y-%m-%d %H:%M:%S"`) |
| `timelib.sleep` | `tl_sec` | — | pause execution for the given number of seconds |

---

© Sisyph Language. Documentation corresponds to the `main.py` interpreter and the `bsyhc.py` compiler.