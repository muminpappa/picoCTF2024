# FactCheck #

## Description ##

This binary is putting together some important piece of
information... Can you uncover that information? Examine this file. Do
you understand its inner workings?

No Hints.

## Solution ##

Ghidra makes a decent job analyzing this binary produced from C++
code. From the resulting code, it seems like the remaining part of the
flag is appended character by character from individual values,
sometimes based on conditions. After some failed attempts in `gdb`
with breakpoints at the `+=` operators of `basic_string` to capture
the characters and / or the new string, it seems easier to evaluate
the code by hand.

First I assign meaningful names to the variables. I choose names that
represent their contents:

``` c++
undefined8 main(void)

{
  char cVar1;
  char *pcVar2;
  long in_FS_OFFSET;
  allocator<char> local_249;
  basic_string<> ctf_str [32];
  basic_string c_7 [32];
  basic_string<> c_5 [32];
  basic_string c_9 [32];
  basic_string c_3 [32];
  basic_string c_0 [32];
  basic_string c_4 [32];
  basic_string c_a [32];
  basic_string<> c_e [32];
  basic_string c2_a [32];
  basic_string<> c_d [32];
  basic_string<> c_b [32];
  basic_string c_2 [32];
  basic_string<> c_6 [32];
  basic_string c2_4 [32];
  basic_string c2_3 [32];
  basic_string<> c_8 [40];
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  std::allocator<char>::allocator();
                    /* try { // try from 001012cf to 001012d3 has its CatchHandler @ 00101975 */
  std::__cxx11::basic_string<>::basic_string((char *)ctf_str,(allocator *)"picoCTF{wELF_d0N3_mate_");
```

From here on, it's easy to evaluate the conditionals and to find the
missing characters for the flag by hand.
