---
title: "SSRF to gaining RCE —( rootme ssrf box)"
author: "Trevor saudi"
date: 2020-11-17T12:34:18.050Z
lastmod: 2022-05-24T14:30:25+03:00

description: ""

subtitle: "Write-up for an SSRF box on the rootme platform."

image: "/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/1.png" 
images:
 - "/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/1.png"
 - "/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/2.png"
 - "/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/3.png"
 - "/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/4.png"
 - "/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/5.png"
 - "/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/6.png"
 - "/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/7.png"
 - "/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/8.png"


aliases:
    - "/ssrf-to-gaining-rce-rootme-ssrf-box-31b7d0e5ad08"

---

Write-up for an [SSRF box] (https://www.root-me.org/?lang=en&amp;page=ctf_alltheday&amp;id_salle=4)on the rootme platform.

![image](/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/1.png#layoutTextWidth)


So from the description, our objective is to get root and find the flag in /root.

### Enumeration

Moving on to the challenge, we are presented with an input box where you can place a url and the site creates a link that redirects you to it.

![image](/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/2.png#layoutTextWidth)

![image](/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/3.png#layoutTextWidth)


To first test for SSRF, you can fuzz the input to see if you can read system files.

![image](/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/4.png#layoutTextWidth)


Nice! We can move on to detect open services running in the internal network of the web server. Intercept the request using burpsuite Intruder and bruteforce for open ports

![image](/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/5.png#layoutTextWidth)


Port 6379 (running the Redis service) timed out on the intruder attack. This means that the port was open and redis was running.

I proceed to port forward localhost on port 1234 using ngrok to expose my IP to the public .

![image](/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/6.png#layoutTextWidth)

### Exploitation

Then used gopher to generate a payload that would get a reverse shell back on netcat. We get RCE !

![image](/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/7.png#layoutTextWidth)


Navigate to /root and get your flag, and /passwd for the validation flag.

![image](/posts/2020-11-17_ssrf-to-gaining-rce-rootme-ssrf-box/images/8.png#layoutTextWidth)


Happy hacking :)
