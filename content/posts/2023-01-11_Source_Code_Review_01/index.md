---
title: "Source Code Review 01 - Hash Length Extension Attack"
author: "Trevor saudi"
date: 2023-01-10

description: "introduction to source code review"


image: "/posts/2023-01-11-Source_Code_Review_01/images/logo.png" 
images:
 - "/posts/2023-01-11-Source_Code_Review_01/images/logo.png"


tags:
- Secure Code Review
- Python
---

![image](/posts/2023-01-11_Source_Code_Review_01/images/logo.png)


## Introduction

- Welcome to the secure code review series, where we take a closer look at different types of code and evaluate them based on best practices, performance, and maintainability, with an emphasis on security. In this series, we'll be reviewing code from various programming languages and frameworks, including Python, Java, and PHP. 
- The goal is to provide valuable insights and feedback to developers and security engineers, as well as to encourage a culture of continuous improvement within the tech community. In each review, we'll be examining sample code for potential security vulnerabilities and providing concrete suggestions for improvement. Whether you're a seasoned developer or just starting out, I hope you'll find this series informative and helpful.

### Strategies

- Let us discuss some of the best-practice strategies and method we can use when reviewing source code

**Top-to-bottom approach**

- This practice takes an approach that begins reviewing code at the highest level of abstraction. By looking at the bigger picture, one can start off by studying the overall architecture of the application, which entails looking into the various modules in an application and their functionalities, dependencies and design patterns.
- Gradually, you move into the specific modules’ functionalities and logic, examining implementation details, documentation, and use of libraries, APIs or dependencies.
- This approach provides a good overview of the application code base and functionalities, and how the different functionalities interact with each other.

**Bottom-to-top approach**

- This idea aims to focus on the specific implementation of the details in the code such as how data types, functions, APIs, libraries, application logic etc. This information lies at the lowest abstraction of code and the reviewer gradually works upward towards higher level of abstraction such as the architecture in use

**Thread-Modelling approach**

- This approach involves identifying known vulnerabilities and reviewing the code to find those vulns

**Risk-based approach**

- This approach involves identifying any potential risks to the system and focusing the code review process on these potential risks

- These approaches can be used alone or in combination to get a greater understanding of the code base, from the bigger picture down to the intricate details. Automation is also a good way to speed up the process and can help to narrow it down to specific and reduce noise.

 

- Let us begin by focusing on the various building blocks to performing secure code review in python applications

### Reviewing Code

- When reviewing sample code for vulnerabilities at the implementation level, you can look for the following:
1. **Dangerous functions**: Some functions introduce security issues when used <kbd>incorrectly or regardless of how they are used</kbd>. e.g a function like `gets() in C`, should never be used as it introduces buffer overflow vulnerabilities. `include()` or `require() in PHP` can be used to achieve RCE via LFI or RFI vulnerabilities, but correct usage of the functions prevents that
2. **Arguments and constants:** Ensure arguments or constants passed to any potentially dangerous functions are properly validated and sanitized to prevent injection attacks 
3. **Filters:** Ensure input and output is properly sanitized and filtered to prevent XSS or other types of injection attacks.
4. **Error handling:** properly handling errors prevents leaking of information which may pose security threats
5. **Authentication and Authorization:** sensitive data and resources should be protected to prevent privilege escalation vulnerabilities or authentication bypasses that access such information. Passwords should be hashed properly, salted or encrypted. Users should also be granted minimum permissions/privileges to perform their jobs

## Sample Vulnerable Code
- Let us look into how we can utilize the strategies and chokepoints discussed above for a simple secure code review
- Can you spot the vulnerability in the code below:

```python
import hashlib
from flask import Flask,redirect
from secrets import token_hex
secret = "[....]"
app = Flask(__name__)

def sign_for_download(download_information):
  # compute signature to ensure the download details
  # cannot be tampered with
  data = secret+download_information
  return hashlib.sha256(data.encode('utf-8')).hexdigest()

@app.route('/redirect_for_download')
def redirect_for_download():
    file_id = token_hex(16) 
    download_info = "file_id="+file_id+"&filename=document.pdf"
    params =download_info+"&sign="+sign_for_download(download_info)
    return redirect("https://trevorsaudi.com/download?"+params, 
                      code=302)
```

## Overview

- We begin by understanding what the sample code does using a top-to-bottom-approach.

### Dependencies

- The sample code begins by importing `hashlib, secrets` and `Flask`. The `hashlib` library is used for hashing of files and objects, `secrets` module is used to generate secure tokens that are difficult to bruteforce and can be used for tokens for password resets, hard-to-guess URLs etc. `Flask` is used to create a flask app

### Functionality

- We have 2 functions: `sign_for_download` and `redirect_for_download`
- We can identify one route as well in the application `/redirect_for_download`. This route maps to the `redirect_for_download()` function in the application. We can also see that it calls sign_for_download and is hence a good starting point for our code review.

**1. redirect_for_download()**
- The function begins by generating a random file ID using token_hex, a method in the `secrets` module.
- The `download_info` variable contains the file ID and some strings i.e  `file_id=123230987623187&filename=document.pdf`
- The `download_info` information gets concatenated with a signature generated by **sign_for_download** function which takes the download info and a secret hardcoded in the code, computes a SHA256 hash of the concatenation and returns the hexdigest.
- The function redirects to [https://trevorsaudi.com/download](https://trevorsaudi.com/download)/?<params> with the download information as the parameters.

**2. sign_for_download**

- This function uses the SHA256 hash function to sign the download information, which involves concatenating a secret with the download information and then computing the SHA256 hash of the concatenated string

```python
data = secret+download_information
return hashlib.sha256(data.encode('utf-8')).hexdigest()
```

### Dangerous functions

- In the ['Reviewing Code'](http://localhost:1313/posts/2023-01-11_source_code_review_01/#reviewing-code) section, we talked about various building blocks and places to focus on in code review. Let us single out the usage of dangerous functions. We mentioned that some functions are not inherently vulnerable, but could introduce security issues when used incorrectly.
- The `sign_for_download` function computes the `SHA256` hash of the concatenation of the secret and download information.
- Cryptographic hash functions like `MD5,SHA1, SHA256, SHA512` are vulnerable to a number of attacks. In this implementation, we are looking at a length extension attack that allows us to tamper with the download data information and still be able to sign it as valid.
- Let us look into the vulnerability in depth:

## Hash-Length Extension attack

- This attack abuses poorly constructed authentication schemes
- A hash function takes input, performs calculations on it, and produces a fixed-length output called a digest.
- If the input is large, it is split into smaller blocks and processed one at a time, such as the `CBC (Cipher Block Chaining)`, where a hash is generated for a block, then for the next block, add the previous hash to the block and hash it
- The function also adds `predictable padding` to the input before processing it. The padding does not add any security to the overall process. `It will vary based on the length of secret+data`, introducing a requirement where the length of the secret is needed to be able to append more data

**Conditions to be met in an attack :**

1. We should know the length of the key
2. We can control the message of the message
3. We already know the hash value of a message containing a key

### Attack principle

- Suppose we have a secret called `secret` and data is data. The hash H(secret|data) is 6036708eba0d11f6ef52ad44e8b74d5b. **In this case, the attacker knows the length of the secret and data**
- If an attacker wants to append the string, hacker:
    - The attacker creates a new message by appending the string "hacker" to the original data, resulting in the new string "datahacker".
    - The attacker calculates the length of the original hash and uses that information to create new padding for the new data. i.e we may need to pad 64 A’s to complete a block of data
    - The attacker calculates the new hash H'(secret|datahacker) using the same hash function and algorithm as the original hash.
    - The attacker can now use the new hash H'(secret|datahacker) to impersonate the original sender, as the new hash will match the original hash of the original data with the added string "hacker".
- That data when sent to the server looks valid because it is similar to what would have been generated by the server, so the message the attacker appends and sends to the server is processed because it matches the hash digest

{{< alert "edit" >}}
In case we do not know the length of the secret, we can bruteforce the padding length to satisfy the hash
{{< /alert >}}



## Tools

- We have some tools that can ease the process of exploitation like **[hashpump](https://github.com/bwall/HashPump)**


## Remediation

### Cryptographic Signing Schemes

- A more secure alternative to using a simple hash function is to implement a cryptographic signing scheme, such as HMAC or a digital signature scheme like RSA or ECDSA. These methods use a key to sign and verify the data, making it more difficult for an attacker to alter it.
- Below is an example of the secure implementation to remediate the vulnerability.

```python
import hmac
import os
from flask import Flask, redirect, request
from secrets import token_hex

app = Flask(__name__)
secret = "[....]"

def sign_for_download(download_information, secret):
    #compute signature to ensure the download details
    #cannot be tampered with
    return hmac.new(secret.encode(), download_information.encode(), digestmod='sha256').hexdigest()

@app.route('/download')
def download():
    download_info = request.args.get("download_info", "")
    signature = request.args.get("signature", "")
    if hmac.compare_digest(sign_for_download(download_info, secret), signature):
        # download the file
        return redirect("https://trevorsaudi.com/downloads/"+download_info, code=302)
    else:
        # return 403 error
        return "Forbidden", 403
```