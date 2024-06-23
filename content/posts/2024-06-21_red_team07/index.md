---
title: "Analysis and Exploitation of a Parser Differential Bug"
author: "Trevor Saudi"
date: 2024-06-11
description: ""
draft: true
subtitle: ""
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

.center { 
       display:inline-block; 
       margin-left: 60px; 
       margin-top: -20px;
}

</style>

![image](/posts/2024-06-11_red_team06/images/logo.png)



## Introduction

- Came across a fascinating vulnerability when reviewing past challenges in a past 'infamous' Google CTF Web Challenge. This particular challenge explores a particular vulnerability occurring wihtin