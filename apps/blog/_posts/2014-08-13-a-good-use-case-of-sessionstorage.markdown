---
layout: post
title: "a good use case of sessionStorage"
date: 2014-08-13 21:10:06 -0400
comments: true
categories: html5
---

HTML5 `sessionStorage` allows us to store and retrieve data in user agent. It has same API as `localStorage`. It also has very [good](http://caniuse.com/#search=sessionstorage) browser support. 

However, it differs `localStorage` in a way that `sessionStorage` is contained inside individual window/tab. This means that data stored in `sessionStorage` will not be visible to other window/tab, even though they may sit on the same domain and path. This is also very different from cookie. 

This single attritube makes `sessionStorage` ideal for managing temporary sessions. 

In my application, user session data by default is stored in `localStorage`. Thus, it persists in local computer until user deletes it. 

User can sign in as other user while the eixsting session is active by opening a sub-tab with new session data saved in the `sessionStorage`. `sessionStorage` has higher priority than `localStorage` in my application, so user can act as the new user in the new tab. The new session will be destroyed when user closes the tab. 
