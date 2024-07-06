---
title: "GOAD Part 1: AD Recon, NTLM relay, ASREPRoasting & Kerberoasting"
author: "Trevor Saudi"
date: 2024-06-11
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

![image](/posts/2024-06-11_red_team06/images/logo.png)



## Introduction

- Game of Active Directory is a fully functional AD lab environment, misconfigured with several AD bug types designed to help understand various AD security concepts. I recently deployed it on a Windows host and have been playing with it.
- In this n-part series, we will explore the various AD misconfigurations and how we can abuse them while maintaining our OPSEC. Part 1 will focus on how we go about with enumeration of the environment to map out the various open services and ports and discover of users in the network. The recon process is the most crucial part as it makes the rest of our attack paths clearer and straightforward.
- We will proceed with looking at some misconfigurations we can exploit when we don't have credentials in an AD environment such as NTLM relay and ASREPRoasting then finish of with kerberoasting. 

## Network Diagram

<div style="width: 930px;">
        <img src="/posts/2024-06-11_red_team06/images/GOAD_schema.png" alt="no image" />
</div>

## Reconnaissance

- From our network diagram, we are dealing with 5 different machines across 3 domains in the network. 
1. `north.sevenkingdoms.local`
    - DC01 (kingslanding)
2. `sevenkingdoms.local`
    - DC02 (winterfell)
    - SRV02 (castleback)
3. `essos.local`
    - DC02 (mereen)
    - SRV03 (braavos)
- The creators of GOAD - Orange Cyberdefense - have also come up with this mindmap that structures our AD pentesting approach. We will frequently refer to this resource throughout these writeups 

### Hosts file setup

- We can begin by mapping out all the machines in our hosts file. Using the IP information and domains given to us, we can then find the `domain controllers` in the network.

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

## Domain User enumeration

- We have several options for this. We can use `crackmapexec or enum4linux` to check for this information.

<div >
        <img src="/posts/2024-06-21_red_team07/images/find-user-list.png" alt="no image" />
</div>

```powershell
crackmapexec smb ips.txt --users 
```

<div >
        <img src="/posts/2024-06-21_red_team07/images/users-enum.png" alt="no image" />
</div>

- We get some domain users and credentials in a user's description.


{{< alert "circle-info" >}}
samwell.tarly : Heartsbane 
{{< /alert >}}

- Recon is a recursive process. Upon getting valid credentials, you should rerun your user enumeration commands with credentials to see whether you get more information

<div>
        <img src="/posts/2024-06-21_red_team07/images/users-enum2.png" alt="no image" />
</div>

- We get more users on the domain

## Domain Group enumeration

- I ran crackmapexec without creds but we don't get an output on any domain

<div>
        <img src="/posts/2024-06-21_red_team07/images/crackmapexec-groups.png" alt="no image" />
</div>

- We can run either `crackmapexec` or `enum4linux` with  samwell's creds and extract some domain group information. We are only able to retrieve information on the `north.sevenkingdoms.local` domain.

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

## Poisoning

<div>
        <img src="/posts/2024-06-21_red_team07/images/poisoning.png" alt="no image" />
</div>

- LLMNR (Link-Local Multicast Resolution), is a protocol in Windows used to resolve NetBIOS names of computers on the same subnet when DNS resolution fails. When attempting to locate unknown resources in a network, LLMNR multicasts requests across a network to attempt to find unknown routes e.g shares.
- Attackers can trick devices to sending sensitive information by pretending to be the resource that another computer is trying to locate. 

### 1. We listen in the interface we're connected in the subnet

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

### 2. Crack with hashcat

```bash
hashcat -m 5600 -a 0 ntlm.txt /usr/share/wordlists/rockyou.txt.gz 
```

- We get `robb.stark's` hash. 
 
{{< alert "circle-info" >}}
robb.stark : sexywolfy
{{< /alert >}}

- `edd's` hash could not be cracked but, we can relay the hashes to machines where `SMB signing` is disabled. SMB signing prevents relay attacks by appending a digital signature on packets for integrity checks.


## Password spraying

- Now that we have some information to work with, we can start out with some simple attacks such as password spra
