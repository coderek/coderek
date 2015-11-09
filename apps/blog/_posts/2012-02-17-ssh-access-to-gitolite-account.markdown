---
layout: post
title: "SSH access to gitolite account"
date: 2012-02-17 15:56 +0800
comments: true
published: false
categories: tools
---

The common practice is to create a repo user account (git) to host all the repository. So in principle, users or admin should not have the need to access it through SSH. But I did set it up for myself using my own account. So I got problem accessing it through SSH, because gitolite blacklisted my Key and it only allow SSH to run “info” command, which is to view all the hosting repositories.



After reading the documentation, I found the solution is to run:

`gl-tool add-shell-user ~/.ssh/id_rsa.pub`

However, at the time, I am already denied access to my own account. So I have to login using root account and switch to my account by running

`su zeng`

, then run the aforementioned command.

Now I can git to my server, access my other files easily.

In fact, it’s indeed a good idea to separate repo account from normal use, because there is nothing in there you can use. Those are nothing more than fragmented git refs. There is no code, no nothing. Moreover, everything can be configured locally and push to the server to make effect. But I think at least the install document should mention the issue instead of letting me encountered the problem and required a root access to fix the problem. 