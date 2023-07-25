---
title: "Malware development: Process Injection with C++"
author: "Trevor Saudi"
date: 2023-07-21
description: "Process Injection with C++"
image: "/posts/2023-07-21_red_team03/images/logo.png"
draft: false
tags:
- Red Teaming
- Malware Development


---
![image](/posts/2023-07-21_red_team03/images/logo.png)

<style>



@import url('https://cdn.rawgit.com/lonekorean/gist-syntax-themes/d49b91b3/stylesheets/one-dark.css');

@import url('https://fonts.googleapis.com/css?family=Open+Sans');


   
  *, ::before, ::after {
    border-style: none;

  }

  body {
  margin: 20px;
  font: 16px 'Open Sans', sans-serif;
}



</style>

## Introduction

- In the previous article we explored how we can write a simple stageless C++ dropper. In this article we build upon the capabilities of the dropper by implementing process injection. 
- Process injection is a well-known defense evasion technique that is used to hide code within the address space of another process. This allows an attacker to mask malicious code as a legitimate process in the system. It can also be used as a persistence technique by migrating to stable processes during post-exploitation.


## High-Level Overview

1. We begin by selecting a target process i.e notepad.exe. We can select any standard process in the system provided we have the necessary permissions
2. Open the process found and obtain a handle to it
3. Allocate memory within that process through the handle we have
4. Write our shellcode into the memory
5. Execute the injected code.

- We will summarize the points into 2: Finding the target process we want to inject to and then injecting into it.
- The final project file can be located here for quick reference: [https://github.com/trevorsaudi/Process-Injection-cpp](https://github.com/trevorsaudi/Process-Injection-cpp)

## 1. Finding a Target Process

### [CreateToolhelp32Snapshot](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot)

- We use this function to create a snapshot of the specified processes in the system. This includes components and activities of the processes. 
- Since we will be enumerating the processes in the system to find our target, we will utilize the `TH32CS_SNAPPROCESS` parameter that allows us to grab all processes in the system. The second parameter is ignored when we use `TH32CS_SNAPPROCESS` so we place a `0` for that
- It returns a handle to the snapshot that's why we define a `HANDLE` variable for it



<script src="https://gist.github.com/trevorsaudi/1c38f1bd35d33698fad7e31cea3be718.js"></script>

<!-- <iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=763.6875&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=HANDLE%2520hProcSnap%2520%253D%2520CreateToolhelp32Snapshot%28TH32CS_SNAPPROCESS%252C%25200%29%253B%250A"
  style="width: 773px; height: 120px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe> -->



### [PROCESSENTRY32 pe32](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/ns-tlhelp32-processentry32)

- This pre-defined windows data structure holds information about a single process when the snapshot was taken
- `pe32` is an instance of `PROCESSENTRY32`

<!-- <iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=763.6875&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=pe32.dwSize%2520%253D%2520sizeof%28PROCESSENTRY32%29%253B%2520"
  style="width: 773px; height: 120px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe> -->

<script src="https://gist.github.com/trevorsaudi/bbf0cdeaf030cc93445c8cc88558e1e1.js"></script>

- `pe32.dwSize` is a member of the PROCESSENTRY32 data structure. It represents the size of the structure in bytes. We grab the size of the structure using `sizeOf`

### [Process32First](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-process32first) [and]() [Process32Next](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-process32next)

- We will use these 2 APIs to enumerate through the running processes looking for a process with a specific name
- They both require the size of the structure to determine how much info to retrieve. 

<!-- <iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=763.6875&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=int%2520pid%2520%253D%25200%253B%2520%2520%250Aif%2520%28%21Process32First%28hProcSnap%252C%2520%2526pe32%29%29%2520%257B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520CloseHandle%28hProcSnap%29%253B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520return%25200%253B%250A%257D%2520%2520%2520%2520%2520%2520%2520" 
  style="width: 773px; height: 170px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">

</iframe> -->

<script src="https://gist.github.com/trevorsaudi/acad1be8b3094dd5bac2627207e855d9.js"></script>

- In line  of the code block above, we get the first process from the snapshot we took, where, `hProcSnap` is a handle to the snapshot of processes and `pe32` is a `PROCESSENTRY32` structure which will get filled with information about a process.
- If the block of code fails to get a process for some reason, we close the handle.

- We now proceed to find the target process below
<!-- <iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=bw&l=text%2Fx-c%2B%2Bsrc&width=766.125&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=while%2520%28Process32Next%28hProcSnap%252C%2520%2526pe32%29%29%2520%257B%250A%2520%2520%2520%2520if%2520%28lstrcmpiA%28procname%252C%2520pe32.szExeFile%29%2520%253D%253D%25200%29%2520%257B%250A%2520%2520%2520%2520%2520%2520%2520%2520pid%2520%253D%2520pe32.th32ProcessID%253B%250A%2520%2520%2520%2520%2520%2520%2520%2520break%253B%250A%2520%2520%2520%2520%257D%250A%257D" 
  style="width: 773px; height: 190px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">

</iframe> -->

<script src="https://gist.github.com/trevorsaudi/1093e839271ea82386152dbf11ffb38e.js"></script>

- We use `Process32Next`, to get the information about the next process. This allows us to cycle through the snapshot. We then compare the name of the current process which is stored in `pe32.szExeFile` with what we are looking for `procname`.

## 2. Injecting into the target process

- This process involves us allocating memory to our target process, writing to it and executing the shellcode from the process calling it.

### [VirtualAllocEx](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualallocex)

- We use this to allocate memory in the `target` process.

<!-- <iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=bw&l=text%2Fx-c%2B%2Bsrc&width=766.125&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=LPVOID%2520pRemoteCode%2520%253D%2520VirtualAllocEx%28hProc%252C%2520NULL%252C%2520payload_len%252C%2520MEM_COMMIT%252C%2520PAGE_EXECUTE_READ%29%253B" 
  style="width: 773px; height: 110px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">

</iframe> -->

<script src="https://gist.github.com/trevorsaudi/a314715df56fd3df8d396fef52985680.js"></script>


- The difference between the VirtualAllocEx and VirtualAlloc is that VirtualAlloc allocates memory within the address space of the `calling process`, while VirtualAllocEx lets you `specify a target process` to allocate memory.


### [WriteProcessMemory](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-writeprocessmemory)

- We use this API to write into the memory in a specified address. We will utilize this to write our shellcode into the memory region we reserved in the target process.


<!-- <iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=bw&l=text%2Fx-c%2B%2Bsrc&width=768.65625&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=%2520WriteProcessMemory%28hProc%252C%2520pRemoteCode%252C%2520%28PVOID%29payload%252C%2520%28SIZE_T%29payload_len%252C%2520%28SIZE_T%2520*%29NULL%29%253B"
  style="width: 773px; height: 110px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">

</iframe> -->

<script src="https://gist.github.com/trevorsaudi/7fd7f42e6d01a5b860d2ed893641f476.js"></script>

### [CreateRemoteThread](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createremotethread)

- This API is used to create a thread that runs in the address space of a target process. Our target being notepad.exe, this API will help us run our shellcode in that context
- We specify `hProc`, a handle to the process we are injecting to.
- We then use `WaitForSingleObject` to specify a timeout for the process.
<!-- 
<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=bw&l=text%2Fx-c%2B%2Bsrc&width=768.65625&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=LPVOID%2520pRemoteCode%2520%253D%2520NULL%253B%250AhThread%2520%253D%2520CreateRemoteThread%28hProc%252C%2520NULL%252C%25200%252C%2520pRemoteCode%252C%2520NULL%252C%25200%252C%2520NULL%29%253B%250A%2520%2520%2520%2520%2520%2520%2520%2520if%2520%28hThread%2520%21%253D%2520NULL%29%2520%257B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520WaitForSingleObject%28hThread%252C%2520500%29%253B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520CloseHandle%28hThread%29%253B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520return%25200%253B%250A%2520%2520%2520%2520%2520%2520%2520%2520%257D%250A%2520%2520%2520%2520%2520%2520%2520%2520return%2520-1%253B"
  style="width: 773px; height: 210px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">

</iframe> -->

<script src="https://gist.github.com/trevorsaudi/2f085dfde14d6d3cf53feafe19e53360.js"></script>


## 3. Final Implant

- The final process injection implementation:

<script src="https://gist.github.com/trevorsaudi/8a1a83fdbeeba7b4f1e9cbaedad99f2d.js"></script>

- You can compile with cl.exe using the following flags

```bash
cl.exe /Ox /MT /W0 /GS- /DNDEBUG /Tcprocessinjection.cpp /link /OUT:processinjection.exe /SUBSYSTEM:CONSOLE /MACHINE:x64
```

{{< alert >}}

Start notepad (or the process you are injecting into) before injecting into it.

{{< /alert >}}


<img src="/posts/2023-07-21_red_team03/images/gif3.gif" alt= "" width="750">

- We can verify the messagebox was spawned in context of notepad using Process Hacker.
- Process Hacker is a tool that can help you monitor resources, debug software and detect malware. 
- It has a functionality called "Find Window and Threads", demonstrated below, which you can click and drag to a window to show the kind of resources (processes, threads, handles etc) it is associated with.


<img src="/posts/2023-07-21_red_team03/images/video3.gif" alt= "" width="750">

- We can also see the memory region we had allocated for our target process, marked as RX (Read Executable) as shown below.


![image](/posts/2023-07-21_red_team03/images/image8.png)

- This brings us to the end of our blog, hope you learnt a ton!
