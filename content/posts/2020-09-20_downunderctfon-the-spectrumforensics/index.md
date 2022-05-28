---
title: "DownUnderCTF-On the Spectrum(Forensics)"
author: "Trevor saudi"
date: 2020-09-20T16:36:30.184Z
lastmod: 2022-05-24T14:30:10+03:00

description: ""

subtitle: "Recently, I’ve been getting hooked with forensics challenges, this being the second solve I made for the team."

image: "/posts/2020-09-20_downunderctfon-the-spectrumforensics/images/1.png" 
images:
 - "/posts/2020-09-20_downunderctfon-the-spectrumforensics/images/1.png"
 - "/posts/2020-09-20_downunderctfon-the-spectrumforensics/images/2.png"


aliases:
    - "/downunderctf-on-the-spectrum-forensics-fa5a9ea1e28e"

tags:
- Forensics
- Audio

---

Recently, I’ve been getting hooked with forensics challenges, this being the second solve I made for the team.

The challenge description is as follows

“ My friend has been sending me lots of WAV files, I think he is trying to communicate with me, what is the message he sent?”

![image](/posts/2020-09-20_downunderctfon-the-spectrumforensics/images/1.png#layoutTextWidth)


The challenge description was already a hint and I pinpointed this to spectrum steganography. Audacity is a popular tool used to analyze waveforms and spectograms

**the audio file**

[https://play.duc.tf/files/cd754e8ca5f4e863149943710549555f/message_1.wav?token=eyJ1c2VyX2lkIjo3NzQsInRlYW1faWQiOjE0NiwiZmlsZV9pZCI6ODV9.X2eJ4g.K-7io8oej81HFrnGLYwMaIrGNMs](https://play.duc.tf/files/cd754e8ca5f4e863149943710549555f/message_1.wav?token=eyJ1c2VyX2lkIjo3NzQsInRlYW1faWQiOjE0NiwiZmlsZV9pZCI6ODV9.X2eJ4g.K-7io8oej81HFrnGLYwMaIrGNMs)

**audacity link to download**

[https://www.audacityteam.org/download/](https://www.audacityteam.org/download/)

Proceeding to open the .wav file with audacity and viewing it as a spectorgram, we get the flag!

![image](/posts/2020-09-20_downunderctfon-the-spectrumforensics/images/2.png#layoutTextWidth)
DUCTF{m4by3_n0t_s0_h1dd3n}



Happy hacking :)
