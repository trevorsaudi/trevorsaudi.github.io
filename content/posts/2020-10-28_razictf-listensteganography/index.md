---
title: "RaziCTF Listen-Steganography"
author: "Trevor saudi"
date: 2020-10-28T09:56:35.018Z
lastmod: 2022-05-24T14:30:23+03:00

description: ""

subtitle: "Beginner-Intermediate CTF that took place on Oct 28. We came 15th :)."

image: "/posts/2020-10-28_razictf-listensteganography/images/1.png" 
images:
 - "/posts/2020-10-28_razictf-listensteganography/images/1.png"
 - "/posts/2020-10-28_razictf-listensteganography/images/2.png"
 - "/posts/2020-10-28_razictf-listensteganography/images/3.png"
 - "/posts/2020-10-28_razictf-listensteganography/images/4.png"


aliases:
    - "/razictf-listen-steganography-6f857c3e0f9b"

tags:
- Morse
- CTF
---

Beginner-Intermediate CTF that took place on Oct 28. We came 15th :).

This is the writeup for Listen, an audio steganogrpahy

![image](/posts/2020-10-28_razictf-listensteganography/images/1.png#layoutTextWidth)


**Challenge description**

_Listen carefully, what do you hear? Look closely, what do you see? To Submit the flag, put it in UPPERCASE and in this format RaziCTF{}. like this: RaziCTF{FLAG}_

We are given a wav audio file. Most audio CTFs are similar so I proceeded to open the wav file with Audacity.

![image](/posts/2020-10-28_razictf-listensteganography/images/2.png#layoutTextWidth)


I like to open my audio files as spectograms for better visibility. When I played the audio I could make out 2 distinct beeps and immediately thought of morse code. In audacity, the 2 distinct beeps are separated as shown above

The short lines represent dots (.) and the longer ones represent dashes (-) in morse code. I proceeded to translate the first wave form into a series of dots and dashes as shown below

![image](/posts/2020-10-28_razictf-listensteganography/images/3.png#layoutTextWidth)
`- .... .  .-. . .- .-..   ..-. .-.. .- --.  .. ...   ... .---- -- .--. .-.. ...-- -- ----- .-. ... ... --`

Decoding as morse code we get the flag :)

![image](/posts/2020-10-28_razictf-listensteganography/images/4.png#layoutTextWidth)


THEREALFLAGISS1MPL3M0RSSM

Submitted the flag as S1MPL3M0RSSM

Happy hacking :)
