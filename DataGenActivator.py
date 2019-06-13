from pwn import *


# for t in range(30, 301, 30):
#     # python DataGen.py Time MaxPeople Floor Speed [OutputFile]
#     for i in range(1, 11):
#         r = process(argv=['DataGen.py',str(t), '10', '10', '5',f'test1-t{t}-{i}'])
#         print(r.recv(200).decode('ascii'))
#         r.sendline('n')
#         print(r.recvall().decode('ascii'))
#         r.close()

# for f in range(5, 11):
#     # python DataGen.py Time MaxPeople Floor Speed [OutputFile]
#     for i in range(1, 11):
#         r = process(argv=['DataGen1.py','180', '10', str(f), '5',f'data/test2-f{f}-{i}'])
#         print(r.recv(200).decode('ascii'))
#         r.sendline('n')
#         print(r.recvall().decode('ascii'))
#         r.close()

# test3
# python DataGen.py Time MaxPeople Floor Speed [OutputFile]
for i in range(1, 11):
    while True:
        r = process(argv=['DataGen3.py','90', '5', '10', '5',f'data/test3-uppeak-{i}'])
        print(r.recv(200).decode('ascii'))
        r.sendline('n')
        msg = r.recvall().decode('ascii')
        print(msg)
        r.close()
        if 'Warning!' not in msg:
            break

for i in range(1, 11):
    while True:
        r = process(argv=['DataGen4.py','90', '5', '10', '5',f'data/test4-downpeak-{i}'])
        print(r.recv(200).decode('ascii'))
        r.sendline('n')
        msg = r.recvall().decode('ascii')
        print(msg)
        r.close()
        if 'Warning!' not in msg:
            break