---
title: "widthless writeup -CSAW CTF Quals 2020"
author: "Trevor saudi"
date: 2020-09-13T16:47:46.811Z
lastmod: 2022-05-24T14:30:03+03:00

description: ""

subtitle: "Diving right into the first web category challenge — widthless."

image: "/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/1.png" 
images:
 - "/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/1.png"
 - "/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/2.png"
 - "/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/3.png"
 - "/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/4.png"
 - "/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/5.png"
 - "/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/6.png"
 - "/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/7.png"
 - "/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/8.png"
 - "/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/9.png"
 - "/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/10.png"
 - "/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/11.png"


aliases:
    - "/widthless-writeup-csaw-ctf-quals-2020-a007b3ddadc3"

tags:
- ZWSP
- Web


---

Diving right into the first web category challenge — widthless.

![image](/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/1.png#layoutTextWidth)


The initial instructions didn’t seem to give us much of a hint :

Welcome to web! Let’s start off with something kinda funky :)

http[://web.chal.csaw.io:5018](http://web.chal.csaw.io:5018/)

I interacted with the website for a few minutes by trying to figure out what the challenge could be about.

![image](/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/2.png#layoutTextWidth)


Tried inputting into the form and it says it couldn’t add me to the newsletter…

After viewing the source, we get the first clue of the challenge

![image](/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/3.png#layoutTextWidth)


ZWSP is fun

### Step 1: Some Reconnaisance

I wanted to gather enough data to figure out what zwsp was all about since I had no clue at first. Googling zwsp, I found out that zwsp (zero width spacing) is a character used in unicode for invisible word separation. More googling reveals that zwsp can be used to hide pieces of information in plain-sight!.

### Step 2: Detecting ZWSP

Stumbled upon a tool called diffchecker that could highlight all the characters that are hidden in a piece of text.

![image](/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/4.png#layoutTextWidth)


Pasting the entire html source code, you can see presence of hidden text inside the document. So how do I uncover it??

### Step 3: Decoding ZWSP

Since I know the characters do exist, I tried finding scripts that could help in revealing the hidden characters and voila, I came across a steganography library written in javascript from github

![image](/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/5.png#layoutTextWidth)


Include the script using the require function and proceed to decode the section containing the zwsp hidden string. It yields a base64 encoded string YWxtMHN0XzJfM3o=

Decoding this gives alm0st_2_3z as the output. Flag maybe?? No, challenge still goes on !

![image](/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/6.png#layoutTextWidth)


Pasting in the decoded string gives this long string.

/ahsdiufghawuflkaekdhjfaldshjfvbalerhjwfvblasdnjfbldf/<pwd>

I spent quite some time trying to figure out what it meant, at first, I thought it was the password to a hidden input field, and tried posting the data to the website but it failed.

Finally, I figured that the string enclosed in backslashes is actually a directory and the pwd is where the decoded string goes.

![image](/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/7.png#layoutTextWidth)


Putting that info in the URL takes us to another page. More ZWSP maybe?

### Step 4: Solving the challenge :D

Viewing the source and repeating the process, but this time actually decoding the whole html source since the zwsp characters were hidden everywhere

![image](/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/8.png#layoutTextWidth)


The following string is yielded from decoding the zwsp — 755f756e6831645f6d33

Decoding from hex to ascii gives —

u_unh1d_m3

![image](/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/9.png#layoutTextWidth)


This time we get another directory with a similar pattern to the last but appending the first and second decoded strings

![image](/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/10.png#layoutTextWidth)


We get the flag :) !!!

![image](/posts/2020-09-13_widthless-writeup-csaw-ctf-quals-2020/images/11.png#layoutTextWidth)


Happy hacking :D
