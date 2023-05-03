---
title: "Symbolic Execution with Angr - part 1"
author: "Trevor Saudi"
date: 2022-08-15

subtitle: "An overview of symbolic execution with angr"

image: "/posts/symbolic_execution_angr_part1/images/angry_face.png" 


aliases:
    - "/symbolic_execution_angr_part1"

tags:
- python
- angr
- reverse engineering
- exploit development



---
![image](/posts/symbolic_execution_angr_part1/images/1.png)

_An overview of the binary analysis python framework angr in performing symbolic execution._

## Symbolic Execution

Before introducing the angr python framework, it is important to understand the key concept that lies at the heart of angr's core functionality - symbolic execution.

Symbolic execution is a technique of program analysis where instead of supplying normal inputs to a program during testing, symbolic inputs that represent arbitrary values are supplied. 

Think of symbolic inputs as variables such as those in algebra. Since we are trying to find a variable that will trigger a given state, symbolic execution will walk through all possible paths to reach that desired state, solving for that particular variable.

Suppose we have an equation as follows:
{{< katex >}}

\\(x^2 + 6x + 18 = 12\\)



x represents our symbol and it depends on a given **execution path** that binds it.

An **execution path** is how you traverse through the program to reach a state.


### Example 1

Given a simple program, let us map out the execution paths of the program

```python 
input = input('Input the password: ')
if input == 'goodpass':
    print 'Success.'
else:
    print 'Try again.'
```



**path 1**: User enters 'goodpass' as input

{{< mermaid >}}
graph TB;
A[input = λ ]-->B[if input == 'goodpass'];
B-->C[print 'Success']
{{< /mermaid >}}

**path 2**: User enters 'pass123' as input

{{< mermaid >}}
graph TB;
A[input = λ ]-->B[if input == 'pass123'];
B-->C[print 'Try Again']
{{< /mermaid >}}

{{< alert >}}
λ is the symbol that represents our input variable
{{< /alert >}}

To find the value of λ, we can walk back in a given execution path to find out what input triggers a given branch. In the first branch, backtracking leads you to **(if input == 'goodpass')**, where goodpass triggers the desirable input.


Let us look into how we can do this using the angr framework

## The Angr Framework

Angr is a binary analysis framework based on a suite of python 3 libraries that allows you to carry out various tasks. 

With its **symbolic execution engine**, it can step into a binary's various states and follow any branch leading to the states, find a state that matches given criteria and solves for a symbolic variable depending on a given execution path as we demonstrated in the Introduction.

Installation instructions can be found [here](https://github.com/angr/angr)

Clone this [repository](https://github.com/jakespringer/angr_ctf.git) which contains the files we will need throughout this n-part series.

In the **dist** directory, you will find all your project files.

```bash
➜  dist git:(master) pwd
/opt/angr_ctf/dist
➜  dist git:(master) ls
00_angr_find                     07_angr_symbolic_file  14_angr_shared_library        scaffold02.py  scaffold09.py  scaffold16.py
01_angr_avoid                    08_angr_constraints    15_angr_arbitrary_read        scaffold03.py  scaffold10.py  scaffold17.py
02_angr_find_condition           09_angr_hooks          16_angr_arbitrary_write       scaffold04.py  scaffold11.py
03_angr_symbolic_registers       10_angr_simprocedures  17_angr_arbitrary_jump        scaffold05.py  scaffold12.py
04_angr_symbolic_stack           11_angr_sim_scanf      lib14_angr_shared_library.so  scaffold06.py  scaffold13.py
05_angr_symbolic_memory          12_angr_veritesting    scaffold00.py                 scaffold07.py  scaffold14.py
06_angr_symbolic_dynamic_memory  13_angr_static_binary  scaffold01.py                 scaffold08.py  scaffold15.py
➜  dist git:(master)
```

## 00_angr_find

The first example we look into sets us up for basic angr usage.
Run the binary in your terminal to see how it works

```bash
➜  dist git:(master) ./00_angr_find
Enter the password: pass123
Try again.
```
### Program analysis
It is a simple program that asks for a password. We can disassemble the program to find out more information.
Using a disassembler of your choice, disassemble the main function and view your control graph.You can use ghidra, IDA pro, Cutter, radare etc. I disassembled with Cutter

The control graph is not too complicated but we don't have to spend time analyzing it to find the password

![image](/posts/symbolic_execution_angr_part1/images/2.png)

2 branches are of interest. 

![image](/posts/symbolic_execution_angr_part1/images/3.png)

Branch 1 triggered "Try again" while branch 2 should trigger "Good job"

Our goal is to trigger branch 2 by supplying the correct password.

### Solution

Let us build out our solution in python step by step.

1. Import necessary libraries. 

```python
import angr
import sys
```

**sys** library will be used to parse our arguments

2. Instantiate an angr project. 

```python
def main():
    path_to_binary =  '/opt/angr_ctf/dist/00_angr_find'
    project = angr.Project(path_to_binary)  #1
    initial_state = project.factory.entry_state() #2
    simulation = project.factory.simgr(initial_state) #3
```    

We provide the path to the project and use the Project method to create an instance of an angr project to work with. ```#1 ```    

We then create an initial_state variable that holds the entry point to the program. This is necessary for the symbolic execution engine to know where to start exploring the program.```#2```    

We follow through with a simulation manager object that starts executing at the entry point of our program. ```#3```

3. Addresses definition

```python
    print_good_address = 0x8048675 #4
    simulation.explore(find=print_good_address) #5
```

The good address that we want is the one of the branches that leads to printing 'Good job' indicated below as 0x8048675

![image](/posts/symbolic_execution_angr_part1/images/4.png)

4. House-keeping

```python
    if simulation.found: #6
        solution_state = simulation.found[0] #7
        solution = solution_state.posix.dumps(sys.stdin.fileno()) #8
        print("[+] Solution found! : {}".format(solution.decode('utf-8'))) #9
    else:
        raise Exception("Could not find the solution") #10

if __name__ == "__main__":
    main()    
```

Once the execution paths to reach our desirable address have been obtained, we begin by checking if our simulation variable contains something. ```#6```. 

If we found something, we obtain the input that triggered that particular state. ```#7```

We then dump it  ```#8``` and print it out ```#9```

If not, we raise an exception ```#10```

Our final script looks as follows:


```python
import angr
import sys 

def main():
    path_to_binary =  '/opt/angr_ctf/dist/00_angr_find'
    project = angr.Project(path_to_binary)
    initial_state = project.factory.entry_state() 
    simulation = project.factory.simgr(initial_state) 
    print_good_address = 0x8048675
    simulation.explore(find=print_good_address)

    if simulation.found:
        solution_state = simulation.found[0]
        solution = solution_state.posix.dumps(sys.stdin.fileno())
        print("[+] Success! Solution is: {}".format(solution.decode('utf-8')))

    else:
        raise Exception("Could not find the solution")


if __name__ == "__main__":
    main()
```

Run it to see angr perform its dark magic


![image](/posts/symbolic_execution_angr_part1/images/6.png)

We easily find the string that triggers our desirable state.

For the next binary 01_angr_avoid, the solution is exactly the same as this only that you shall have to specify the address of the branch you want to avoid.

In the next tutorial, we will look at more advanced concepts such as how to avoid path explosion and also injecting symbolic values into registers. Stay tuned!