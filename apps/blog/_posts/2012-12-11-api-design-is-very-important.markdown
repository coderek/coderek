---
layout: post
title: "API design is very important"
date: 2012-12-11 23:34 +0800
comments: true
categories: 
- Software Engineering
---

I was reading coolshell.cn tonight. The author refers to the chapter of modularity in the book `The Art of Unix Programming` as the most charming chapter. Thus, I searched and read it. When I read the following, I couldn't agree more with the book: 

> The APIs between modules have a dual role. On the implementation level, they function as choke points between the modules, preventing the internals of each from leaking into its neighbors. On the design level, it is the APIs (not the bits of implementation between them) that really **define your architecture**.

It reminds me an argument with a senior java engineer happened a while ago. 



The argument started by me complaining about the slow progression of the project. The project we are doing exposes RESTful API to Client applications to do various tasks. The senior engineer stuck at the design phases and some minor issues. I am dependent on his job which I think is straight-forward. After some time, I grow impatient to him and start complaining. I always told him that we need to start by designing the APIs we want to expose first, and document for those APIs. The reason I gave is exactly the same as the excerpt above. I think, design by API can reveal our targets effectively and we could start working concurrently on server and client side efficiently. He thinks this is unimportant. I don't really know his reason. He can't really articulate well anyway. The argument ended up by him calling me idiot. 

As he is senior, I didn't fight back and followed his design. So this is his design. He actually has no design on his own. He uses a framework that is copied from another open source project which does similar work as our's. The result is that he produces a lot of java code in very short time, then the rest of time are mostly spent on debugging, finding out how to modify others' code to suit our requirement. Small changes requires days to complete on his side, let alone some impossible tasks. I tried to document some APIs we exposed, but soon find out that it's impossible to keep up with the changes. We don't have proper API designs!! We are not following RESTful design. We just invent api calls on the spot. OMG! That's the big problem. 

The three complexities of software engineering: source code, interface, implementation. I believe we have all of them vialoted! Our source code is stinkily long. Our interface like I said is a total mess. Our implementation sucks like a hell, many repeated code, bad layered design. Since the code is too long, we never had any preoper refactoring done. This is totally bad. The worse thing is that we are still at the early phase of the project. 

I am mostly doing the client stuff while touching the backend sometimes when the senior developer is unavailable. I can see how painful to change things, and how easy to get lost. 

The senior java engineer is stubborn and persistently thinks that we have to lay down a solid foundation before real work is started. This is true in certain cases. But as java developer always like to complicate things, his solution is inefficient to the simple job. In fact our system is nothing more than a simplified CMS. Although he has many years of experience in java, but I think he is just a novice in architecture design.

In the end, I find that he focus too much on detailed work, and rely too much on others' established source code which is too complex for our problem. He hopes others working code can reduce our work load. But this is not true at all. I haven't mentioned the fatal design flaws that the frameworks has on our system. 

To add some thoughts: 

> OO languages make abstraction easy — perhaps too easy. They encourage architectures with thick glue and elaborate layers. This can be good when the problem domain is truly complex and demands a lot of abstraction, but it can backfire badly if coders end up doing simple things in complex ways just because they can.

> All OO languages show some tendency to suck programmers into the trap of excessive layering. Object frameworks and object browsers are not a substitute for good design or documentation, but they often get treated as one. Too many layers destroy transparency: It becomes too difficult to see down through them and mentally model what the code is actually doing. The Rules of Simplicity, Clarity, and Transparency get violated wholesale, and the result is code full of obscure bugs and continuing maintenance problems.
