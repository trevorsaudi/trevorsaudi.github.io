---
title: "CyberTalents Weekend CTF-gu55y writeup(PHP Object Injection)"
author: "Trevor saudi"
date: 2020-12-20T16:26:19.158Z
lastmod: 2022-05-24T14:30:29+03:00

description: ""

subtitle: "Had some spare time over the weekend to participate in this awesome CTF. This challenge covers a web app vulnerability — PHP Object…"

image: "/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/1.png" 
images:
 - "/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/1.png"
 - "/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/2.png"
 - "/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/3.png"
 - "/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/4.png"
 - "/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/5.png"
 - "/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/6.png"
 - "/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/7.png"
 - "/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/8.png"
 - "/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/9.png"


aliases:
    - "/cybertalents-weekend-ctf-gu55y-writeup-php-object-injection-dfe173d9f446"

tags:
- Web
- PHP
---

Had some spare time over the weekend to participate in this awesome CTF. This challenge covers a web app vulnerability — PHP Object Injection(Insecure deserialization). Let’s dive in!

![image](/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/1.png#layoutTextWidth)

> I wonder if you can guess what's going on

### Enumeration 

We get a simple input form that we can fuzz around for a bit to get an idea of what is going on :)

![image](/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/2.png#layoutTextWidth)


Interacting with the form, you notice how the strings get appended to each other.

![image](/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/3.png#layoutTextWidth)

![image](/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/4.png#layoutTextWidth)


Calls for some enumeration. Viewing the source of the page reveals interesting information

![image](/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/5.png#layoutTextWidth)


You can read more on vim swap files below. Typically in vim, swap files act as recovery files when you’re working with vim as your editor.

[Should you disable Vim&#39;s swap files (.swp) being created?](https://webdevetc.com/blog/should-you-disable-vims-swap-files-swp-being-created/)


Following the article, we can access the swap file for the challenge at [http://18.156.117.120/guessy/.index.php.swp](http://18.156.117.120/guessy/.index.php.swp).

Opening the contents of the swap we get the following

![image](/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/6.png#layoutTextWidth)


This information will come in handy towards the end :)

Enumerating further to investigate on the behavior of the input form, I took a look at the cookies and got some juicy info.

![image](/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/7.png#layoutTextWidth)

![image](/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/8.png#layoutTextWidth)


`a%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22hey+%22%3Bi%3A1%3Bs%3A5%3A%22there%22%3B%7D” which is URL encoding for “a:2:{i:0;s:4:”hey+”;i:1;s:5:”there”;}`

Sweet! We have some PHP objects being used to store the data from the input form. Summarizing an article from [https://portswigger.net/web-security/deserialization/exploiting](https://portswigger.net/web-security/deserialization/exploiting) , this is how PHP objects work.

PHP uses a mostly human-readable string format, with letters representing the data type and numbers representing the length of each entry. For example, consider a `User` object with the attributes:

```php
$user->name = "carlos";
$user->isLoggedIn = true;
```
When serialized, this object may look something like this:

`O:4:&#34;User&#34;:2:{s:4:&#34;name&#34;:s:6:&#34;carlos&#34;; s:10:&#34;isLoggedIn&#34;:b:1;}`

This can be interpreted as follows:

*   `O:4:"User"` - An object with the 4-character class name `&#34;User&#34;`
*   `2` - the object has 2 attributes
*   `s:4:"name"` - The key of the first attribute is the 4-character string `"name"`
*   `s:6:"carlos"` - The value of the first attribute is the 6-character string `"carlos"`
*   `s:10:"isLoggedIn"` - The key of the second attribute is the 10-character string `"isLoggedIn"`
*   `b:1` - The value of the second attribute is the boolean value `true`

We can now use the information we have to create our exploit. The swap file contains some php code that uses a magic method `(__toString)` to return an object of the `index.php` page from the class `l33t`. You can read more on magic methods here

#### [What are PHP Magic Methods?](https://culttt.com/2014/04/16/php-magic-methods/)


Simply put, the toString method is being used to return information on the index.php page. We can use this method in constructing a payload that helps us return fl4g.php instead. Keep in mind that the source attribute needs to be included for us to read the fl4g.php page

This article came in handy in creating the final payload to get the flag

#### [How PHP Object Injection works - PHP Object Injection](https://www.tarlogic.com/en/blog/how-php-object-injection-works-php-object-injection/)

### Exploitation

Our final payload will like this
```a:3:{i:0;s:5:"hello";i:1;s:5:"there";i:2;O:4:"l33t":1:{s:6:"source";s:8:"fl4g.php";}}```

URL encode it and supply as the cookie value for list. voila ! you get the flag.
`flag{5w337_PHP_0bj3c7_!nj3c7!0n}`
![image](/posts/2020-12-20_cybertalents-weekend-ctfgu55y-writeupphp-object-injection/images/9.png#layoutTextWidth)


Happy hacking!
