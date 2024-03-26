# C3 #

> ## Description ##
>
> This is the Custom Cyclical Cipher! Download the
> [ciphertext](ciphertext) here. Download the [encoder](convert.py)
> here. Enclose the flag in our wrapper for submission. If the flag
> was "example" you would submit "picoCTF{example}".
>
> ## Hints ##
>
> Modern crypto schemes don't depend on the encoder to be secret, but
> this one does.

## Solution ##

### First step ###

The back conversion needs reverse the steps. That means iterate
  backwards over the ciphertext, last character to first character

1. calculate the previous index from the current index and the index
  of the current encrypted value in `lookup2`,
2. look up the the decrypted value in `lookup1` and prepend it to the
   decrypted message,
3. set the current index to the value of the previous index.

As the initial value for `prev` is not known, put a look around it to
try out all 40 values, and break that loop when the final value of
`cur` becomes 0.

The script is in [`convert_back.py`](convert_back.py). When run as

``` bash
python3 convert_back.py < ciphertext 
```

it prints a Python2 script with some more hints:

``` python
#asciiorder
#fortychars
#selfinput
#pythontwo

chars = ""
from fileinput import input
for line in input():
    chars += line
b = 1 / 1

for i in range(len(chars)):
    if i == b * b * b:
        print chars[i] #prints
        b += 1 / 1
```

It seems crucial to really keep that script exactly, so better write
it to a file with

``` bash
python3 convert_back.py < ciphertext decode.py
```

## Second step ##

The script needs Python 2. After trying some inputs I feed the script
to itself ("selfinput") and the resulting string (printed vertically)
works as contents of the flag. 

``` bash
python2 decode.py < decode.py
```

