---
title: "Secure Code Review - Hash Length Extension Attack"
author: "Trevor Saudi"
date: 2023-01-10

description: "Introduction to source code review"


image: "/posts/2023-01-11-Source_Code_Review_01/images/logo.png" 
images:
 - "/posts/2023-01-11-Source_Code_Review_01/images/logo.png"


tags:
- Secure Code Review
- Hash length extension 
- Python
---


![image](/posts/2022-06-13_zipslip-vulnerability-justctf2022/images/logo.png)

## Introduction

- Welcome to the secure code review series, where we take a closer look at different types of code and evaluate them based on potential security vulnerabilities. In this series, we'll be reviewing code from various programming languages, including <kbd>Python, Java, and PHP</kbd>. 
- The goal is to provide valuable insights and feedback to developers and security engineers, as well as to encourage a culture of continuous improvement within the tech community. In each review, we'll be examining sample code for potential security vulnerabilities and providing concrete suggestions for improvement. Whether you're a seasoned developer or just starting out, I hope you'll find this series informative and helpful.
- The only prerequisite for this series is <kbd>being able to read some code :) <kbd>

### Strategies

- Let us discuss some of the best-practice strategies and method we can use when reviewing source code

**Top-to-bottom approach**

- This practice takes an approach that <kbd> begins reviewing code at the  highest level of abstraction </kbd>. By looking at the bigger picture, one can start off by studying the overall architecture of the application, which entails looking into the various modules in an application and their functionalities, dependencies and design patterns.
- Gradually, you move into the specific modules’ functionalities and logic, examining implementation details, documentation, and use of libraries, APIs or dependencies.
- This approach provides a good overview of the application code base and functionalities, and how the different functionalities interact with each other.

**Bottom-to-top approach**

- This idea aims to <kbd>focus on the specific implementation of the details in the code </kbd>such as how data types, functions, APIs, libraries, application logic etc. This information lies at the lowest abstraction of code and the reviewer gradually works upward towards higher level of abstraction such as the architecture in use

**Threat-Modelling approach**

- This approach involves identifying known vulnerabilities and reviewing the code to find those vulns

**Risk-based approach**

- This approach involves identifying any potential risks to the system and focusing the code review process on these potential risks

- These approaches can be used alone or in combination to get a greater understanding of the code base, from the bigger picture down to the intricate details. Automation is also a good way to speed up the process and can help to narrow it down to specific and reduce noise.

 
- Let us begin by focusing on the various building blocks to performing secure code review in python applications

### Reviewing Code

- When reviewing sample code for vulnerabilities at the implementation level, you can look for the following:
1. **Dangerous functions**: Some functions introduce security issues when used <kbd>incorrectly or regardless of how they are used</kbd>. e.g a function like `gets() in C`, should never be used as it introduces buffer overflow vulnerabilities. `include()` or `require() in PHP` can be used to achieve RCE via LFI or RFI vulnerabilities, but correct usage of the functions prevents that
2. **Arguments and constants:** Ensure arguments or constants passed to any potentially dangerous functions are <kbd>properly validated and sanitized</kbd> to prevent injection attacks 
3. **Filters:** Ensure input and output is properly sanitized and filtered to prevent XSS or other types of injection attacks.
4. **Error handling:** properly handling errors prevents leaking of information which may pose security threats
5. **Authentication and Authorization:** sensitive data and resources should be protected to prevent privilege escalation vulnerabilities or authentication bypasses that access such information. Passwords should be hashed properly, salted or encrypted. Users should also be granted minimum permissions/privileges to perform their jobs

## Sample Vulnerable Code
- Let us look into how we can utilize the strategies and chokepoints discussed above for a simple secure code review
- Can you spot the vulnerability in the code below:

```python

import hashlib
from flask import Flask, redirect
from secrets import token_hex

secret = "secret_key"
app = Flask(__name__)

def sign_for_reset(reset_information):
    # compute signature to ensure the reset details cannot be tampered with
    data = secret+reset_information
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

@app.route('/reset_password/<email>')
def reset_password_route(email):
    token = token_hex(16) 
    reset_info = "token="+token+"&email="+email
    params = reset_info+"&sign="+sign_for_reset(reset_info)
    return redirect("https://trevorsaudi.com/reset_password?"+params, code=302)

if __name__ == "__main__":
    app.run()
```

## Overview

- We begin by understanding what the sample code does using a top-to-bottom-approach.

### Dependencies

- The sample code begins by importing `hashlib, secrets` and `Flask`. The `hashlib` library is used for hashing of files and objects, `secrets` module is used to generate secure tokens that are difficult to bruteforce and can be used for tokens for password resets, hard-to-guess URLs etc. `Flask` is used to create a flask app

### Functionality

- We have 2 functions: `sign_for_reset` and `reset_password`
- We can identify one route as well in the application `/reset_password`. This route maps to the `reset_password()` function in the application. We can also see that it calls sign_for_reset and is hence a good starting point for our code review.

**1. sign_for_reset()**
- The function begins by generating a random ID using token_hex, a method in the `secrets` module.
- The `reset_info` variable contains a concatenation of the token ID and the email we are resetting the password for
- The `reset_info` information then gets concatenated with a signature generated by the **sign_for_reset** function which takes the download info and a secret hardcoded in the code, computes a SHA256 hash of the concatenation and returns the hexdigest.
- The function redirects to <params>https://trevorsaudi.com/reset_password?<params> with the download information as the parameters.

**2. sign_for_reset**

- This function uses the SHA256 hash function to sign the download information, which involves concatenating a secret with the password reset information and then computing the SHA256 hash of the concatenated string


### Dangerous functions

- In the ['Reviewing Code'](http://localhost:1313/posts/2023-01-11_source_code_review_01/#reviewing-code) section, we talked about various building blocks and places to focus on in code review. Let us single out the usage of dangerous functions. We mentioned that some functions are not inherently vulnerable, but could introduce security issues when used incorrectly.
- The `sign_for_reset` function computes the `SHA256` hash of the concatenation of the secret and download information.
- Cryptographic hash functions like `MD5,SHA1, SHA256, SHA512` are vulnerable to several attacks. In this implementation, we are looking at a length extension attack that allows us to tamper with the download data information and still be able to sign it as valid.
- Let us look into the vulnerability in depth:

## Hash-Length Extension attack

- This attack abuses poorly constructed authentication schemes
- A hash function takes input, performs calculations on it, and produces a fixed-length output called a digest.
- If the input is large, it is split into smaller blocks and processed one at a time, such as the `CBC (Cipher Block Chaining)`, where a hash is generated for a block, then for the next block, add the previous hash to the block and hash it
- The function also adds `predictable padding` to the input before processing it. The padding does not add any security to the overall process. `It will vary based on the length of secret+data`, introducing a requirement where the length of the secret is needed to be able to append more data

### Conditions to be met in an attack :

1. We should know the length of the key
2. We can control the content of the message
3. We already know the hash value of a message containing a key

### Attack principle

- In summary, this is how the attack works:

1. An attacker intercepts a password reset link that is sent to a user's email. The link contains a token and a hash of the token and email address.

2. The attacker knows that the hash function being used is vulnerable to hash length extension attacks, such as the one in the code provided.

3. The attacker can use a tool such as **[hashpump](https://github.com/bwall/HashPump)** to generate a new hash that has the same prefix as the original hash, but with additional data appended to it. The additional data is a command to change the email address associated with the account to the attacker's email address.

4. The attacker can then use the modified password reset link to reset the password for the account, effectively taking over the account.

{{< alert "edit" >}}
In case we do not know the length of the secret, we can bruteforce the padding length to find a hash similar to the one generated by the program
{{< /alert >}}



## Remediation

### Cryptographic Signing Schemes

- A more secure alternative to using a simple hash function is to implement a cryptographic signing scheme, such as HMAC or a digital signature scheme like RSA or ECDSA. These methods use a key to sign and verify the data, making it more difficult for an attacker to alter it.

- Below is an example of the secure implementation to remediate the vulnerability. hmac module is used to create a message authentication code (MAC) of the reset information. The MAC uses a secret key to sign the data. An attacker can't generate a valid MAC without knowing the secret key

```python
import hmac

secret = "secret_key"
app = Flask(__name__)

def sign_for_reset(reset_information):
    # compute signature to ensure the reset details cannot be tampered with
    data = reset_information
    return hmac.new(secret.encode('utf-8'), msg=data.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

@app.route('/reset_password/<email>')
def reset_password_route(email):
    token = token_hex(16) 
    reset_info = "token="+token+"&email="+email
    params = reset_info+"&sign="+sign_for_reset(reset_info)
    return redirect("https://trevorsaudi.com/reset_password?"+params, code=302)

if __name__ == "__main__":
    app.run()

```

- Hmac module is used to create a message authentication code (MAC) of the reset information. The MAC uses a secret key to sign the data. An attacker can't generate a valid MAC without knowing the secret key, hence mitigating the vulnerability


