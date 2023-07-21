---
title: "Malware development: Process Injection with C++"
author: "Trevor Saudi"
date: 2023-07-19
description: "Process Injection with C++"
image: "/posts/2023-03-25_red_team01/images/logo.png"
draft: true
tags:
- Red Teaming
- Malware Development

---
![image](/posts/2023-03-25_red_team02/images/logo.png)


## Introduction

- In the previous article we explored how we can write a simple stageless C++ dropper. In this article we build upon the capabilities of the dropper by implementing process injection. 
- Process injection is a well-known defense evasion technique that is used to hide code within the address space of another process. This allows an attacker to mask malicious code as a legitimate process in the system. It can also be used as a persistence technique by migrating to stable processes during post-exploitation.


## High-Level Overview

1. We begin by selecting a target process i.e notepad.exe. We can select any standard process in the system provided we have the necessary permissions
2. Open the process found and obtain a handle to it
3. Allocate memory within that process through the handle we have
4. Write our shellcode into the memory
5. Execute the injected code.

- The process is alike to what was covered in the previous article. The only addition is point 1 and 2.
- We will summarize the points into 2: Finding the target process we want to inject to and then injecting into it

## 1. Finding a Target Process

### [CreateToolhelp32Snapshot](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot)

- We use this function to create a snapshot of the specified processes in the system. This includes components and activities of the processes. 
- Since we will be enumerating the processes in the system to find our target, we will utilize the `TH32CS_SNAPPROCESS` parameter that allows us to grab all processes in the system. The second parameter is ignored when we use `TH32CS_SNAPPROCESS` so we place a `0` for that
- It returns a handle to the snapshot that's why we define a `HANDLE` variable for it


<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=777.6875&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=HANDLE%2520hProcSnap%2520%253D%2520CreateToolhelp32Snapshot%28TH32CS_SNAPPROCESS%252C%25200%29%253B%250A"
  style="width: 783px; height: 120px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe

### [PROCESSENTRY32 pe32](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/ns-tlhelp32-processentry32)

- This pre-defined windows data structure holds information about a single process when the snapshot was taken
- `pe32` is an instance of `PROCESSENTRY32`

<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=777.6875&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=pe32.dwSize%2520%253D%2520sizeof%28PROCESSENTRY32%29%253B%2520"
  style="width: 783px; height: 120px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe

- `pe32.dwSize` is a member of the PROCESSENTRY32 data structure. It represents the size of the structure in bytes. We grab the size of the structure using `sizeOf`

### [Process32First](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-process32first) [and]() [Process32Next](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-process32next)

- We will use these 2 APIs to enumerate through the running processes looking for a process with a specific name
- They both require the size of the structure to determine how much info to retrieve. 

<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=777.6875&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=int%2520pid%2520%253D%25200%253B%2520%2520%250Aif%2520%28%21Process32First%28hProcSnap%252C%2520%2526pe32%29%29%2520%257B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520CloseHandle%28hProcSnap%29%253B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520return%25200%253B%250A%257D%2520%2520%2520%2520%2520%2520%2520"
  style="width: 783px; height: 420px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">

<iframe

- In the above, we get the first process from the snapshot we took. `hProcSnap` is a handle to the snapshot of processes. `pe32` will be 

## Injecting into the target process


