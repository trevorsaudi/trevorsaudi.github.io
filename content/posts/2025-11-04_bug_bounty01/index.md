---
title: "0-1500$ in my first 24 days of bug bounty "
author: "Trevor Saudi"
date: 2025-11-04
description: ""
image: "/posts/2025-11-04_bug_bounty01/images/bounty2.png"
draft: false
subtitle: "A story of how i landed my first bug"
tags:
- Web Security
- Bug bounty
---
![image](/posts/2025-11-04_bug_bounty01/images/bounty.png)

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



## Introduction

- This article is about a journey I recently embarked on to improve my Web security skills. It ended up being a very important experience where I changed my mindset in approaching learning, problem-solving, consistency and discipline
- I took on a challenge where I try to consistently hack on a `bug bounty target` till you achieve a personal objective. Juggling this and a busy 9-5 was surely going to be a task!

- For those that may be unfamiliar with bug bounty: 

> A bug bounty program is a crowdsourced cybersecurity initiative where companies invite ethical hackers and security researchers to find and report software bugs and security vulnerabilities in their applications. In return, they offer monetary rewards or other incentives for successful discoveries. [1](https://ciphrexlabs.com/bcontent/how-to-start-bug-bounty-hunting)


### Picking a target

- The first step and probably the hardest for most beginners. Alot of experienced researchers advocate for [various ways](https://www.uprootsecurity.com/blog/choosing-the-right-bug-bounty-target-a-hacker-s-guide) of choosing your target, I personally prefer working with targets I am already familiar with. It helps to form a connection with the target which goes a long way in maintaining momentum 

- I therefore selected a target which I am a frequent user. I was familiar with a lot of the features, and it gave me an idea of what bugs to look for first.

- Furthermore, I decided to stick to my target for more than 3 months or even more and build a solid understanding that might give me an edge during hunting. 
- I also selected a `secondary target` on a different platform that I would go to in case things get monotonous on the main target.

- While fingerprinting the target, I discovered `GraphQl` was in use. I must admit, I had never worked on GraphQl before, so I sort out to fill this gap and picked up this book -> [`Black Hat GraphQL - Nick Aleks`](https://www.amazon.com/Black-Hat-GraphQL-Attacking-Generation/dp/1718502842). Super useful resource that helped me get familiar and know what to expect when hunting on my target.
![blackhatgql](/posts/2025-11-04_bug_bounty01/images/bql.png)

- [Graphql](https://graphql.org/) is a query language for APIs that lets clients ask for exactly what data they need.
![blackhatgql](/posts/2025-11-04_bug_bounty01/images/graphql1.png)

#### Why GraphQL makes a good BAC target

- GraphQL encourages direct object access by design. It revolves around objects and IDs, which gives more opportunity for `broken access control` bugs to arise. 
- Access control is often incorrectly implemented because the nature of nested queries make authorization complex
- Hidden fields expose more attack vector opportunity.

### Finding IDOR bugs on the target


#### Recon 

- I selected the main app due to rich features that would offer more opportunity for `broken access control bugs` e.g IDORs. My recon process for hunting this bug type is mostly manual. I start by defining the application boundaries e.g `Horizontal` (User to User), `Vertical`(Privilege levels) or `Logical Boundaries` (Workflow/State).
- Here is a quick AI summary of what that entails, which you can use as a base framework for understanding the boundaries of your testing
![summary1](/posts/2025-11-04_bug_bounty01/images//summary-template.png)
- I then create user accounts representing different boundaries, and track their various metadata.

#### Note taking
- Taking good notes allows you to keep track and be thorough with your testing. 

- During testing, I keep track of all requests that I come through as shown below, performing my tests across the various boundaries:
![summary2](/posts/2025-11-04_bug_bounty01/images/attack.png)

- I also keep an Excel sheet to track every possible GraphQL operation name. Here I categorized the operation names, which helped me know what features to start hitting. 


- I automated the process of retrieving the operation names by writing a parser that would extract unique operation names from burp and notify me on discord when new operation names are encountered that I had not tested before. All this tracked on my Excel sheet as well. 

![summary2](/posts/2025-11-04_bug_bounty01/images/operation-parser.png)

- During hunting I also used the autorize extension in Burpsuite to quicken the testing process. 

#### Hunting on New Features

- One big advantage of hunting on a single target for a long time is you tend to quickly notice when new features come up.
- You can keep track of new features via newsletters, the company main page, their social media pages etc.

#### Finding the first 2 IDORs

- I scoured the main application within a few days, testing every single feature that existed.
- After testing the older well known features, I discovered one low severity IDOR that allowed me to leak backup histories, but the triage team decided it had no useful impact to an attacker. I did not give up :)
- When monotony strikes, and I get bored, I would go back to my secondary target to refresh my perspective before coming back. There, I landed 2 duplicates of a Critical and a Medium severity bug.

![summary2](/posts/2025-11-04_bug_bounty01/images/duplicate.jpg)
![summary2](/posts/2025-11-04_bug_bounty01/images/duplicate2.jpg)


- One day when browsing the main target, I noticed 2 `new features` introduced to the platform. I immediately began hunting on these.  
- The tool I wrote extracted all new operation names that I had not tested, making the hunting process faster. 
- And finally, `24 days` later after starting the journey, I was able to find a medium severity UUID IDOR on one of the new features that allowed me to leak emails and configuration data of other users in the platform.
- I had no way of leaking the UUID, nevertheless, I showed I could retrieve the UUIDs via github dorking and this helped maintain the impact. This landed me first bounty - 700$ + 800$ bonus.
![summary2](/posts/2025-11-04_bug_bounty01/images/bounty.png)
- While this was an incredibly simple bug to find, hunting daily and efficiently helped me identify it first.

### Takeaways

- Is the journey worth it? Yes. If you like to hack and want to get paid for it I think it is worth putting the effort for.
- Consistency beats talent.
- Visualize your goal and actively work towards it. 
- Be patient. It can take a while even for someone with a security background to land their first valid paid bug. This field is highly competitive so be ready for duplicates and informatives.

### Resources.

- Recently came across this goldmine on twitter: https://x.com/the_IDORminator
- Writeup compilation: https://pentester.land/writeups/
- Portswigger labs