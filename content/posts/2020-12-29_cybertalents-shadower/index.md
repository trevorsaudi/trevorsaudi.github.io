---
title: "CyberTalents | Shadower"
author: "Trevor saudi"
date: 2020-12-29T20:45:22.417Z
lastmod: 2022-05-24T14:30:37+03:00

description: ""

subtitle: "In the machine section we have this medium level box to root. Diving right in!"

image: "/posts/2020-12-29_cybertalents-shadower/images/1.png" 
images:
 - "/posts/2020-12-29_cybertalents-shadower/images/1.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/2.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/3.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/4.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/5.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/6.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/7.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/8.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/9.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/10.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/11.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/12.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/13.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/14.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/15.png"
 - "/posts/2020-12-29_cybertalents-shadower/images/16.jpeg"


aliases:
    - "/cybertalents-shadower-fb601ce474dc"

tags:
- Privesc
- Machine
- CTF
---

In the machine section in Cybertalents, we have this medium level box to root. Diving right in!

### Enumeration

![image](/posts/2020-12-29_cybertalents-shadower/images/1.png#layoutTextWidth)
> Get The highest privilege on the machine and find the flag!``VPN Target IP: 172.24.209.176``Public Target IP: 18.193.123.37

Performed some nmap port scanning to get an overview of running ports and services

![image](/posts/2020-12-29_cybertalents-shadower/images/2.png#layoutTextWidth)


ssh and apache are running. So we can move on to view the web server. We get a default apache page, enumerating further we can reveal more interesting pages.

![image](/posts/2020-12-29_cybertalents-shadower/images/3.png#layoutTextWidth)


Bruteforcing directories using dirsearch we get some info .

![image](/posts/2020-12-29_cybertalents-shadower/images/4.png#layoutTextWidth)


Viewing the pages listed

![image](/posts/2020-12-29_cybertalents-shadower/images/5.png#layoutTextWidth)


Well, not much at first glance till we interact with the site. Tried viewing the source of the main page, about us and contact us. Contact us gives us an interesting file.

![image](/posts/2020-12-29_cybertalents-shadower/images/6.png#layoutTextWidth)


Ended up with this huuuuuuge chunk of nested base64 encoding

![image](/posts/2020-12-29_cybertalents-shadower/images/7.png#layoutTextWidth)


So, using python we can recursively decode that.

### Scripting

![image](/posts/2020-12-29_cybertalents-shadower/images/8.png#layoutTextWidth)


Okay, so this seems to be credentials. Judging from the open ports-ssh login credentials.

But we need a user for that. From the challenge name ‘Shadower’ I deduced that this hinted at the /etc/shadow file and possibly some LFI could be involved.

Back to the contact us page. We can fuzz the URL for some LFI and see if we get lucky.

![image](/posts/2020-12-29_cybertalents-shadower/images/9.png#layoutTextWidth)


Sweet! if you look closely, you can see our target user - john. Logging in with those credentials…

![image](/posts/2020-12-29_cybertalents-shadower/images/10.png#layoutTextWidth)


we’re in! Now for the sweet part of the challenge. Getting root access to the box.

### Privilege Escalation

Tried viewing what commands john could run as sudo

![image](/posts/2020-12-29_cybertalents-shadower/images/11.png#layoutTextWidth)


A bit unlucky.

Well, to quicken our priv esc , you can run linpeas on the box to enumerate on potential vectors. You can clone it from github [https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite)

Make the script executable by running _chmod +x_. Then run the script

![image](/posts/2020-12-29_cybertalents-shadower/images/12.png#layoutTextWidth)


From linpeas results, the /etc/passwd file is writable. Sweet! We can add our own root user and use that to get the flag.

Tried editing the /etc/passwd file directly. Worked, but I couldn’t assign a password to the user

![image](/posts/2020-12-29_cybertalents-shadower/images/13.png#layoutTextWidth)


So instead, opted to use OpenSSL. This article came in handy.

[Editing /etc/passwd File for Privilege Escalation](https://www.hackingarticles.in/editing-etc-passwd-file-for-privilege-escalation/)

![image](/posts/2020-12-29_cybertalents-shadower/images/14.png#layoutTextWidth)


Following the article, create your own salt for the password using openssl. Paste into /etc/passwd following this format

![image](/posts/2020-12-29_cybertalents-shadower/images/15.png#layoutTextWidth)


Nice! We get root. You can stabilize the shell using **_python3 -c “import pty; pty.spawn(‘/bin/bash’)”_**

cd into /root, get your flag in the “-” directory.

![image](/posts/2020-12-29_cybertalents-shadower/images/16.jpeg#layoutTextWidth)


Happy hacking :)
