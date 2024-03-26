import sys

enc_chars = sys.stdin.read()

lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"


for guess in range(0, 40):
    cur = guess
    out = ""
    for char in enc_chars[::-1]:
        prev = (cur - lookup2.index(char)) % 40
        out += lookup1[cur]
        cur = prev

    if cur == 0:
        break

sys.stdout.write(out[::-1])
