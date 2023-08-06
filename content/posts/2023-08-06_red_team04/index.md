---
title: "Malware development: APC Injection with C++"
author: "Trevor Saudi"
date: 2023-08-06
description: "Process Injection part 2: QueueUserAPC Injection with C++"
image: "/posts/2023-08-06_red_team04/images/logo.png"
draft: false
tags:
- Red Teaming
- Malware Development


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



</style>

![image](/posts/2023-08-06_red_team04/images/logo.png)


## Introduction

- In our previous blog post, we looked into classic process injection, going into the various techniques such as finding target processes to inject to using various APIs, as well as injecting into the said processes.
- There are several methods to perform process injection, we will dive into APC Injection, a more advanced technique, that offers more advantages to the vanilla method.

## Why?

- This method is harder to detect than the standard process injection. Despite implementing some common APIs used in malware development such as `VirtualAllocEx, WriteProcessMemory and OpenProcess`, the major difference is in how shellcode is executed.
- Traditional process injection executes shellcode using `CreateRemoteThread`. This API is overtly suspicious and will get flagged. APC injection uses an API called `QueueUserAPC`, which is less suspicious since it is used in scheduling work for a thread when it becomes idle.
- Enough of the technical jargon, let's dive into what these terms mean.


## Program Execution in Modern Operating Systems


- When programs are executed in Windows, the operating system allocates necessary resources to the program to start the execution.
- During the execution, multiple threads are usually assigned to a program. A thread in this case represents a sequence of instructions that can be scheduled by the OS to run.
- If a program needs to perform I/O operations such as reading of data from files, it uses `synchronous calls`, which halts the execution of the thread to allow the I/O operation to take place.
- To address this inefficiency issue, modern Operating Systems will provide support for `asynchronous calls`. This allows the thread to continue execution after handing over the I/O operation to the OS.

## Asynchronous Procedure Calls

- When an asynchronous I/O operation is completed, the operating system can `queue an APC associated with that I/O operation`. 
- The APC can contain some code or a function that is `executed in response to the completion of the I/O event`. This requires a thread to be in an `alertable state`, which is when a thread is idle and ready to receive Asynchronous Procedure Calls. This allows the OS to deliver the APC to the thread hence executing the code.


### QueueUserAPC() 

- This Windows API allows an application to queue an APC to a specified thread. Its implementation is as follows:

<script src="https://gist.github.com/trevorsaudi/4e746b74ed05aa90bfeb3315131b7b0a.js"></script>

- `pfnAPC`: This is a pointer to the function that you want to be executed asynchronously. This function will be invoked when the thread is in a `state where it can process APCs` (also known as an `alertable state`).

- `hThread`: This is a `handle` to the thread that you want to queue the APC to. A handle can be thought of as a unique identifier used to interact with a resource, in our case this will be a specific thread.

- `dwData`: This is the data that you want to `pass to the APC function`. It's a single number (an integer, technically a `ULONG_PTR`) that can be used for whatever you want. It is up to you to decide what you want for this value (error code, status code, commands)


#### Implementing the QueueUserAPC() API

- I will demonstrate a simple example of how we queue an APC in C++. We will create a thread and execute it. After its execution, we will then queue our APC and see how it gets executed.

1. Starting with an empty C++ project. Import the Windows.h header and create a simple thread as shown.
- `ThreadProc` is a callback function that is going to be executed by CreateThread() as a thread.

<br>

<script src="https://gist.github.com/trevorsaudi/379ad5cc5a614ab5c8b92062641e7d6e.js"></script>

<br>

2. We can use print statements to show that the thread is being executed.

<br>

<script src="https://gist.github.com/trevorsaudi/1d5e663762296ec74353d8c11d4d798d.js"></script>

<br>

- We use `wprintf` to print out our messages. It is similar to `printf` but is used to print wide-character strings. It takes in wide character literals indicated by the prefix `L`
- `GetLastError` is used to grab the last error code value

<br>
{{< alert >}}
When `CreateThread` is called, it may return before ThreadProc finishes executing. That is why we use the `sleep function` inside the main() function to allow ThreadProc to finish executing. 
{{< /alert >}}
<br>

3. We finally queue in our APC using the `QueueUserAPC` function. Remember that we mentioned we can only queue in threads that have been put in an `alertable state`. So how do you do this?

- [msdn](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-queueuserapc) docs describes this as shown in the screenshot below.


![image](/posts/2023-08-06_red_team04/images/image1.png)

- TLDR; We can use the `SleepEx` function to make our thread `alertable before queueing in the APC`. We adjust our code by adding the API and a [callback function](https://learn.microsoft.com/en-us/windows/win32/api/winnt/nc-winnt-papcfunc) that will be queued in after the thread has been executed.
- The callback function has a parameter called `Parameter`, which contains the data that is passed in the `dwData` parameter in the QueueUserAPC() function, which was `123`. We can print it out as well to confirm that as shown in line 22

<br>

<script src="https://gist.github.com/trevorsaudi/ba3eb25f6240ba3ab3ee973fa74292eb.js"></script>

- It executes as shown:

<img src="/posts/2023-08-06_red_team04/images/gif5.gif" alt= "" width="750">


### Implementing QueueUserAPC() in our implant.

#### High-Level Overview

- We now have some understanding of how QueueUserAPC works. A high-level breakdown of how the implementation works is as follows.


1. Create the target process in a suspended state.
2. Allocate memory using `VirtualAllocEx` in the suspended process.
3. Define the `APC callback routine`, it is going to point to our shellcode
4. Write shellcode into the allocated memory withing the target process using `WriteProcessMemory`
5. Queue the APC to the main thread using `QueueUserAPC`.
6. Once the thread is resumed the shellcode is executed.

<br>


<script src="https://gist.github.com/trevorsaudi/071f253df7fd1a3f438f73f57d2ab054.js"></script>


<b>Key Points</b>

- In line 38, we define our APC routine using `PTHREAD_START_ROUTINE` which declares the APC callback as a pointer to a variable. In this case, our variable would be the `shellcode` defined in line 6.
- In lines 45 & 46 we define 2 structures necessary in implementation of the `CreateProcessA` API. We use these structures to access information about the process that we are creating. You can see this in line 52 where we obtain the process id and thread id of notepad.

#### Final demo

- Using processhacker, we can further verify our process spawned in the context of notepad as shown.

<img src="/posts/2023-08-06_red_team04/images/gif6.gif" alt= "" width="750">


## Conclusion

- I hope you enjoyed diving deep into how this technique works. You can play around with the code and see if you can implement some form of encryption for the shellcode. Happy hacking !!
