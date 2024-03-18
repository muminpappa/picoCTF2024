# Classic Crackme 0x100 #

## Description ##

A classic Crackme. Find the password, get the flag! Binary can be
downloaded here. Crack the Binary file locally and recover the
password. Use the same password on the server to get the flag!

Additional details will be available after launching your challenge
instance.

## Hints ##

Let the machine figure out the symbols!

## Solution ##

Ghidra refuses to analyze the binary. So back to `gdb` and `lay
asm`. Stepping through the code I notice that after reading in the
password some magic happens before `memcmp()` is called, right before
something is printed out and the program returns. 

I place a breakpoint in `memcmp()` and examine the registers holding
the three arguments (see `man memcmp`):

``` gdb
(gdb) display /s $rdi
1: x/s $rdi  <error: No registers.>
(gdb) display /s $rsi
2: x/s $rsi  <error: No registers.>
(gdb) display /u $rdx
3: /u $rdx = <error: No registers.>
(gdb) rbreak memcmp
Breakpoint 1 at 0x401060
<function, no debug info> memcmp@plt;
```

The errors come from the fact that the program is not running. Now
let's see how the arguments to `memcmp()` look like:

``` gdb
(gdb) r
Starting program: /home/kali/tmp/Classic_Crackme_0x100/crackme100 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Enter the secret password: Hi

Breakpoint 1, 0x0000000000401060 in memcmp@plt ()
1: x/s $rdi  0x7fffffffdd50:    "HlQTQTTWQTTWTWWZQTTWTWWZTWWZWZZ]QTTWTWWZTWWZWZZ]TW"
2: x/s $rsi  0x7fffffffdd90:    "mpknnphjngbhgzydttvkahppevhkmpwgdzxsykkokriepfnrdm"
3: /u $rdx = 50
```

Running this several times with different passwords gives following
insights:

1. The first argument (address in `rdi`) contains the scrambled
   password.
2. The password scrambling uses a plain Vigenére-like rotation. 
3. Only rotations such as 0, -3, -6, -9 seem to occur

Now let's consider the hint and make the computer figure out the
correct password:

1. Start with an empty password.
2. While the password is shorter than the scrambled string in `rsi`,
   repeat:
   1. Take the first character of the scrambled correct password, for
   which the plaintext character is not known.
   2. For offsets 0, -3, -6 and so on
	  1. apply the offset to the scrambled character to guess a plain
      character (e.g. d becomes a as `d - a = 3`)
	  2. append the new guessed plaintext character to the password and
      try it out
	  3. If it appears to produce the correct scrambled character, keep
      the new password and break the loop.
3. Print the password.

The bash script to automate this is in
[`get_password.sh`](get_password.sh). It uses a [`gdb`
script](gdb_script).

Can probably be achieved much easier with Python. Or maybe completely
with `gdb` script?

## Useful things I learned on the way ##

* In `gdb`, `rbreak` sets breakpoint at function with matching name.
* In `bash`, the expression `${target:${#pw}:1}` returns a slice of the string in
  target, starting at length of the string in variable `pw`, and 1
  character long.
* In `bash`, `0x$(printf "%x" "'$c")` produces the hex number for
  the character in variable `c`. The single apostrophe is not a typo. 
* In `bash`,  `printf "%x" "$n"` produces the hex format of the number
  in variable `n`.
* In `bash`, `printf "\x$n"` results in the actual character
  represented by the hex number in variable `n`.
