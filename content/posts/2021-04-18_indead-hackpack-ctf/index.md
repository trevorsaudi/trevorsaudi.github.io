---
title: "Indead Hackpack CTF"
author: "Trevor saudi"
date: 2021-04-18T07:43:48.016Z
lastmod: 2022-05-24T14:31:56+03:00

description: ""

subtitle: "getimagesize() File upload vulnerability"

image: "/posts/2021-04-18_indead-hackpack-ctf/images/1.png" 
images:
 - "/posts/2021-04-18_indead-hackpack-ctf/images/1.png"
 - "/posts/2021-04-18_indead-hackpack-ctf/images/2.png"
 - "/posts/2021-04-18_indead-hackpack-ctf/images/3.png"
 - "/posts/2021-04-18_indead-hackpack-ctf/images/4.png"
 - "/posts/2021-04-18_indead-hackpack-ctf/images/5.png"
 - "/posts/2021-04-18_indead-hackpack-ctf/images/6.png"
 - "/posts/2021-04-18_indead-hackpack-ctf/images/7.png"
 - "/posts/2021-04-18_indead-hackpack-ctf/images/8.png"


aliases:
    - "/indead-hackpack-ctf-1b3878120da5"


tags:
- PHP
---

## getimagesize() File upload vulnerability

In this write-up we go through Indead in the web category

### Enumeration 

We are given a web page with an upload functionality.

![image](/posts/2021-04-18_indead-hackpack-ctf/images/1.png#layoutTextWidth)


I immediately went for a file upload vulnerability and tried uploading a simple php web shell.

![image](/posts/2021-04-18_indead-hackpack-ctf/images/2.png#layoutTextWidth)


The file gets rejected even after trying some few file extension bypasses. I tried looking for more clues so I bruteforced the site and got something interesting

![image](/posts/2021-04-18_indead-hackpack-ctf/images/3.png#layoutTextWidth)


Tried robots.txt

![image](/posts/2021-04-18_indead-hackpack-ctf/images/4.png#layoutTextWidth)


Interesting, file extensions with phps have been disabled.
> **PHPS** is a **PHP** Source Code **file** that contains Hypertext Preprocessor code. They are often used as web page **files** that usually generate HTML from a **PHP** engine running on a web server

So I tried using index.phps instead of index.php and got some source code

![image](/posts/2021-04-18_indead-hackpack-ctf/images/5.png#layoutTextWidth)


Let us access core.php as core.phps

![image](/posts/2021-04-18_indead-hackpack-ctf/images/6.png#layoutTextWidth)


Sweet :) We get the source code for the challenge. The upload directory is `very_long_directory_path` which we need to take note of for later.

getimagesize() is used to perform the checks on files being uploaded to the server. This function checks the header of a file and determines whether it is an image or not. We can bypass this as follows

![image](/posts/2021-04-18_indead-hackpack-ctf/images/7.png#layoutTextWidth)

### Exploitation
The header bypasses getimagesize() and we upload our webshell to `very_long_directory_path`

We can access the flag via <url>/`very_long_directory_path/exploit.php?cmd=cat /var/www/flag.txt`

![image](/posts/2021-04-18_indead-hackpack-ctf/images/8.png#layoutTextWidth)
