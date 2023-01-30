---
title: "Secure Code Review 02 - Path Traversal Bugs"
author: "Trevor Saudi"
date: 2023-01-29

description: "Introduction to source code review"


image: "/posts/2023-01-11-Source_Code_Review_01/images/logo.png" 
images:
 - "/posts/2023-01-11-Source_Code_Review_01/images/logo.png"

tags:
- Secure Code Review
- Hash length extension 
- Python
---


![image](/posts/2022-06-13_zipslip-vulnerability-justctf2022/images/logo2.png)

## Introduction

- In the second part of the secure code review series, we look at <kbd>path traversal bugs</kbd>. A pretty simple bug to exploit with a very high impact on vulnerable systems.
- The path/directory traversal bug allows an attacker to read arbitrary files on the server hosting the application. The impact may lead to the loss of sensitive information like credentials, customer data etc
- Let us look into some vulnerable Python code and see how this issue arises.

## Sample Vulnerable Code

- Can you spot where the issue is?

```python

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        cookies = SimpleCookie(self.headers.get('Auth-Token'))
        if cookies.get('auth_id'):
            username=open(cookies.get('auth_id').value).readlines()[0]
        else:
            username='guest'
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Welcome</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<h1>Hello %s</h1>" % username, "utf-8"))
        self.wfile.write(bytes("<p>This is a protected area, please provide valid token to access</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
```

## Overview
- Let us look at what the application does, discuss a technique for tracing user input and then identify our vulnerability.

### Functionality

- We have one class containing a method called `do_GET`
- From the [python documentation](https://docs.python.org/3/library/http.server.html#http.server.SimpleHTTPRequestHandler.do_GET), the method works by mapping a request to a local file by interpreting the request as a path relative to the working directory
- This method is contained with the `http.server` in-built module
- We begin by retrieving the value of the header 'Auth-Token' and creating a `SimpleCookie` object
- We then check if there is a cookie named `auth_id` in the request headers by using the `get()` method of the SimpleCookie object. When such a cookie is present, it `opens a file with the value of the cookie as its name`, reads the first line of that file, and assigns it to the username variable. When the cookie is not present, the username variable is assigned the value of `guest`.

### Source and Sink

- This terminology is commonly used in data flow analysis and can be applied to the analysis of code. A source is where data comes from while a sink is where data ends. Therefore, we approach our analysis by looking for a`ny areas of the application where a user can input data,` then look at how the data is `being handled`. Spot any `dangerous functions` and find how we can force the application to behave in an unintended way.

### Vulnerability

- Let us apply the above method in finding the issue with the code
- We have this line where we get the header of Auth-Token. 

```python3
    cookies = SimpleCookie(self.headers.get('Auth-Token'))
```

- A user can change the value of the Auth-Token ID and supply the request to the server with their own data. But this is not helpful because that data is not processed by any dangerous function in the code.

- The other part of the code where we receive user input is

```python3
    username=open(cookies.get('auth_id').value).readlines()[0]
```

- We are getting the value of the auth_id cookie. This data can be modified by a user before sending it to the server. Being a point of input, let us look at any dangerous functions in use

- The data is passed to the `open` function that `opens a file and returns a file object`. Because we can edit into the cookie value, it makes it possible that `we can supply a file outside the web root directory` in the server and a file object will be returned and we can read information from the server

- In a nutshell, that is how such a bug can occur in an application. How can this be exploited?

## Attack principle

1. We modify a request being sent to the server and change the "auth_id" cookie to a value such as `'../../../etc/passwd'`
2. The server processes the request by parsing that value and using the `open` function to load the directory. The `../` character allows the attacker to move upward the directory tree
3. The object is accessed and returned to the body 

- The example below shows how the attack works in real-time. Using the python3 IDLE terminal, we can use the open function to read the etc passwd directory as shown: 

```python3
>>> open('../../../etc/passwd').readlines()[0]
'root: x:0:0:root:/root:/usr/bin/zsh\n'
>>> 
```

## Impact

1. `Arbitrary File read`: An attacker can read files on the system with the permissions the web server is running on. This could lead to the disclosure of sensitive info
2. `Remote Code Execution`: Typically, this vulnerability exists commonly in applications that allow one to upload files. An attacker could potentially upload malware to a server and use the path traversal vuln to execute the file gaining remote code execution on a server


## Mitigations

1. Input validation/ Sanitizing user input

- In this method, we patch the issue by sanitizing any foreign characters that may be sent as part of the cookie such as the `../`
- A good way to implement input validation is by `combining it with different security measures`
- In the example below, we filter the `..` by ensuring those characters do not appear in the cookie:

```python3

import os
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
      cookies = SimpleCookie(self.headers.get('Auth-Token'))
      if cookies.get('auth_id'):
        auth_id = cookies.get('auth_id').value
        if ".." in auth_id or not auth_id.isalnum():
          self.send_response(400)
       .
       .
       .
       return
       username=open(auth_id).readlines()[0]
      else:
        username='stranger'
        self.send_response(200)
       .
       .
       .

```
{{< alert >}}

The problem with this implementation is the filter can be bypassed e.g using `URL encoded characters like  %2e%2e`  and other methods

{{< /alert >}}

- Input validating for those URL-encoded characters and other potential bypasses `is not enough` because attackers are constantly finding new creative ways to bypass filters

2. Whitelisting

- This makes it way harder to perform a path traversal because only a select number of paths are allowed. It prevents one from accessing any other files. In the example below we use an array called whitelist which contains the directories the user can access.

```python
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
      cookies = SimpleCookie(self.headers.get('Cookie'))
      if cookies.get('session_id'):
        session_id = cookies.get('session_id').value
        whitelist = ["/path/to/file1", "/path/to/file2", "/path/to/file3"]
        if session_id not in whitelist:
          self.send_response(404)
          .
          .
          .
          return
        username=open(session_id).readlines()[0]
        
      else:
        username='stranger'

```
3. Principle of least privilege

- Ensure the web server user is running with only the minimum necessary privileges. This reduces the impact of the vulnerability.

4. Sandboxing

- Sandbox environments are hardened environments that create a string boundary between the running programs and the operating system.
- Even if an attacker were to gain access, they won't be able to reach other areas of the system, network, OS etc