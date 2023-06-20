---
title: "Cryptography 04 - Fermat's Little Theorem"
author: "Trevor Saudi"
date: 2023-03-12
draft: true
description: "Fermat's Little Theorem"

image: "/posts/2023-03-19_modular_arithmetic/images/logo.png" 
images:
 - "/posts/2023-03-19_modular_arithmetic/images/logo.png"
tags:
- Cryptography
- Cryptohack
- Python
---

![image](/posts/2023-03-19_modular_arithmetic/images/logo.png)


## Introduction

- In the previous article we dove deep into a fundamental topic in number theory and cryptography - modular arithmetic. In this blog, we will look at some interesting Mathematical properties surrounding modular arithmetic, one of them being the fermat's little theorem.
- It is a very important topic in public key cryptography as it helps us test whether a number is prime or not, which is essential in generation of large prime numbers that are used in encryption
- The theorem states that if p is a prime number and a is relatively prime to p, then then a^(p-1) is congruent to 1 (mod p)
- We can represent this in modular arithmetic as

    {{< katex >}}
    \\(f(a,b,c) = (a^2+b^2+c^2)^3\\)
