---
layout: post
title: "sublime tips"
date: 2014-06-26 21:00:33 -0400
comments: true
categories: tools tips
published: false
---

Here are a few good tips I found recently about sublime.

### macro

We can use macro just like it in the real Vim.

in Mac: 

1. press `control` + `q` to start recording
2. do the task we want to repeat
3. press `control` + `q` to stop recording
4. press `control` + `q` + `shift` to repeat the actions

We can save the macro performed. There is `save macro` option in the `Tools` menu.


### find and replace 

Sublimes find and replace feature is another extremely powerful tool. I am talking about the find by regex actually.

If I want to change a list of functions in this form

```
function abc() {
} 
```

to this form

```
exports.abc = function () {
    
} 
```

All I need is find and replace by regex.

1. press `command` + `option` + `f` to open find and replace UI
2. click the `*` to enable regex
3. find `^function[ ]*(\w*)`
4. replace `exports.\1 = function`

Done :)



