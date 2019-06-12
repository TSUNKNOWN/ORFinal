from pwn import *


for t in range(30, 301, 30):
    # python DataGen.py Time MaxPeople Floor Speed [OutputFile]
    for i in range(1, 11):
        r = process(argv=['DataGen.py',str(t), '10', '10', '5',f'test1-t{t}-{i}'])
        print(r.recv(200).decode('ascii'))
        r.sendline('n')
        print(r.recvall().decode('ascii'))
        r.close()

for f in range(5, 11):
    # python DataGen.py Time MaxPeople Floor Speed [OutputFile]
    for i in range(1, 11):
        r = process(argv=['DataGen.py','180', '10', str(f), '5',f'test2-f{t}-{i}'])
        print(r.recv(200).decode('ascii'))
        r.sendline('n')
        print(r.recvall().decode('ascii'))
        r.close()
