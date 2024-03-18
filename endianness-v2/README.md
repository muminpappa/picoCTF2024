# endianness-v2 #

## Description ##

Here's a file that was recovered from a 32-bits system that organized
the bytes a weird way. We're not even sure what type of file it
is. Download it here and see what you can get out of it

No hints

## Solution ##

Check the first bytes of `challengefile`:

``` bash
hexdump -n 32 challengefile                                                                 
```

results in:
       
``` comments
0000000 ffe0 ffd8 4a46 0010 0001 4946 0001 0100
0000010 0000 0001 0043 ffdb 0606 0008 0508 0706
0000020
```

The magic bytes `ffe0 ffd8` indicate that this might be a jpeg file
(https://en.wikipedia.org/wiki/List_of_file_signatures), just stored
32-bit little-endian. 

Luckily, 

``` bash
xxd -e -g 4 challengefile | xxd -r > out.jpg
```

indeed produces a JPEG file that can be displayed to write down the
flag. 
	
## Learnings ##

* `xxd` with option `-g 4` groups bytes as 4.
* `xxd` with option `-e` treats the data as little-endian.
