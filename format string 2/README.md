# format string 2 #

> ## Description ##
>
> This program is not impressed by cheap parlor tricks like reading
> arbitrary data off the stack. To impress this program you must
> change data on the stack! Download the binary here. Download the
> [source here](vuln.c).
>
> Additional details will be available after launching your challenge
> instance.
>
> ## Hints ##
>
> pwntools are very useful for this problem!

## Solution ##

This challenge really helps to get familiar with `pwnlib`. With the
help of a `%n` instruction, it is possible to write to the memory of a
process. However, crafting the format string manually is tedious. The
`fmtstr` module of `pwnlib` can generate a suitable payload based on

1. the offset (i.e. which argument)
2. the address(es) to overwrite
3. what to write to these addresses

``` python
payload = fmtstr_payload(offset, {addr: flag})
```

Let's figure out address and what to write there first: The **address**
can be found with e.g. `readelf` or `objdump`:

``` bash
objdump -Ds vuln | grep sus
```

	402040 68616e67 65206d79 20737573 70696369  hange my suspici
    4020e0 00257300 73757320 3d203078 25780a00  .%s.sus = 0x%x..
    404060 73757321                             sus!            
     401273:       8b 05 e7 2d 00 00       mov    0x2de7(%rip),%eax        # 404060 <sus>
     4012df:       8b 05 7b 2d 00 00       mov    0x2d7b(%rip),%eax        # 404060 <sus>

``` bash
readelf -s vuln | grep sus
```

	28: 0000000000404060     4 OBJECT  GLOBAL DEFAULT   25 sus

So the global variable `sus` we need to overwrite is at
`0x404060`, 4 bytes long. From line 18 of the source code we see that
the value should be changed to `0x67616c66`. That's the easy part.

How to find the offset? Fortunately, the `FmtStr` class can figure out
that by itself; it just needs a function to call for communication
with the vulnerable process. This function sends data to and receives
data from `vuln`, it basically mimics the interaction with the
user. The key is that it should return the payload so that `FmtStr`
can determine the offset.

As the data entered by the user is reflected back in the line 

	Here's your input: <data>
	
the most obvious way was to

* `decode()` that line,
* `split(' ')`,
* select element 3 of the list, and
* `encode()` it again.

Using this helper function `exec_fmt()`, it should now be possible to
determine the offset. However, this failed with below error:

	File "/usr/lib/python3/dist-packages/pwnlib/util/packing.py", line 149, in pack
	   raise ValueError("pack(): number does not fit within word_size [%i, %r, %r]" % (0, number, limit))
	ValueError: pack(): number does not fit within word_size [0, 140721382761552, 4294967296]

The reason is that the value of `context.bits` was set to 32. Setting
`context.arch = 'amd64'` made things work.

Here is the [complete solution](pwn_this_format.py).

## Learnings ##

* pwnlib is awesome, e.g. for format string vulnerabilities
* While using `pwn` set the correct `context.arch`, e.g. 'amd64'
* `pwn` can determine the offset for format string automatically, see
  https://docs.pwntools.com/en/stable/fmtstr.html#module-pwnlib.fmtstr
* `pwnlib.fmtstr_payload()` can generate payload to write to memory
