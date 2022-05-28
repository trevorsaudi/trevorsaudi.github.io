---
title: "DownUnderCTF-Tim Tams(Misc)"
author: "Trevor saudi"
date: 2020-09-20T16:56:47.222Z
lastmod: 2022-05-24T14:30:12+03:00

description: ""

subtitle: "Misc challenges are usually random and require logic and lots of patience to solve. Surprisingly this one wasn’t too challenging."

image: "/posts/2020-09-20_downunderctftim-tamsmisc/images/1.png" 
images:
 - "/posts/2020-09-20_downunderctftim-tamsmisc/images/1.png"
 - "/posts/2020-09-20_downunderctftim-tamsmisc/images/2.png"


aliases:
    - "/downunderctf-tim-tams-misc-5d94158e97a8"

tags:
- Forensics
- QSSTV
- Audio
---

Misc challenges are usually random and require logic and lots of patience to solve. Surprisingly this one wasn’t too challenging.

The challenge description is as follows

![image](/posts/2020-09-20_downunderctftim-tamsmisc/images/1.png#layoutTextWidth)


We are given a really noisy wav audio file, I had no clue of solving this at first when my regular audio steganography tools failed. But my teammate came into play with a really good suggestion. **QSSTV**!

[https://storage.googleapis.com/files.duc.tf/uploads/Clive.wav](https://storage.googleapis.com/files.duc.tf/uploads/Clive.wav)

**QSSTV** is a utility for dealing with slow scan television signals. From the challenge description, we can pick out a hint “When I eat too many Tim Tams, I get rather slow!”.

I used the following commands to setup qsstv on linux
``sudo apt-get install pavucontrol  
sudo apt-get install qsstv``

We need the pavucontrol utility to be able to open audio files.

Type qsstv on the terminal to open the program and select the audio file you’re going to work with

![image](/posts/2020-09-20_downunderctftim-tamsmisc/images/2.png#layoutTextWidth)


qsstv maps the wav audio into an image and we can see at the top left what appears to be an encoded flag.

QHGPS{UHZOYR_Z3Z3_1BEQ}

This is ROT13, we decode the flag to: DUTCF{HUMBLE_M3M3_1ORD}

Happy hacking :)
