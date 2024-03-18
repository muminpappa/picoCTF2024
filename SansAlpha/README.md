# SansAlpha #

https://play.picoctf.org/events/73/challenges/challenge/436?category=5&page=1

## Description ##

The Multiverse is within your grasp! Unfortunately, the server that
contains the secrets of the multiverse is in a universe where
keyboards only have numbers and (most) symbols.

Additional details will be available after launching your challenge
instance.

## Hints ##

Where can you get some letters?

## Solution ##

After connecting to the instance, I face a prompt

	SansAlpha$
	
Entering any command containing a letter causes a response

	SansAlpha: Unknown character detected

Ending the session with `CTRL+D` leads to

	Traceback (most recent call last):
	  File "/usr/local/sansalpha.py", line 12, in <module>
		if user_in[-1] != "\n":
	IndexError: string index out of range
	Connection to mimas.picoctf.net closed.

So there seems to be a Python script that filters certain
letters. After some testing it turns out that all letters and the
backslash are filtered. 

Approaches not working for me:

* Escaping from the Python script
* Uploading a file with `scp`
* Executing other commands directly w/o a terminal

Some exploration of the closer environment:

```
SansAlpha$ .[!.]*
bash: .bashrc: command not found

SansAlpha$ *
bash: blargh: command not found

SansAlpha$ ./*
bash: ./blargh: Is a directory

SansAlpha$ ../*
bash: ../ctf-player: Is a directory

SansAlpha$ ~
bash: /home/ctf-player: Is a directory

SansAlpha$ */*
bash: blargh/flag.txt: Permission denied

SansAlpha$ _1=(*/*)
SansAlpha$ ${_1[0]}
bash: blargh/flag.txt: Permission denied

SansAlpha$ ${_1[1]}
bash: blargh/on-alpha-9.txt: Permission denied

SansAlpha$ _1=(*)
SansAlpha$ ${_1[0]}
bash: blargh: command not found

SansAlpha$ ${_1[1]}
bash: on-calastran.txt: command not found

SansAlpha$ ${_1[2]}
```

So what can we execute? Let's look for something like `cat` to print
the flag to the screen:

```
SansAlpha$ _1=(/*/???)
SansAlpha$ ${_1[0]}
apt 2.0.6 (amd64)
Usage: apt [options] command

apt is a commandline package manager ...
```

Ok. Just need to iterate through `_1` now to find `cat`.

```
SansAlpha$ ${_1[1]}
Usage: mawk [Options] [Program] [file ...]

Program:
    The -f option value is the name of a file ...
```

Seems like `awk` links to `mawk`. Ok, also useful. Let's continue:

```
SansAlpha$ ${_1[2]}
c++: fatal error: no input files
compilation terminated.

SansAlpha$ ${_1[3]}
gcc: fatal error: no input files
compilation terminated.

SansAlpha$ ${_1[4]}
gcc: fatal error: no input files
compilation terminated.

SansAlpha$ ${_1[5]}
SansAlpha$ ${_1[6]}
${_1[6]}

SansAlpha$ ${_1[7]}
${_1[7]}
```

Seems like there is no `cat` in `/bin`. Ok, `awk` should work, too. It
is not possible to use

``` bash
awk '{ print }' file
```

but there is a shorthand for `print:

``` bash
awk '1' file
```

The command 

``` bash
SansAlpha$ _1=(/*/???)
SansAlpha$ _2=(*/*.*)
SansAlpha$ ${_1[1]} '1' ${_2[0]}
return 0 picoCTF{...}
```

That one was nice!
