---
title: "Creating malicious Chrome Updater files [.msix] for initial access"
author: "Trevor saudi"
date: 2024-06-11
description: ""
draft: false
subtitle: ""
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
}

</style>



## Introduction

- I recently worked on a project involving adversary emulation of the `BlackCat/ALPHV ransomware operation`. Part of the observed TTPs was abuse of the Windows App installer to create malicous `Chrome updater files` for initial access. These updater files come in (.msix) file extension which is a windows installer package.
<br>
- In this article, we will go over the .msix file format to understand how exactly this package format can be used to execute malicious code on an unsuspecting victim. We will then analyze a malicious sample and further attempt to recreate and test it in a virtual environment.

## The MSIX File Format

- Packaging of files in Windows has undergone several changes over the course of years which has led to the rise of various packaging file formats such as the `EXE, MSI, APPX` and a newer generation such as the MSIX which combines features from the MSI and the APPX packaging. 
- Packaging is important for delivery and distribution of applications as it enables a simplified way of deploying and installing files by packaging all the necessary components and libraries into a single package that is straighforward to use.
- The general MSIX file format can be deconstructed as shown:

<div class="center">
<img src="/posts/2024-06-11_asd/images/msix.png"> 
</div>

### 1. Package Payload

- `Application Files`: This section contains the necessary appllications required for the packaged application to run. These can be exes, DLLs, Config files, resource files or any other type of file.

### 2. Footprint Files

- `AppxManifest.xml`: This file contains metadata about the app apackage such as the entry points, capabilities, names of the package, version, publisher, dependencies, etc.
- `AppxBlockMap.xml`: To ensure file integrity, this file will contain the checksums of all the files in the package
- `AppxSignature.p7x`: The digital signature verifying the publisher's identity and ensures that a package has not been tampered with
- `CodeIntegrity.cat`: This file keeps a cryptographic catalogue file(hence the extension name) to ensure integrity and security of the package

### Why MSIX

- One interesting feature about the MSIX package format is that it supports differential updates, meaning, only the parts of the application that have changed can be updated using a single setup file. This allows for creation of udpater files for various applications such as Chrome in this case.

## Package Support Framework

- The Package Support Framework (PSF), is an open source kit in windows designed to facilitate installation and operation of applications in Windows. It helps one apply fixes to an application without modifying code.

- It allows for extensive configuration to tailor the behaviour of applications. This customization allows resolving of specific compatibility issues without needing tob modify the original code.

<div class="center">
<img src="/posts/2024-06-11_asd/images/psf.png"> 
</div>

- In the diagram above, we see the interaction between the PSF and the packaged application at runtime. Let's discuss the various components.

  - `Config.JSON`: Contains settings and parameters for the PSF.
  - `PsfLauncher.exe`: The initial launcher that initiates the framework.
  - `Runtime Manager dll`: Dll responsible for managing runtime operations within the framework
  - `Runtime fix dll`: Dll that provides runtime fixes and patches required by the application


- The PSF can be used to define post-installation scripts, which will be executed either before or after the application that was packaged has been run. We will see how we can stage our malware for initial access using this.

## Analysis of a malicious sample

- Let us look at a malicious sample from 
