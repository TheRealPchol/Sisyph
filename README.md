# Sisyph

**Sisyph** is an imperative, line-oriented programming language. A program is a sequence of command lines executed line by line by a Python interpreter. Sisyph does not invent its own arithmetic or logic — every expression and variable value is a Python expression. The language takes care of program structure (labels, jumps, subroutines), while all computation is delegated to Python.

The project ships with **BSYHC** (Base Sisyph Compiler) — a compiler that packs `.syh` files into self-contained Python executables, and five standard libraries written in Sisyph itself.

## Features

- Simple line-oriented syntax: each line is one command
- Labels (`@name`), unconditional jumps (`goto`), subroutines with a call stack (`goto back`)
- Single-line conditionals: `if <expression> then <command>`
- Built-in libraries: `stdlib` (I/O), `v` (types), `file` (files), `pylib` (raw Python), `dc` (data classes)
- Any Python expression works anywhere: f-strings, comprehensions, `__import__`
- Line comments with `~~` (everything after `~~` is ignored)
- Multiple commands per line with `;` separator
- `include` mechanism for reusing code and libraries
- **BSYHC compiler**: compile to a self-contained `.py` or a binary (ELF/EXE via PyInstaller), decompile back, merge multiple files into one
- Standard libraries: `mathlib`, `strlib`, `listlib`, `randlib`, `timelib`
- Documentation in 5 languages × 3 formats (Markdown, plain text, HTML)

## Requirements

- Python 3 (no third-party dependencies)

## Quick start

Clone or download the project, then run a program:

```bash
python3 main.py a.syh          # interpret a program
python3 main.py b.syh          # interactive example (guessing game)
```

Hello, world:

```
include stdlib

stdlib.stdout "Hello, world!"
exit 0
```

## Project structure

```
.
├── main.py              # the Sisyph interpreter
├── bsyhc.py             # BSYHC: compiler / decompiler / interpreter driver
├── lib/
│   ├── mathlib.syh      # standard library: mathematics
│   ├── strlib.syh       # standard library: strings
│   ├── listlib.syh      # standard library: lists
│   ├── randlib.syh      # standard library: randomness
│   └── timelib.syh      # standard library: time
├── examples/
│   ├── guess.syh        # "guess the number" game (randlib, strlib)
│   └── math_demo.syh    # mathlib + listlib demo
├── docs/
│   ├── ru-ru/           # Russian documentation (md/txt/html + examples)
│   ├── en-en/           # English (UK) documentation
│   ├── en-ua/           # English (US) documentation
│   ├── de-ge/           # German documentation
│   └── sp-sp/           # Spanish documentation
├── a.syh, b.syh         # example programs
└── bsyhc.txt            # original BSYHC specification
```

## Interpreter (`main.py`)

Run a `.syh` program:

```bash
python3 main.py program.syh
```

Language basics:

```
include v
include stdlib

@main
stdlib.stdin name "What is your name? "
v.str greeting f"Hello, {name}!"
stdlib.stdout greeting
goto end

@end
exit 0
```

Commands: `include`, `goto`, `goto back`, `exit`, `if ... then`, and the built-in libraries `stdlib` (`stdlib.stdout`, `stdlib.stdin`), `v` (`v.int`, `v.str`, `v.float`, `v.bool`, `v.list`), `file` (`file.read/write/append/delete/exists/lines`), `pylib` (direct access to Python), `dc` (`dc.mkdc/set/get/remkey/move/copy/copy2var/move2var` — data classes).

## Compiler (`bsyhc.py`)

BSYHC (Base Sisyph Compiler) packs a `.syh` file into an array (one line per element), embeds a copy of the interpreter, and runs the program straight from the array. The compiled `.py` is **self-contained** — it does not require `main.py`.

```bash
# compile
python3 bsyhc.py -i b.syh -c -o bsyhc-test-b.py

# compile to a binary (ELF via PyInstaller, Linux)
python3 bsyhc.py -i b.syh -c -elf -o b_bin

# compile to a binary (EXE via PyInstaller, Windows)
python3 bsyhc.py -i b.syh -c -exe -o b.exe

# decompile back to .syh
python3 bsyhc.py -i bsyhc-test-b.py -d -o b-de.syh

# decompile a built binary back to .syh
python3 bsyhc.py -i b_bin -d -o b-de.syh

# interpret (same as main.py)
python3 bsyhc.py -i b.syh
```

Compile several files into one executable and embed the libraries:

```bash
python3 bsyhc.py -i guess.syh -i lib/randlib.syh -i lib/strlib.syh -c --merge include -o guess.py
python3 guess.py
```

Flags: `-i/--input` (repeatable), `-o/--output`, `-c/--compile`, `--py` (generate only the intermediate `.py` for a manual PyInstaller build), `-d/--decompile`, `-elf` (compile to an ELF binary via PyInstaller on Linux), `-exe` (compile to an EXE binary via PyInstaller on Windows), `-k/--keep-intermediate` (keep the intermediate `.py` when building a binary), `--merge concat|include`, `--split` (restore each source file on decompilation).

Binary builds require [PyInstaller](https://pyinstaller.org) (`pip install pyinstaller`; the project's `env/` includes it). The build runs in a temporary directory — `build/`, `dist/`, `*.spec` and the intermediate `.py` are removed automatically, only the final binary remains. PyInstaller cannot cross-compile, so on Linux `-exe` produces a native binary named `*.exe`; a real Windows EXE must be built on Windows. Binaries built by BSYHC can be decompiled back into `.syh` with `-d`.

### Intermediate Python file

`-c` produces a self-contained `.py` — this file *is* the intermediate representation that PyInstaller turns into a binary for `-elf` / `-exe`. Generate it explicitly with `--py` and build the binary yourself, step by step:

```bash
python3 bsyhc.py -i b.syh --py -o app.py                    # step 1: intermediate .py (prints the PyInstaller command)
pyinstaller --onefile --noconfirm --name app app.py         # step 2: manual binary build
```

During a regular `-elf` / `-exe` build the intermediate `.py` lives in a temporary directory and is deleted afterwards. Use `-k` to keep it next to the binary and get the exact rebuild command printed:

```bash
python3 bsyhc.py -i b.syh -c -elf -o b_bin -k               # builds b_bin and keeps b_bin.py
```

## Standard libraries

Libraries are ordinary `.syh` files: load with `include <name>`, call subroutines with `goto <name>.<subroutine>`. A subroutine reads its input variables (each library has its own prefix) and writes the result into `<prefix>_result`. The library files live in `lib/` and are referenced without a path — `include` first looks for `<name>.syh` in the current directory, then in `lib/`. For distribution, copy the needed `.syh` files or compile everything into one executable with BSYHC (`--merge include`).

| Library | Prefix | Provides |
|---|---|---|
| `mathlib.syh` | `ml_` | `abs`, `sign`, `min2`, `max2`, `clamp`, `pow`, `is_even`, `is_odd`, `factorial`, `gcd` |
| `strlib.syh` | `sl_` | `upper`, `lower`, `capitalize`, `length`, `strip`, `reverse`, `contains`, `replace`, `split`, `join`, `is_digit` |
| `listlib.syh` | `ll_` | `length`, `sum`, `min`, `max`, `sort`, `reverse`, `unique`, `contains`, `append`, `range_n` |
| `randlib.syh` | `rl_` | `randint`, `uniform`, `choice`, `shuffle` |
| `timelib.syh` | `tl_` | `now`, `strftime`, `sleep` |

Example:

```
include v
include stdlib
include mathlib

v.int ml_x 5
goto mathlib.factorial
stdlib.stdout f"5! = {ml_result}\n"
exit 0
```

```
5! = 120
```

## Documentation

Full reference documentation is available in five languages, each in three formats (Markdown, plain text, HTML) with example programs:

- **Russian** — `docs/ru-ru/`
- **English (UK)** — `docs/en-en/`
- **English (US)** — `docs/en-ua/`
- **German** — `docs/de-ge/`
- **Spanish** — `docs/sp-sp/`

Each documentation set covers the language, all built-in libraries, the BSYHC compiler and the standard libraries.

## License

MIT. See [LICENSE](LICENSE).

---

© Sisyph Language
