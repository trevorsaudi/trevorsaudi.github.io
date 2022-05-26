---
title: "Vulncon CTF — maze"
author: "Trevor saudi"
date: 2020-12-20T17:57:47.794Z
lastmod: 2022-05-24T14:30:32+03:00

description: ""

subtitle: "Took part in Vulncon CTF this weekend where our team settled for 34th place out of 442 teams. Diving into the first web challenge…"

image: "/posts/2020-12-20_vulncon-ctfmaze/images/1.png" 
images:
 - "/posts/2020-12-20_vulncon-ctfmaze/images/1.png"
 - "/posts/2020-12-20_vulncon-ctfmaze/images/2.png"
 - "/posts/2020-12-20_vulncon-ctfmaze/images/3.png"
 - "/posts/2020-12-20_vulncon-ctfmaze/images/4.png"
 - "/posts/2020-12-20_vulncon-ctfmaze/images/5.png"
 - "/posts/2020-12-20_vulncon-ctfmaze/images/6.png"
 - "/posts/2020-12-20_vulncon-ctfmaze/images/7.png"
 - "/posts/2020-12-20_vulncon-ctfmaze/images/8.png"
 - "/posts/2020-12-20_vulncon-ctfmaze/images/9.png"
 - "/posts/2020-12-20_vulncon-ctfmaze/images/10.png"
 - "/posts/2020-12-20_vulncon-ctfmaze/images/11.png"


aliases:
    - "/vulncon-ctf-maze-7a47b10a0b2c"

---

Took part in Vulncon CTF this weekend where our team settled for 34th place out of 442 teams. Diving into the first web challenge -maze(easy category).

![image](/posts/2020-12-20_vulncon-ctfmaze/images/1.png#layoutTextWidth)


From the hint we are told we can use gobuster. So I did some directory bruteforcing with the tool of my choice -dirsearch :)

![image](/posts/2020-12-20_vulncon-ctfmaze/images/2.png#layoutTextWidth)


Our tool picks up an interesting directory /projects/

![image](/posts/2020-12-20_vulncon-ctfmaze/images/3.png#layoutTextWidth)


27 is my lucky number… a hint maybe? Viewing the source of the page, we get more interesting information

![image](/posts/2020-12-20_vulncon-ctfmaze/images/4.png#layoutTextWidth)


Accessing the image that has been commented out gives us this QR code.

![image](/posts/2020-12-20_vulncon-ctfmaze/images/5.png#layoutTextWidth)


Scanning this gives the word. “hello”. Since the image was named “image-0.png” I tried viewing “image-1.png” and got another image. So this means we have multiple images which gives a string after being scanned. From the /projects/ directory the hint given tells us that we have 27 images in total.

I used wget to recursively download all images

![image](/posts/2020-12-20_vulncon-ctfmaze/images/6.png#layoutTextWidth)


So now, we can write a small python script to decode all the QR codes.

![image](/posts/2020-12-20_vulncon-ctfmaze/images/7.png#layoutTextWidth)


This gives us the following sentence

![image](/posts/2020-12-20_vulncon-ctfmaze/images/8.png#layoutTextWidth)


Performed more analysis on image 13

![image](/posts/2020-12-20_vulncon-ctfmaze/images/9.png#layoutTextWidth)


We get an interesting string at the Creator tag. Decoding with basecrack we get a rotated string

![image](/posts/2020-12-20_vulncon-ctfmaze/images/10.png#layoutTextWidth)


Decoded with ROT13 to get the flag.

![image](/posts/2020-12-20_vulncon-ctfmaze/images/11.png#layoutTextWidth)
