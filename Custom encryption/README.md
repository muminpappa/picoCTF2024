# Custom encryption #

## Description ##

> Can you get sense of this code file and write the function that will
> decode the given encrypted file content. Find the [encrypted file
> here](enc_flag) and [code file](custom_encryption.py) might be good to
> analyze and get the flag.
>
> ## Hints ##
>
> Understanding encryption algorithm to come up with decryption
> algorithm.

## Solution ##

Decryption here means to reverse the encryption process, i.e. going
backwards:

1. Feed the integer array into a `decrypt()` function that returns a
   "semicipher" string. Basically
   
   * divide each integer by `311 * key`
   * convert result to character
   * append to semicipher
   
   The `key` is the `shared_key` from the encryption script; we can
   just calculate it with the given code, hardcoding the values for
   `a` and `b` instead of choosing random values.
   
2. Feed the `semicipher` backwards into
   `dynamic_xor_encrypt(plain_text, text_key)`. Reverse the string
   result.
   
The full code that prints the flag is in
[`custom_decryption.py`](custom_decryption.py).
