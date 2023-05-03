---
title: "CyberSpace Kenya— StegaPwn"
author: "Trevor saudi"
date: 2021-01-24T10:49:06.490Z
lastmod: 2022-05-24T14:30:45+03:00

description: ""

subtitle: "Crontab Privilege escalation"

image: "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/1.png" 
images:
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/1.png"
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/2.png"
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/3.png"
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/4.jpeg"
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/5.png"
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/6.png"
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/7.png"
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/8.png"
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/9.png"
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/10.png"
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/11.png"
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/12.png"
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/13.png"
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/14.png"
 - "/posts/2021-01-24_cyberspace-kenya-stegapwn/images/15.png"


aliases:
    - "/cyberspace-kenya-stegapwn-721bed4e8600"

tags:
- Privesc
- Machine
- CTF

---

### Crontab Privilege escalation

In this awesome beginner friendly CTF, I will be taking you through how I rooted the box. [https://ctf.cyberspace.co.ke/vault/stegapwn](https://ctf.cyberspace.co.ke/vault/stegapwn)

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/1.png#layoutTextWidth)


The challenge is divided into guiding questions. From the name of the challenge, we can deduce some steganography and Pwning will be involved.
> **_What is the IP, passphrase, username, password?_**

Starting off with steganography, I downloaded the cheetah image to my machine. Tried some low hanging fruits like viewing the strings of the image using `strings `command. `exiftool` to extract some metadata from the image. `xxd `to check for some corrupted bytes, `stegsolve `and `binwalk `but none gave in.

My last option was that some data was hidden in the image using a tool like steghide. This can be confirmed by viewing the header of the strings output.

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/2.png#layoutTextWidth)


Intuitively, this weird string is a common occurrence when hiding data using steghide. So I tried extracting the hidden data

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/3.png#layoutTextWidth)


Well, now we need the passphrase to get the contents. Stegextract is a tool for bruteforcing passphrases. But….using the rockyou wordlist(which has more than 8 million lines of text) with stegextract was a bad idea

My machine overheated a couple of times and even had to turn it off :(

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/4.jpeg#layoutTextWidth)


After thinking on how i could optimize the bruteforce approach, I noticed an unintended hint from the challenge. The length of the passphrase is expected to be 11 characters from the number of asterix used as placeholders for the answer

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/5.png#layoutTextWidth)


Filtered out all words not equal to 11 characters.

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/6.png#layoutTextWidth)


Ran the bruteforce again without melting my motherboard :)

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/7.png#layoutTextWidth)


At the time of writing this article, I found out about a tool from a friend of mine called stegseek that goes through the rockyou wordlist in less than 10 seconds. I guess I know what tool to use next time in a similar challenge.

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/8.png#layoutTextWidth)

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/9.png#layoutTextWidth)


### Privilege escalation

Now we ssh into the box using the credentials given, and attempt to gain root access.

Running linpeas for automatic enumeration for privilege escalation vectors,

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/10.png#layoutTextWidth)


We have a writable script at /usr/local/sbin called runshell.sh that a hint reveals to be a cronjob running as root.

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/11.png#layoutTextWidth)


Running a process monitor also shows the script being executed after a certain period of time

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/12.png#layoutTextWidth)


Nice. So we can try using a reverse shell inside the runshell.sh script to get back a connection with the UID=1000 which belongs to a user called r374RD

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/13.png#layoutTextWidth)


I used ngrok to portforward on port 1234, got the shell back where 3.138.180.119 is the hostname for my forwarded IP.

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/14.png#layoutTextWidth)


Gives back a reverse shell after 5 minutes. sudo -l reveals we can run any commands as SUDO so I switched to root user by `sudo su` Flag is in the root directory.

Happy hacking :)

![image](/posts/2021-01-24_cyberspace-kenya-stegapwn/images/15.png#layoutTextWidth)


Happy hacking :)