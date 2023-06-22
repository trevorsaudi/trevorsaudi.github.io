---
title: "Cryptography - The Basics"
author: "Trevor Saudi"
date: 2023-03-01

description: "Introduction to cryptography"


image: "/posts/2023-03-01_crypto_basics/images/logo.png" 
images:
 - "/posts/2023-03-01_crypto_basics/images/logo.png"

tags:
- Cryptography
- Cryptohack
- Python
---



## Introduction

![image](/posts/2023-03-01_crypto_basics/images/logo.png)

- I spent the better part of the start of my year doing a lot of problem-solving with Python (secretly preparing for interviews :D ). Most of that entailed revisiting data structures and algorithms.

- Because I am not landing any Google or Microsoft roles anytime soon :) , that knowledge will not go to waste. So let's learn some cryptography with Python!

- I thought this would be a fun experience to document how I solve various cryptography challenges starting from basic beginner-level problems from Cryptohack or Cryptopals to advanced-level problems. This first blog will be focused on laying the groundwork and getting our hands dirty with some practical basic problems that will be used to build upon future challenges 

- Let us look at various important methods and concepts that will serve as our building blocks

## ord() and chr()

- Ascii is a character encoding format that can be used to represent characters/letters. Each letter is assigned a number from 0-127

- The `ord()` function in python can be used to convert ascii characters to their corresponding integers while `chr()` does the opposite.

```bash
>>> ord('A')
65
>>> ord('a')
97
>>> ord('B')
66
>>> chr(65)
'A'
>>> chr(97)
'a'
>>> 

```
### Challenge

- Using the below integer array, convert the numbers to their corresponding ASCII characters to obtain a flag.

`[99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]`

### Solution

- The solution is pretty straight-forward

1. We define a function that takes in an array. Create a result array to store the output of our conversion
2. Iterate through the int_array which is our input, use `chr` on each array item to get the corresponding ASCII value
3. Append to our result and return the output

```python3
def convert(int_arr):
    res = []
    for i in int_arr:
        res.append(chr(i))
    return res


if __name__=='__main__':
    print(convert([99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]))

    # ['c', 'r', 'y', 'p', 't', 'o', '{', 'A', 'S', 'C', 'I', 'I', '_', 'p', 'r', '1', 'n', 't', '4', 'b', 'l', '3', '}']

```
## Hex

- We've mentioned ASCII in our previous example. During encryption, it is common to end up with gibberish ASCII output. That is where hexadecimal comes in. It is a 16-bit number system which means it can represent ASCII in 16 digits/values.
- To use hex effectively, let us see the different ways we can manipulate it.

### bytes.fromhex() and .hex()

- These methods perform an easy conversion between hex and ascii

> Note that .hex() only works with bytes and not strings

```bash
>>> bytes.fromhex('63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d')
b'crypto{You_will_be_working_with_hex_strings_a_lot}'
>>> output = b'crypto{You_will_be_working_with_hex_strings_a_lot}'
>>> output.hex()
'63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d'
>>> 

```

## Base64

- Base64 is another common character encoding format used to represent ASCII in form of 64 characters where each character is equal to 6 bits

### b64encode and b64decode()

- To use these methods in python you first import base64.
- In the below example, we convert a hex string to ASCII bytes, then convert the bytes to bas64

```bash
>>> import base64
>>> bytes_converted = bytes.fromhex('72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf')
>>> base64.b64encode(bytes_converted)
b'crypto/Base+64+Encoding+is+Web+Safe/'
>>> 
```

## Numbers and Bytes

- It is important to know how to handle numbers since some cryptosystems like RSA deal with mathematical computations so it is good to know how to convert characters to numbers

### PyCryptodome

- This library comes packed with methods that will be useful for us.
- You can install it with pip as shown

![image](/posts/2023-03-01_crypto_basics/images/cyrpto1.png)

#### bytes_to_long and long_to_bytes

- These are methods that can be used to quickly convert between integers and bytes as shown:

```bash
>>> from Crypto.Util.number import *
>>> message = b'HELLO'
>>> bytes_to_long(message)
310400273487
>>> long_to_bytes(310400273487)
b'HELLO'
>>> 
```

## XOR

- `One not both` is how I quickly remember XOR operations. It is commonly denoted as `⊕` or the caret operator `^`

| Input 1 | Input 2 | Output |
| --- | --- | --- |
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

- When dealing with longer characters, we XOR bit by bit.
- `pwntools` is a nice library that has an XOR method we can use to work with any data types.

![image](/posts/2023-03-01_crypto_basics/images/crypto2.png)


```bash
>>> from pwn import *
>>> xor(b'abc',13)
b'lon'
>>> xor(13,13)
b'\x00'
>>> xor(123,13)
b'v'
>>> 

```

### XOR Properties

- Suppose a chain of encryptions were done on a plaintext and we have a resulting ciphertext, how do we go about reversing the ciphertext?
- This is where the XOR properties come into play. There are 4 main properties to look into

1. `XOR is Commutative`

- the order does not matter

```bash
a ^ b = b ^ a
```

2. `XOR is Associative`

- When performing an XOR operation on three or more values, the order in which we group those values does not affect the result of the operation.

```bash
a ^ (b ^ c) = (b ^ a) ^ c = c ^ (a ^ b)
```

3. `Identity`

- An element XOR'd with 0 remains unchanged

```bash
a ^ 0 = a
```

4. `Self-inverse`

- An element XOR'd with itself evaluates to 0

```bash
a ^ a = 0
```

### Challenge: Undoing chain of encyrptions

- Given the following chain of encryptions, find the FLAG value

```javascript
KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf
```

### Solution
- Since we have the value of KEY1, we can calculate the rest as follows

> Note that for all operations, we need to convert the hexadecimal to bytes before working with the data.

1. Find the value of KEY2
2. Find the value of KEY3
3. Find the value of FLAG

```python3
>>> KEY1=bytes.fromhex('a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313')
>>> KEY2=xor(KEY1,bytes.fromhex('37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e'))
>>> KEY3=xor(KEY2,bytes.fromhex('c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1'))
>>> FLAG=xor(KEY1,KEY2,KEY3,bytes.fromhex('04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf'))
>>> FLAG
b'crypto{x0r_i5_ass0c1at1v3}'
>>> 
```

### Challenge: Favourite Byte

- We have learnt some fundamentals in working with XOR. Let's apply that to solve some more challenges

> As mentioned for the millionth time, convert to bytes when given data

I've hidden some data using XOR with a single byte, but that byte is a secret. Don't forget to decode from hex first: 

`73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d`

### Solution

1. We first convert our hex to bytes
2. We mentioned that ASCII goes from 0-127 characters, we can iterate over that range converting each integer to ASCII bytes
3. For each element converted to ASCII bytes, we XOR it with our target input

```python3
from pwn import *

def main(input_hex):
    input_bytes = bytes.fromhex(input_hex) #1
    for i in range(0,128): #2
        result = xor(input_bytes,chr(i).encode('utf-8')) #3
        if b'crypto' in result:
            print(result)
            break

if __name__ == '__main__':
    main('73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d') # b'crypto{0x10_15_my_f4v0ur173_by7e}'


```

- I added a check to filter for the bytes 'crypto' which is part of the flag format that we expect in the output 

### Challenge: You either know, XOR you don't

- This is an interesting challenge that relies on the partial knowledge of our output to get the key

### Solution

1. We know part of the flag `crypto{`. We can begin by XORing that with the ciphertext and see if we get anything meaningful that can help us get the key

```bash
>>> from pwn import *
>>> flag = bytes.fromhex('0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104')
>>> output = xor(flag,b'crypto')
>>> output
b'myXORk}:rVU\x10DFWg)adxE+dQFTX\x0fS[Me$~s\x11EF(euk'
>>> output = xor(flag,b'crypto{')
>>> output
b'myXORke+y_Q\x0bHOMe$~seG8bGURN\x04DFWg)a|\x1dTM!an\x7f'


```
- From the above you can see that we XOR'd using b'crypto' then proceeded to add the bracket to b'crypto{' and got an output that had some information that allows us to get the key

2. We can take an educated guess and try using b'myXORkey' which is part of the output of the secret and obtain the flag

```bash
>>> output = xor(flag,b'myXORkey')
>>> output
b'crypto{1f_y0u_Kn0w_En0uGH_y0u_Kn0w_1t_4ll}'
>>> 

```

- We get the flag

## CONCLUSION

- We have covered some basic building blocks that will serve to be very useful in understanding other cryptography concepts. See you in the next blog!