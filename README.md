# CCCC - A very special "decompiler"

CCCC is a tool that lets you extract functions as bytecode strings you
can then drop into C source files, cast to function, then execute.

The bytecode strings are not made to be pretty, but I could add
a flag to make it a little bit prettier. For now, the strings are as
compact as they can be.

It follows absolutely no C best practice and is actually pretty rarely
useful, rendering your code immediately non-portable and fixed to
the architecture your code was originally made for (or whatever assembly
you used with `-a`)

It only works on linux despite being made in python (because it uses tools
that are built on that system)

It's just an excuse for me to experiment with compiled binaries, I guess.

## Usage

```
cccc [options] [--] objfile
```
Here are the various options you can pass to this program :

- `-k <symbol,...>` : A list of symbols to only keep
- `-s <section,...>` : A list of sections to only keep
- `-t <type>` : The type that corresponds to the C string unit
- `-a <id>` : Dumps the ASM string as a function named `id`
- `-D` : Dump all symbols (like objdump's -D)
- `-b <id>` : Dumps the input C function as a symbol named `id`
- `-f` : Append a function definition (for `-b` or `-a`)
  Renames the symbol as `id_fn` to name the function itself `id`
- `--args <args>` : The arguments of the function(s),
  with the parentheses (for `-b` and/or `-f`)
- `--returns <type>` : The return type of the function(s)
  (for `-b` and/or `-f`)

Adding `--` will tell it to stop reading options.

## Prerequisites

This tool requires `gcc` and `objdump` in your path.
If you are using this tool, you probably have them already installed.

## Example

This is a way you can use CCCC to drop a bunch of bytecode that will run the
`exit` syscall (linux, x86-64):

```c
__attribute__((section(".text#")))
const char exit_function[16] =
    "UH\x89\xe5H\xc7\xc0<\0\0\0\x0f\x05\x90]\xc3";
const void (*exit2)(volatile register long status) =
    (void(*)(long)) exit_function;

void _start(void)
{
    exit2(0); // This will exit using the provided exit code.
}
```

(Compile it using `gcc -nostdlib <source_file>` to get a usable result)

As mentioned, not that useful considering you can use `exit(n)` in literally
any circumstance, and that would be much more portable.

## Making of this program

This was made in a random Discord VC at 2AM. Don't expect clean code, or more
than a single massive commit. Don't even expect a docstring.

Also, this has nearly no error handling.
