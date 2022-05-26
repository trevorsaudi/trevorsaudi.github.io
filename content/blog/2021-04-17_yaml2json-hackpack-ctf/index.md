---
title: "Yaml-2-Json Hackpack CTF"
author: "Trevor saudi"
date: 2021-04-17T18:46:32.088Z
lastmod: 2022-05-24T14:31:54+03:00

description: ""

subtitle: "Exploiting a deserialize vunlerability in pyyaml"

image: "/posts/2021-04-17_yaml2json-hackpack-ctf/images/1.png" 
images:
 - "/posts/2021-04-17_yaml2json-hackpack-ctf/images/1.png"
 - "/posts/2021-04-17_yaml2json-hackpack-ctf/images/2.png"
 - "/posts/2021-04-17_yaml2json-hackpack-ctf/images/3.png"
 - "/posts/2021-04-17_yaml2json-hackpack-ctf/images/4.png"


aliases:
    - "/yaml-2-json-hackpack-ctf-7de28ef0ecff"

---

#### Exploiting a deserialize vunlerability in pyyaml

Hackpack has recently concluded and we placed 47th out of 447 teams. In this short writeup we look at Yaml-2-Json in the web category

![image](/posts/2021-04-17_yaml2json-hackpack-ctf/images/1.png#layoutTextWidth)


In this challenge we exploit a code execution vulnerability in pyYaml- a yaml parser and emitter for python. The server is using [pyYAML](https://github.com/yaml/pyyaml/tree/5.3.1) and Flask.

We get a simple web page with an option to parse yaml to json. I thought of using python payloads to get some code execution but they failed at first.

![image](/posts/2021-04-17_yaml2json-hackpack-ctf/images/2.png#layoutTextWidth)


The message at the bottom hinting that I was not on a premium account prompted me to investigate the cookies.

Interestingly enough we can modify the premium value to true so we get premium privileges on the service

![image](/posts/2021-04-17_yaml2json-hackpack-ctf/images/3.png#layoutTextWidth)


Sweet, so let’s go for RCE and read our flag from the server

I used the following payload at first but it fails since subprocess will only accept single commands like `whoami, id`
`user_input: !!python/object/apply:subprocess.check_output [&#39;cat /tmp/flag.txt&#39;]`

My teammate [Koimet](https://twitter.com/k0imet_) helped me refine my payload to the following which gives us the flag
`user_input: !!python/object/apply:subprocess.check_output  
       args: [ cat /tmp/flag.txt ]  
       kwds: { shell: true }`
![image](/posts/2021-04-17_yaml2json-hackpack-ctf/images/4.png#layoutTextWidth)
