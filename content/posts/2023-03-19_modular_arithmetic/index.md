---
title: "Cryptography 03 - Modular Arithmetic"
author: "Trevor Saudi"
date: 2023-03-12

description: "Euclidean Algorithm"


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

- What happens when the hour hand of your wall clock crosses 12? It simply goes back to 1.
- That is modular arithmetic. When numbers wrap around upon reaching a given point. When you get to hour 13 on your wall clock, it goes back to 1. 14 becomes 2, 15 becomes 3 and so on... A concept you understand from when you learnt how to tell the time
- Looking at the clock in terms of modular arithmetic, when we cross over the clock at 12 and go to 13, we instead switch to 1 because 1 is the remainder of 13 mod 12. The range of numbers in this case is bounded by 12 and any remainders will simply be in this range.
- This concept is very important in cryptography as it is fundamental to computing private and public keys in RSA as you will see in future blogs. This is true because modular arithmetic introduces the perspective of `finiteness`, allowing us to work with a range of values defined by a modulo operation. This makes it more efficient when handling large prime numbers and factorization in RSA. 
- We will utilize the concepts learnt before - euclidean algorithm  and its extended version, to understand how to compute various operations in modular arithmetic

## Theory of Congruences


- The theory of congruences deals with the concept of numbers being equivalent or congruent to each other, based on a given modulus.
- Sometimes also referred to as an equivalence relation, it follows the principle that algebraic operations done with `equivalent elements` will yield `equivalent results`
- Elements are said to be equivalent to each other based on a specific relationship for example:
- Let's take for example an equation: `A ≡ B(mod C)`, we say that A is congruent to B modulo C, which means that A and B have the same remainder when divided by C. Meaning A and B are equivalent or in the same equivalence class

- We can also look at it this way:
    
    - `A ≡ B(mod C)`, therefore
    
    - `A - B` is divisible by C
- So if we had the following:

    - `37 ≡ 57(mod 10)`

    - `37 - 57` is divisible by `10`

    - `-20` is divisible by `10`

- So `37` and `57` are in the same `equivalence class`
- Let’s apply that knowledge to solve for x in the following equation

    - `11 = x mod 6`

- According to the theory of congruences, both 11 and x have the same remainder when divided by 6. Or, 11 - x is going to be divisible by 6
- We can therefore calculate x by taking 11 mod 6.

    - `11 mod 6 = 5`, therefore

    - `11 = 5 mod 6`

    - `11-5 = 6` which is divisible by 6

- We can also say that 11 and 5 are in the same equivalence class because they both have the same remainder when divided by 6.
- These equivalence relationships are bound by various properties that will help us understand other concepts:

## Properties of an equivalence relation

- `Reflexivity`: every element is related to itself, meaning A is equivalent to A. So a = a (mod n)
- `Symmetry`: if A is equivalent to B, then B is equivalent to A. So a = b(mod n) and b = a (mod n)
- `Transitivity`: if A is equivalent to B and B is equivalent to C, then A is equivalent to C. So if a = b (mod n) and b = c(mod n), then a = c (mod n)

## Modular Inverse

- Before we talk about modular inverses. Let's start by understanding what an inverse is. You have probably come across the concept in your algebra class, where if you multiply a number by its inverse, you get 1
- The inverse of a number `10` would be `1/10`  also written as 10 <sup>-1</sup>. So `10 * 1/10` is `1`
- Note that 0 does not have an inverse
- With the above concept of inverses in mind, in modular arithmetic, a modular inverse of a number a is another number b such that their product is congruent to 1 modulo a given modulus m. In other words, if we have `a * b ≡ 1 (mod m)`, then `b` is the modular inverse of `a modulo m`.
- This can also be written as `a * b (mod m) = 1`. This is important because we are going to use this to calculate modular inverses in the next section

<br>

{{< alert >}}

Modular inverses exist if and only if a and m are coprime, meaning they have no common factors other than 1. If a and m are not coprime, then there is no integer b that satisfies the congruence equation.

{{< /alert >}}

### Calculating modular inverses: Naive approach

- Enough theory, let us see how we can use the euclidean algorithm and its extended version to compute modular inverses
- Find the modular inverse of 3 mod 5
- The expression can be written as
    `3 * b ≡ 1 (mod 5)` 


- You Calculate 3 * b mod 5 for b values 0 through c - 1

- So we plug in the values 0 - 4 for b till we find an equation that gives 1 as the answer

    `3 * 0 mod 5 = 0`

    `3 * 1 mod 5 = 3`

    `3 * 2 mod 5 = 1` <---------- answer

- So the modular inverse of 3 mod 5 is 2
- Let us build some intuition with this calculations:
- Find the modular inverse of 3 mod 13
- The expression can be written as


    `3 * b  ≡ 1 (mod 13)` 

- We ask ourselves this question, what number when multiplied by 3 and divided by 13 will give 1 as the answer?

    `3 * 0 mod 13 = 0`

    `3 * 1 mod 13 = 3`

    `3 * 2 mod 13 = 6`

    `3 * 3 mod 13 = 9`

    `3 * 4 mod 13 = 12`

    `3 * 5 mod 13 = 2`

    `3 * 6 mod 13 = 5`

    `3 * 7 mod 13 = 8`

    `3 * 8 mod 13 = 11`

    `3 * 9 mod 13 = 1` <----------- answer (27 mod 13 is 1)

- The modular inverse of 3 mod 13 becomes 9


### Calculating modular inverses: Euclidean algorithm

- We explained in detail how to calculate the euclidean algorithm and its extended version in the previous [blog](https://trevorsaudi.com/posts/2023-03-12_euclidean_modular/).
- Seeing that it's an efficient method for finding GCD, we can apply the algorithm and its extended version to calculate coefficients that will find us the modular inverse

- Find the modular inverse of 197 mod 3000

- The expression can be written as

    `197 * b  ≡ 1 (mod 3000)` or 

    `197 * b (mod 3000) = 1`


#### Step 1: Find the GCD of 197 and 3000 

- We can do this using the euclidean algorithm

    `3000 = 15(197) + 45`

    `197 = 4 (45) + 17`

    `45 = 2(17) + 11`

    `17 = 1(11) + 6`

    `11 = 1(6) + 5`

    `6 = 1(5) + 1`

- We can see that the GCD of the 2 numbers is 1. There are no common factors between the 2 numbers meaning the numbers are `co-prime`, which was a condition to find these modular inverses

#### Step 2: Express 1 as the difference between multiples of 3000 and 197

- We generally want to follow the pattern of this equation:  `197 * b (mod 3000) = 1`, to find the multiples, we perform back substitution as we saw in the previous blog post with the extended euclidean algorithm

    `1 = 6- 1(5)`

    `  = 2(6) - 1(11)`

    `  = 2(17) - 3(11)`

    `  = 8(17) - 3(45)`

    `  = 8(197) - 3(45)`

    `  = 533(197) - 35(3000)` <--------- We reach this point where we get the multiples of 3000 and 197 that will give us 1

#### Step 3: Apply modulo to both sides

- So,

    `1 = 533(197) - 35(3000)`

- Becomes,

    `1 (mod 3000)= (533(197) - 35(3000))(mod 3000)`

    `1 =  533(197)(mod 3000)` # 3000 mod 3000 is equal to 0 so that part of the equation is removed
    
- The modular inverse becomes 533
- The operations discussed with modular inverses are crucial in key generation in various cryptosystems like RSA

## Conclusion

- I hope your brains are not fried yet :) In the future blogs, we will see how we can use simple prebuilt tools to perform these computations for us and make our lives easier :D. See you in the next blog where we introduce even cooler math concepts 
