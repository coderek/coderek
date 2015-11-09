---
layout: post
title: "a shallow look at: lodash - functions"
date: 2014-06-08 21:15:51 -0400
comments: true
categories: JavaScript
---

For qutie a long time, i have been a faithful user of underscore/lodash utility library. The functions i've used are limited to only those simple ones however. e.g. `map`, `reduce`, `filter`, `each`, `range`, `pick`, `pluck` . I thought I wouldn't have a need for more complicated ones, thus never look at other functions.

Turns out, there are in fact more useful functions than I thought of. Many of them are thoughtful patterns that experienced developers used to simplify their work. Here I look at some of them.



### `debounce`

This function can be used in two occations:

1. when you want to execute a function once only after a countdown. the triggering event happening before the countdown will restart the countdown so the execution of the function is delayed.

2. when you want to have a cooldown time for the execution of a function. the triggering event happening before the cooldown will restart the cooldown so the next execution of the function is delayed.

these are 3 interesting and useful use cases given in the documentation.

```javascript
// avoid costly calculations while the window size is in flux
var lazyLayout = _.debounce(calculateLayout, 150);
jQuery(window).on('resize', lazyLayout);

// execute `sendMail` when the click event is fired, debouncing subsequent calls
jQuery('#postbox').on('click', _.debounce(sendMail, 300, {
 'leading': true,
 'trailing': false
});

// ensure `batchLog` is executed once after 1 second of debounced calls
var source = new EventSource('/stream');
source.addEventListener('message', _.debounce(batchLog, 250, {
 'maxWait': 1000
}, false);

```


### `throttle`
Implemented using `debounce`, make sure a function is only executed once within a time span. This will not maintain the context.

```javascript

// override toastr to make it throttle
toastr.success = _.throttle(toastr.success, 1000, {trailing: false});
toastr.info    = _.throttle(toastr.info , 1000, {trailing: false});
toastr.error   = _.throttle(toastr.error, 1000, {trailing: false});
toastr.warning = _.throttle(toastr.warning, 1000, {trailing: false});

// throttled function will not maintain the scope, unless it's bound to
// but we can do this

var a = {
    b: 1,
    c: _.throttle(function () {
        return this.b;
    }, 100),
    d: function () {
        return this.b;
    }
};

alert(a.c()); // 1

var e = _.throttle(a.d, 100);

alert(e()); // undefined

var f = _.throttle(a.d.bind(a), 100);

alert(f()); // 1

```

### `wrap`
Wrapper function, it's a great way to override the default behavior of an object method.

```javascript
// Wrap Backbone.History.navigate so that in-app routing
// (`router.navigate('/path')`) can be intercepted with a
// confirmation if there are any unsaved models.
Backbone.History.prototype.navigate = _.wrap(Backbone.History.prototype.navigate, function(oldNav, fragment, options) {
  var prompt = getPrompt('unloadRouterPrompt', fragment, options);
  if (prompt) {
    if (confirm(prompt + ' \n\nAre you sure you want to leave this page?')) {
      oldNav.call(this, fragment, options);
    }
  } else {
    oldNav.call(this, fragment, options);
  }
});

```

### `partial` or `parital right`

It creates a copy of a function that bind some of the arguments of a function. The context is not changed.
John Resig has some notes about his technique. [http://ejohn.org/blog/partial-functions-in-javascript/](http://ejohn.org/blog/partial-functions-in-javascript/)

```javascript
// backbone model

this.on('change:clickthrough_url', _.partial(sanitizeUrl, 'clickthrough_url'));
this.on('change:image_url', _.partial(sanitizeUrl, 'image_url'));
this.on('change:video_url', _.partial(sanitizeUrl, 'video_url'));

function sanitizeUrl(attrName, model, url) {
    ....
    model.set(attrName, sanitizedUrl);
}

```

### `defer` 

It uses setTimeout 0 to defer compute-intensive task to the end of task queue, so UI renderings do not need to wait for the completion of the task.

```javascript
_.defer(function(){ alert('deferred'); });
// Returns from the function before the alert runs.
```
