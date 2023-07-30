---
title: "Malware development: APC Injection with C++"
author: "Trevor Saudi"
date: 2023-07-30
description: "Process Injection part 2: QueueUserAPC Process Injection with C++"
image: "/posts/2023-07-21_red_team03/images/logo.png"
draft: true
tags:
- Red Teaming
- Malware Development

---

## Introduction

- In our previous blog post, we looked into classic process injection, going into the various techniques such as finding target processes to inject to using various APIs, as well as injecting into the said processes.
- There are several methods to perform process injection, we will dive into APC Injection, a more advanced technique, that offers more advantages to the vanilla method.

## Why?

- This method is harder to detect than the standard process injection. Despite implementing some common APIs used in malware development such as `VirtualAllocEx, WriteProcessMemory and OpenProcess`, the major difference is in how shellcode is executed.
- Traditional process injection executes shellcode using `CreateRemoteThread`. This API is overtly suspicious and will get flagged. APC injection uses an API called `QueueUserAPC`, which is less suspicious since it is used in scheduling work for a thread when it becomes idle.

## Asynchronous Procedure Calls

