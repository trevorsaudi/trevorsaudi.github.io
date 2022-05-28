---
title: "RCE on Unauthenticated Redis server"
author: "Trevor saudi"
date: 2021-03-23T18:02:12.222Z
lastmod: 2022-05-24T14:31:21+03:00

description: ""

subtitle: "In this brief walk-through , we will be hacking a vulnerable database server by showcasing the res room in Tryhackme."

image: "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/1.png" 
images:
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/1.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/2.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/3.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/4.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/5.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/6.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/7.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/8.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/9.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/10.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/11.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/12.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/13.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/14.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/15.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/16.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/17.png"
 - "/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/18.png"


aliases:
    - "/rce-on-unauthenticated-redis-server-11d3494ded5f"

---

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/1.png#layoutTextWidth)


> In this brief walk-through , we will be hacking a vulnerable database server by showcasing the [res room](https://tryhackme.com/room/res) in Tryhackme.

### Enumeration

As always, spin up our machine instance and begin some enumeration. For speed and more accuracy, I perform a port scan using rustscan( an incredibly fast port scanning tool) and then do a default scripts and vuln scan using nmap as shown below

```bash
rustscan -a <IP>
nmap -sC -sV --scripts=vuln <IP> -p 80,6379
```
![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/2.png#layoutTextWidth)


We get port 80 and 6379. Nmap does not gives us much info.

We have an exposed redis instance that we will look into and a web server running on port 80. Accessing this via browser we get a default apache page. Nothing interesing.

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/3.png#layoutTextWidth)


We can try bruteforcing for any important directories that may be worth looking into. Here I fired up dirsearch, another blazingly fast directory scanner. In other scenarios it’s good to also maximize accuracy by using additional tools like gobuster and dirbuster that may pick up interesting directories.

```bash 
python3 dirsearch.py -u <IP> -e "*"
```


We don’t get anything interesting.

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/4.png#layoutTextWidth)


### Exploitation

[6379 - Pentesting Redis](https://book.hacktricks.xyz/pentesting/6379-pentesting-redis#redis-rce)


The article above came in handy in gaining RCE. I used redis-cli to interact with the instance. You can install redis-cli as shown below
```bash     
sudo apt-get install redis-tools
```


We have unauthenticated access to the database instance.

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/5.png#layoutTextWidth)


According to the article, for us to achieve RCE on the server, we need to find the path to the web site folder. Remember our default apache page? Well that comes in handy here

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/6.png#layoutTextWidth)


The document root is highlighted `/var/www/html`. Now we change our directory to that folder and try uploading some files.

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/7.png#layoutTextWidth)


As a POC, we can try displaying phpinfo as shown above and accessing it on the browser.

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/8.png#layoutTextWidth)


Sweet :) This means we have remote code execution on this server. We can therefore proceed to getting a shell, escalating our privileges and gaining root access.

### Remote Code Execution

To gain RCE. Create another file and append the following code to be able to execute code on a parameter.

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/9.png#layoutTextWidth)


We get RCE :)

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/10.png#layoutTextWidth)


Nice. Now lets get a reverse shell. From [payloadallthethings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#python) we can get our python revshell, modify it and set up a netcat listener

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/11.png#layoutTextWidth)


Grab your shell :)

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/12.png#layoutTextWidth)


Stabilize the shell by backgrounding it using `ctrl+z` and then `stty raw -echo;fg` to resume.

Navigate directories to get your user.txt flag.

### Privilege escalation

My approach for privesc before uploading linpeas or any enumerator is to first check for sudo rights the user has using `sudo -l,` then check for SUID bits set

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/13.png#layoutTextWidth)


xxd has suid bit set. And it owned by the root user. Head over to [GTFObins](https://gtfobins.github.io/gtfobins/xxd/#sudo) and check through xxd.

Interesting, in this exploit, we can read sensitive info using the xxd binary like /etc/shadow file.
```bash
LFILE=file_to_read
xxd "$LFILE" | xxd -r
```
![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/14.png#layoutTextWidth)


I read this file and grabbed the hash of the vianka user, since it was part of this challenge to get the user’s password

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/15.png#layoutTextWidth)


We can crack their password using john.

```bash
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```
![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/16.png#layoutTextWidth)


We get the password as `beautiful1` We can do some horizontal privilege escalation to and execute commands as vianka.

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/17.png#layoutTextWidth)


Vianka has all sudo permission on the machine as shown by the command `sudo -l`

For the root flag

![image](/posts/2021-03-23_rce-on-unauthenticated-redis-server/images/18.png#layoutTextWidth)


If you’ve made it this far, like , share and follow for more articles

Happy hacking :)
