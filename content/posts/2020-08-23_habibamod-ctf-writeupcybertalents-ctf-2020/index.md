---
title: "Habibamod CTF writeup — CyberTalents CTF 2020"
author: "Trevor saudi"
date: 2020-08-23T12:36:41.827Z
lastmod: 2022-05-24T14:29:59+03:00

description: ""

subtitle: "CyberTalents organized a national CTF competition yesterday which my team and I participated and settled for 2nd place. This is a write-up…"

image: "/posts/2020-08-23_habibamod-ctf-writeupcybertalents-ctf-2020/images/1.png" 
images:
 - "/posts/2020-08-23_habibamod-ctf-writeupcybertalents-ctf-2020/images/1.png"
 - "/posts/2020-08-23_habibamod-ctf-writeupcybertalents-ctf-2020/images/2.png"
 - "/posts/2020-08-23_habibamod-ctf-writeupcybertalents-ctf-2020/images/3.png"
 - "/posts/2020-08-23_habibamod-ctf-writeupcybertalents-ctf-2020/images/4.png"
 - "/posts/2020-08-23_habibamod-ctf-writeupcybertalents-ctf-2020/images/5.png"
 - "/posts/2020-08-23_habibamod-ctf-writeupcybertalents-ctf-2020/images/6.png"


aliases:
    - "/habibamod-ctf-writeup-cybertalents-ctf-2020-fb5631e83e16"

---

_CyberTalents organized a national CTF competition yesterday which my team and I participated and settled for 2nd place. This is a write-up of the Habibamod challenge (Forensics category)._

**PART ONE: PCAP ANALYSIS**

We are given a .pcap file (packet capture file) that contains information about communication between 2 people.

Proceed to open the file using wireshark as shown below

![image](/posts/2020-08-23_habibamod-ctf-writeupcybertalents-ctf-2020/images/1.png#layoutTextWidth)


Scrolling through the different streams, you notice pieces of text captured during the communication. I then followed the TCP stream to get the full capture. Right click on the packet highlighted, click on follow, then TCP stream

![image](/posts/2020-08-23_habibamod-ctf-writeupcybertalents-ctf-2020/images/2.png#layoutTextWidth)


Voila! you get a dump of the communication data captured.

![image](/posts/2020-08-23_habibamod-ctf-writeupcybertalents-ctf-2020/images/3.png#layoutTextWidth)


The captured data consists of 2 parts. A string called data, and a base64 encoded string called encoder.

**PART TWO: Python Scripting**

I proceeded to decode the base64 data to ascii, giving us a function written in python to convert text to binary, then binary to a combination of dots(0) and exclamation marks (1)

![image](/posts/2020-08-23_habibamod-ctf-writeupcybertalents-ctf-2020/images/4.png#layoutTextWidth)


I wrote a really simple python script to reverse the process, but encountered issues using the binascii library since the binary string was too long. So I manually decoded the binary string.

![image](/posts/2020-08-23_habibamod-ctf-writeupcybertalents-ctf-2020/images/5.png#layoutTextWidth)


Decoding the binary string gives us the flag : )

![image](/posts/2020-08-23_habibamod-ctf-writeupcybertalents-ctf-2020/images/6.png#layoutTextWidth)


Happy hacking :D
