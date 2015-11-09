---
layout: post
title: "JavaScript and Closures"
date: 2011-10-24 15:37 +0800
comments: true
categories: JavaScript
---

因为新工作的缘故这两天开始学习JavaScript。
一直在看David Flanagan的JavaScript: The Definitive Guide 6th Edition，收获颇丰。

以前在云风的博客上第一次看到closure这个词的时候就很好奇，但那篇介绍是以C作为例子，讲的也不是很清楚，所以一直都没搞懂closure这个东西。
现在读JavaScript，对这个closure算是有一定理解。
Closure 中文叫做闭包，在JavaScript里函数都是有闭包的特性。



理解闭包必须分两步：
1.JS里面函数是first-class function，就是说函数跟class是一个级别的。 函数可以直接赋值到变量上，它的类型为”function”，这个变量可以直接用来invoke函数。

```javascript
function test1() {
    console.log(1);
}
func_var = test1;
console.log(typeof func_var); //"function"
func_var(); // invoked test1 -> '1'
```

2.JS使用lexical scoping，也就是一个函数的scope在它define的时候就确定了，而不是在invoke的时候才确定。

```javascript
function test2() {
    var b = 1;
    return function () {console.log(++b);};
} 
b = 10;  //无影响
test2()(); //2
test2()(); //2
func_var = test2();
func_var(); //2
func_var(); //3
func_var(); //4
```

可以观察到，如果直接从运行从test2那里得到的函数，得到的结果会一直都是2。因为，每次运行test2，一个新的context被建立，一个新的b在这个context里面被建立。每次返回的匿名函数被挂接在一个新的context里面，所以它使用的b的值一直都是1。
然而，将test2返回的函数赋值到func_var上的时候，被返回的匿名函数原本的context被保存，就像把这个context空间封闭住了，只有，这个匿名函数可以访问。所以每次这个func_var被运行的时候都会只用之前旧的b，它相当于这个函数的私有变量了。
这种closure使var b成为test2这个object的私有变量，把data hide起来，不受其他scope的影响。可以猜想，JS使用这种特性可以实现object-oriented programming。

PS: from SICP about first-class procedures
> In general, programming languages impose restrictions on the ways in which computational elements can be manipulated. Elements with the fewest restrictions are said to have first-class status. Some of the “rights and privileges” of first-class elements are:

>   * They may be named by variables.
>   * They may be passed as arguments to procedures.
>   * They may be returned as the results of procedures.
>   * They may be included in data structures.

> Lisp, unlike other common programming languages, awards procedures full first-class status. This poses challenges for efficient implementation, but the resulting gain in expressive power is enormous.

Javascript is like Lisp very much in this aspect.

updated Dec 3, 2013

In JavaScript, only `function` key word define a scope.

The following example demostrate an important rule in JavaScript:  

    Variables will only be looked up from the scope where it's accessed. 


``` javascript
var fight = function () {
  return hit + 1; // hit is not undefined
}

var fight_again = function () {
  var hit = 3;
  return fight(); // return undefined variable
};

fight_again()
```

``` javascript
var fight = function () {
  return hit + 1;
}

var hit = 0;
var fight_again = function () {
  var hit = 3;
  return fight(); // return 1
};

fight_again()
```
