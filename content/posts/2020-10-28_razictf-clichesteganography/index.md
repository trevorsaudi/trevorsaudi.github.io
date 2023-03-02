---
title: "RaziCTF Cliche-Steganography"
author: "Trevor saudi"
date: 2020-10-28T10:15:04.517Z
lastmod: 2022-05-24T14:30:20+03:00

description: ""

subtitle: "Another audio steganography challenge from RaziCTF. As the name suggest this is a  cliche challenge in CTFs :/"

image: "/posts/2020-10-28_razictf-clichesteganography/images/1.png" 
images:
 - "/posts/2020-10-28_razictf-clichesteganography/images/1.png"
 - "/posts/2020-10-28_razictf-clichesteganography/images/2.png"


aliases:
    - "/razictf-cliche-steganography-8b9de1bc8f25"

tags:
- QSSTV
- Audio
- CTF
---
Another audio steganography challenge from RaziCTF.

Proceeding to solve

![image](/posts/2020-10-28_razictf-clichesteganography/images/1.png#layoutTextWidth)


**Challenge description**

_I told my friend SCOTTIE that this challenge is cliché and he said I’m not the only 1 who thinks that way._

The challenge is based on Slow-scan television (SSTV) which is a method for picture transmission used by amateur radio operators to transmit and receive images. The highlighted SCOTTIE from the challenge description hints directly at the transmission mode frequently used in SSTV.

We can use a tool called QSSTV to decode the piece of audio wav file from the challenge. A detailed installation description and an example on how to decode can be found [here](https://ourcodeworld.com/articles/read/956/how-to-convert-decode-a-slow-scan-television-transmissions-sstv-audio-file-to-images-using-qsstv-in-ubuntu-18-04)

From the screenshot below, I pressed the play button to start recording on QSSTV then played the wav file from the challenge. Slowly, it starts to reveal the flag.

![image](/posts/2020-10-28_razictf-clichesteganography/images/2.png#layoutTextWidth)


RaziCTF{h0w_y0u_d0in}

Happy hacking :)
