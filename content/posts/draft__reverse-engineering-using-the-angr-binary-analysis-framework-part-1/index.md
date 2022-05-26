---
title: "Reverse Engineering using the angr binary analysis framework (part 1)"
author: ""
date: 
lastmod: 2022-05-24T14:32:23+03:00
draft: true
description: ""

subtitle: "In this article, we look at an interesting tool called angr and how we can use it to perform binary analysis and symbolic execution when…"

image: "/posts/draft__reverse-engineering-using-the-angr-binary-analysis-framework-part-1/images/1.jpg" 
images:
 - "/posts/draft__reverse-engineering-using-the-angr-binary-analysis-framework-part-1/images/1.jpg"
 - "/posts/draft__reverse-engineering-using-the-angr-binary-analysis-framework-part-1/images/2.png"
 - "/posts/draft__reverse-engineering-using-the-angr-binary-analysis-framework-part-1/images/3.png"
 - "/posts/draft__reverse-engineering-using-the-angr-binary-analysis-framework-part-1/images/4.png"


---

In this article, we look at an interesting tool called angr and how we can use it to perform binary analysis and symbolic execution when reverse engineering programs. 

#### Table of Contents

1.  Introduction
2.  Symbolic execution and analysis
3.  Reversing using angr
4.  Limitations of symbolic execution

### Introduction
> angr is an open-source binary analysis platform for Python that combines both static and dynamic analysis and provides tools to solve various tasks

Reverse engineering is a process used in several sectors in IT security such as malware analysis, bug bounty , source code review etc. It seeks to find vulnerabilities and understand the inner workings of software. 

One of the main goals of reversing is to identify how components relate with each other and represent the relationships in higher abstraction levels. During software reverse engineering, we analyze binary code to find out it’s functionality. There are many ways and tools of analyzing and reversing a compiled program and symbolic execution is one of them

### Symbolic Execution and Binary Analysis

Symbolic execution is a process of analyzing a program to determine what inputs cause each part of a program to execute. We can use a simple program below to illustrate this




It is a basic program that reads and checks a user’s input, and validates it if the input is not equal to 20. Running this code with the input as 5 for example, will cause it to fail, if we supply 20 we get a “well done” message.

In symbolic execution, instead of supplying 5 or 20 as our input, a **symbolic input** is supplied. The symbolic input is mathematically represented by a symbol such as γ (lambda), and then tracked down execution in terms of that symbol.

Suppose you buy 5 mangoes that cost 500 shillings, how much will one mango cost? This can be represented as follows:

5x = 500

Where x is the symbolic input that will be supplied to satisfy the equation. 

Enough of mangoes and back to the program above. During symbolic execution, γ will be supplied to **var** instead of normal integers like (concrete values) 1,2,3,4. Execution will proceed to the 2 branches (failing or printing well done), each path will get assigned a copy of the program’ s state at the branch instruction as well as the constraint e.g **γ == 5** for the first branch and **γ != 5** for the second branch.

These 2 paths can be executed independently and during termination (when the program exits or reaches a failed state), the symbolic execution process will generate a concrete value like 1,2,3,4,5 by solving the constraints for each path — In simpler terms , the symbolic execution engine is going to determine that in order for us to reach the undesired state **exit()**, **γ** would need to equal a value that is not 5.

That may have been a lot to digest but it gets simpler with an example as you will see in the next section

![image](/posts/draft__reverse-engineering-using-the-angr-binary-analysis-framework-part-1/images/1.jpg#layoutTextWidth)


### Reversing using angr

Head over to this link and obtain the binary file we will use for the practical bit.

#### Static Analysis

We will utilize disassembly and decompiling tools to understand what our program is doing. I like to use ghidra for both. We can also utilize other tools for this exercise.

We begin by interacting with our target program to understand what it is doing.

![image](/posts/draft__reverse-engineering-using-the-angr-binary-analysis-framework-part-1/images/2.png#layoutTextWidth)


Our program asks for a password input and displays “Try again” when we supply a wrong password. When we supply a correct password we should expect a certain input.

We proceed to input the program to ghidra to further understand the inner workings of our program. Head over to the functions and observe what is being imported in the program.

![image](/posts/draft__reverse-engineering-using-the-angr-binary-analysis-framework-part-1/images/3.png#layoutTextWidth)


The main entry point to the program shows us that at line 15, our program requests a password. The string is placed in a variable which is then passed into “complex function” for some operations. “Good job” is outputted when we supply the correct password.

We can take a look at “complex function”.

![image](/posts/draft__reverse-engineering-using-the-angr-binary-analysis-framework-part-1/images/4.png#layoutTextWidth)


It indeed is complex :) . Because we are lazy and won’t take too much time reversing the function by hand, we will **angr** the holy grail of symbolic execution, to solve for **γ ,** which in this case is the password we want to supply.
