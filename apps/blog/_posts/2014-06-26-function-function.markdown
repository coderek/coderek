---
layout: post
title: "function function"
date: 2014-06-26 20:02:44 -0400
comments: true
categories: programming
---


We did a lot of code refactoring recently. Besides adopting jshint and jscs in our development process, another major thing is that I started using functions extensively.

The coolshell has an article about the functional programming. I read it several time and agree with most of the points in the article. Functional style has its significant place in the programming world. Functions are the foundamental construct that any programming language has to have. It's such a powerful concept that can be extended to simulate many other programming concepts.

For example, function can be used as `module`. This is the basic function declaration

``` javascript
function MyModule (Backbone, Handlebars, jQuery) {

}
```

It can be easily matched to a module pattern. Parameters are the dependencies. It creates a function scope, that encapsulates the code inside.

Another example, function can be used as `class`, or `class` methods. `class` is essentially a template for **a number of stateful functions**. With different context, the functions can represent different object.

``` javascript

// class function
function sayHello() {
    console.log("hello: " + this.name);
}

// a context
var andy = {name: 'andy'};

// another context
var harry = {name: 'harry'};

// both of them can use `sayHello`
// just mount its context onto the function

sayHello.call(andy);
sayHello.call(harry);

```

Function is so powerful such that the `golang` as a replacement of C++, totally abandoned OOP construct (interface is left only, but not useful), since all things can be done using function. Yes, simplicity rules.

Stateless function has benefit of determinism. Stateless means the function can operate without relying on any context. This means, it doesn't use global variable nor `this` context.

``` javascript
function plus(a, b) {
    return a + b;
}
```

This is a simple stateless function. It has no hidden dependencies. It's testable and can be easily made thread-safe.

How beautiful it is!

Ideally, the software we write should consist of **logics** and **controls** only. Logics is the foundamentals of the software, i.e. business logics. It defines the lower bound complexity of the software. Controls are helpers to achieve the logics. How we build the controls defines the performance, correctness and user experience of the software.

Ideally, the trunk of the software should contain only logics. Logicless controls like stateless functions should be extracted out of the program flow. It can be used as utilities.

Thus, another thing I've done for the refactoring is to extract all the functions that has nothing to do with business logics to a cental place. Even this function is used inside a class, or as a method.

E.g.

``` javascript
var User = Backbone.Model.extend({
    defaults: {
        permissions: ['delete']
    },
    comparePermission: function (perm) {
        ......
        // compare perm with this.get('permissions')
        ......
        return isSame;
    }
});

// extract comparePermission to the below

// fns.js

exports.comparePermission = function (perms1, perms2) {
    ...
    return isSame;
} ;

```

I ensure that the functions in the `fns.js` operate in a context free way. This has several benefits.

1. easy to verify
2. easy to test
3. support abstraction of business logic

My class now is lighter, slimer and easy to read.

I love simplicity.
