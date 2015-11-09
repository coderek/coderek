---
layout: post
title: "Synchronize JavaScript Promises"
date: 2014-07-06 14:08:04 -0400
comments: true
categories: JavaScript
---

We all know that JavaScript is best known for asynchronous programming. In order to cope with the callback hell in such style, people have introduced concept of promise. [[proposal](https://groups.google.com/forum/#!topic/commonjs/6T9z75fohDk)]

With promise, instead of writing code like this

``` javascript

loadWebApp(function() {
    login(function() {
        openUserPreferences(function () {
            changePassword(function() {

            });
        });
    });
});

````

we can do this

``` javascript
loadWebApp().
   then(login).
   then(openUserPreferences).
   then(changePassword).
   then(null, function(err) {
     console.error("An error was thrown! " + err);
    });
```

The code does the same thing, though the latter is far more readable. This is an nice attempt to synchronize JavaScript. 

Today when I study the Selenium WebdriverJS [API](https://code.google.com/p/selenium/wiki/WebDriverJs#Understanding_the_API), I found something even more advanced. It's called `ControlFlow`. With it, we can write something like this.

``` javascript

loadWebApp();

login();

openUserPreferences();

changePassword();

``` 

See the difference? Now it's exactly the same as other synchronous languages, like Ruby. How can it be? What is this `ControlFlow` thing? 

It turns out, the `ControlFlow` behaves like a task queue. Calling its `execute` method with a function, it will put the function in the queue and run it after its previous task is done. Each task returns a promise. The `ControlFlow` recognize the completion of a task by looking at the promise's status. Thus, it serilaizes the execution of the tasks.

To use this feature, one must instantiate a `ControlFlow` instance and call the `execute` method in a wrapper function in respect to the target function. 

What's even better is that, there can be multiple `ControlFlow` running concurrently. It's basically a simulated thread. This is a higher level *thread* comparing to JavaAcript Callbacks.

The cost of this approach is that the functions need to be built on promise and wrapped using `ControlFlow`. A layer of abstraction. Is it worthy? At least, IMHO, writing BBD using this style is a good idea.  


PS: I just found that there is this briliant middleware pattern which is used in [connect](https://github.com/senchalabs/connect/blob/master/lib/proto.js#L82) which express is based on. 

``` javascript
//process n number of async functions in order. used when promises aren't viable e.g. cross file or service calls.

var MiddlewareService = function(){
  var stack = [],
    isProcessingStack = false,
    commonState = { task: 0 };


  function push(fn){
    stack.push(fn);

    if(!isProcessingStack)
      next();
  }

  function next(err){
    if(err)
      throw new Error(err);
    
    var fn = stack.shift();

    if(fn){
      isProcessingStack = true;
      fn(commonState, next);
    }
    else
      isProcessingStack = false;
  }

  return {
    push: push
  };
}();



function doWork(commonState, next){
  commonState.task++;
  console.log('Starging something async:' + commonState.task);

  setTimeout(function(){
    console.log('Completed async task: ' + commonState.task);
    next();
  }, 2000);  
}

MiddlewareService.push(doWork);
MiddlewareService.push(doWork);
MiddlewareService.push(doWork);

/* OUTPUT

Starging something async:1
Completed async task: 1
Starging something async:2
Completed async task: 2
Starging something async:3
Completed async task: 3

*/
```
