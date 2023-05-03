---
title: "whistleblow-CSAW CTF Quals 2020"
author: "Trevor saudi"
date: 2020-09-14T10:41:54.486Z
lastmod: 2022-05-24T14:30:07+03:00

description: ""

subtitle: "The second challenge in the web category."

image: "/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/1.png" 
images:
 - "/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/1.png"
 - "/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/2.png"
 - "/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/3.png"
 - "/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/4.png"
 - "/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/5.png"
 - "/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/6.png"
 - "/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/7.png"
 - "/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/8.png"
 - "/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/9.png"
 - "/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/10.png"


aliases:
    - "/whistleblow-csaw-ctf-quals-2020-9e4bd6ba7aa2"
tags:
- Web
- AWS S3
- CTF

---

The second challenge in the web category.

![image](/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/1.png#layoutTextWidth)


From the description and 2 hints, this was what I was able to deduce after several minutes:

### Challenge description:

One of your coworkers in the cloud security department sent you an urgent email, probably about some privacy concerns for your company.

**Hint 1:**

Presigning is always better than postsigning

**Hint 2:**

Isn’t one of the pieces you find a folder? Look for flag.txt!

**letter:**

![image](/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/2.png#layoutTextWidth)


From hint 1 , lots of googling reveals the challenge is related to aws. Since I hadn’t worked with any aws CTFs before, I decided to delve into some related writeups and reading aws documentations to get some context on what this challenge was about

This particular writeup came in handy !

[AWS S3 CTF Challenges](https://n0j.github.io/2017/10/02/aws-s3-ctf.html)


Okay, so we’ve gathered enough information on how to start the challenge…

### Step 1: Authenticating as a valid user

From the letter , ‘ Make sure you’re a valid user!’ is a hint that you need to successfully authenticate as a valid aws user to access the S3 bucket which is ad586b62e3b5921bd86fe2efa4919208

![image](/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/3.png#layoutTextWidth)


### Step 2: Accessing the S3 bucket

The aws documentation came in handy! I believe in reading documentation as it saves you alot from unintended errors.

[ls - AWS CLI 1.18.137 Command Reference](https://docs.aws.amazon.com/cli/latest/reference/s3/ls.html)


From the documentation, you get a command to list the contents of the bucket

Interesting , so the bucket contains several folders

![image](/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/4.png#layoutTextWidth)


### Step 3: Analysing the bucket contents

I had to find a way to easily work with the contents of the bucket. The best way was to recursively download the bucket contents to my local directory

The cp command comes in handy and we get access to all folders in the bucket in our current local directory.

![image](/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/5.png#layoutTextWidth)


Now my guess work starts here :D

I have no way of automating this process since I don’t know what to do, so I manually start to view the folders looking for anything juicy. The second folder reveals something interesting.

![image](/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/6.png#layoutTextWidth)


I tried to access the bucket using the aws ls command but that was a dead end. The hunt goes on !

I continued probing the folders and something interesting pops up. An unusually long string.

![image](/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/7.png#layoutTextWidth)


Hmmm… this was my lightbulb moment, everything starts to add up as I reread the hints and the presigning information comes in handy.

Pre-signed URLs have five pieces of information; bucket, object, access key, signature, and expiration. `awscli` tends to present them in this form:
``https://<bucket>.s3.amazonaws.com/<object>?AWSAccessKeyId=<key>&amp;Expires=<expiration>&amp;Signature=<signature>``

Since the first two pieces of strings stands out from the rest of the other texts in terms of length, I decided to try and grab pieces of text less than/ greater than 30 characters.

![image](/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/8.png#layoutTextWidth)


### Step 4: Solving the challenge

From the above info, we retrieve the following pieces of text

![image](/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/9.png#layoutTextWidth)


Since we now know what presigning urls is, let’s piece the info we have and get the flag.

From the letter, we can get the expiry date and the state in which the letter and convert it into unix time.

From aws presigning protocol documentation

[Authenticating Requests: Using Query Parameters (AWS Signature Version 4)](https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-query-string-auth.html#query-string-auth-v4-signing-example)


we can derive the following:

**path to flag**=[https://super-top-secret-dont-look.s3.us-east-2.amazonaws.com/.sorry/.for/.nothing/flag.txt](https://super-top-secret-dont-look.s3.us-east-2.amazonaws.com/.sorry/.for/.nothing/flag.txt)

**identity**=AKIAQHTF3NZUTQBCUQCK

**Signature**=3560cef4b02815e7c5f95f1351c1146c8eeeb7ae0aff0adc5c106f6488db5b6b

**X-Amz-Algorithm**=AWS4-HMAC-SHA256

**X-Amz-Date**=20200909T195323Z _(Unix date format of the date given in the letter)_

**X-Amz-Credential**=AKIAQHTF3NZUTQBCUQCK/20200909/us-east-2/s3/aws4_request (intenity+date+region)

**X-Amz-SignedHeaders**=host

**X-Amz-Expires**=604800 _(One week in unix time(s))_

**Final url**

[https://super-top-secret-dont-look.s3.us-east-2.amazonaws.com/.sorry/.for/.nothing/flag.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&amp;X-Amz-Credential=AKIAQHTF3NZUTQBCUQCK/20200909/us-east-2/s3/aws4_request&amp;X-Amz-Date=20200909T195323Z&amp;X-Amz-Expires=604800&amp;X-Amz-SignedHeaders=host&amp;X-Amz-Signature=3560cef4b02815e7c5f95f1351c1146c8eeeb7ae0aff0adc5c106f6488db5b6b.](https://super-top-secret-dont-look.s3.us-east-2.amazonaws.com/.sorry/.for/.nothing/flag.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&amp;X-Amz-Credential=AKIAQHTF3NZUTQBCUQCK/20200909/us-east-2/s3/aws4_request&amp;X-Amz-Date=20200909T195323Z&amp;X-Amz-Expires=604800&amp;X-Amz-SignedHeaders=host&amp;X-Amz-Signature=3560cef4b02815e7c5f95f1351c1146c8eeeb7ae0aff0adc5c106f6488db5b6b.)

**Curling the request to get the flag**

![image](/posts/2020-09-14_whistleblowcsaw-ctf-quals-2020/images/10.png#layoutTextWidth)
