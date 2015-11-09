---
layout: post
title: "wrapper object in javascript"
date: 2011-10-26 15:35 +0800
comments: true
categories: JavaScript
---

In JavaScript, primitive types behave like objects. They use dot expression to access certain methods. For example

```javascript
var str = "abcd";
console.log(str.length); //4
```

But for object, every property is mutable. If we change the length to 10, it should be changed to 10. However, this is not the case.



```javascript
str.length =10;
console.log(str.length); //4
```

This is because, primitive types don’t actually have methods or properties. The access of those methods or properties invokes creation of their Wrapper Objects, which are String(), Numeric() and Boolean(). So when str.length is evaluated, something like this line is invoked.

```javascript
var tmp_str = new String(str); 
return tmp_str.length; 
delete tmp_str;
```

After tmp_str is returned, it is destroyed. This is a wrapper object. It abstract the actual behaviours of primitive types, making it like a read-only object. Attempting to add/modify method or properties of primitive data types results in no effects. (because changes are only made to wrapper objects which are destroyed after access)

Another thing I learned about JS today is that, all objects in Javascript are “pass by reference”. All primitive types are “pass by value”.
Array are objects. so

```javascript
var a=[1,2,3];
var b=a;
a[2]=0;
console.log(b); //[1,2,0]
```

 

So if there is a need to copy an independent object from another object, we have to write our own copy function.

```javascript
function copyArr(a) {
    var b=[];
    for (var i=0;i<a.length;i++) {
        b[i] = a[i];        
    }
    return b;
}
var a=[1,2,3];
var b=copyArr(a);
a[2]=0;
console.log(a); //[1,2,0]
console.log(b); //[1,2,3]
```

