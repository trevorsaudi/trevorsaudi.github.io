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
       margin-left: 40px; 
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
<img src="/posts/2024-06-11_asd/images/msix.png" alt="Students in Science Class" > 
</div>

### 1. Package Payload

- `Application Files`: This section contains the necessary appllications required for the packaged application to run. These can be exes, DLLs, Config files, resource files or any other type of file.

### 2. Footprint Files

- `AppxManifest.xml`: This file contains metadata about the app apackage such as the entry points, capabilities, names of the package, version, publisher, dependencies, etc.
- `AppxBlockMap.xml`: To ensure file integrity, this file will contain the checksums of all the files in the package
- `AppxSignature.p7x`: The digital signature verifying the publisher's identity and ensures that a package has not been tampered with
- `CodeIntegrity.cat`: This file keeps a cryptographic catalogue file(hence the extension name) to ensure integrity and security of the package

### Why MSIX

- One interesting feature about the MSIX package format is that it supports differential updates, meaning, only the parts of the application that have changed can be updated using a single setup file. This allows for creation of udpater files for various applications.

## Analysis of a malicious sample

