---
layout: post
title: "How I use Backbone.Stickit"
date: 2014-09-04 22:48:43 -0400
comments: true
published: false
categories: 
- Backbone
- Software Engineering
---

[Backbone Stickit](http://nytimes.github.io/backbone.stickit/) is a Backbone plugin to solve the problem of two way data binding. 

Naive two data binding is simply synching all views and model. However, there are a few practical issues. 

1. validation of model attributes
   
   Data need to be validated from view to model only. Data can only be set after it's validated. However, validation can't be just client side, server side also need to validate data. So in my case, I do the followings:

   1. validate on client side
   2. send the server to create or update resource
   3. set or save change locally

   In order to validate data before setting it in the model, I need to set `updateModel` option in stickit to `false`. Then I need to get all changed values. Since I am not setting any attribute when the form is changed, I can't get changed values from `Backbone.Model`'s `changed` attribute. By the way, Backbone model's way of managing changed attributes is very much broken. It's suggested to use library like [Backbone Trackit](https://github.com/NYTimes/backbone.trackit). What I want is to trigger all the `getVal` function I have defined in the view binding object, to get all changed values. Stickit doesn't provide that function natively, I have to come up with my own way to do so. 

``` javascript
stickitGetValues : function (attrNames, options) {
    options = options || {};

    var changes = {};
    _.each(this.bindings, function(v, selector) {
        var namespace = '.stickit.' + this.model.cid;
        var $el = this.$(selector);
        var binding = this.bindings[selector];
        if (_.isString(binding)) {
            binding = {observe: binding};
        }
        var config = Backbone.Stickit.getConfiguration($el, binding);
        if (_.contains(attrNames, config.observe)) {
            var val = config.getVal.call(this, $el, 'manual', config);
            if (!options.patch || this.model.get(config.observe) !== val) {
                changes[config.observe] = val;
            }
        }
    }, this);

    return changes;
}

```

   I borrowed `Stickit.getConfiguration` function to get the config by `$el`. Hence, I can have access to the `getVal` function, I've defined in the view bindings. Here, if `patch` option is not supplied, I return all values. Then I do the validation like this:


``` javascript
// in the view
var attrs = this.stickitGetValues(this.model.keys());
var errors = this.model.validate(attrs);

```

   And save like this:

``` javascript
if (_.isEmpty(errors)) {
   this.model.save(attrs, {wait: true, patch: !this.model.isNew()});
} 
```

   This will only set the model (hence trigger change events) after the request is returned successfully.

2. data type of model attributes
   
   In order to do validation, we need to need the proper data type of the attribute and get the attribute with correct type. This is best done in Stickit's `getVal` function:


``` javascript
'[data-id=max_age]'    : {
    observe: 'max_age',
    getVal: function ($el) {
        return _toInt($el.val());
    },

    update: function ($el, val) {
        $el.val(val);
    }
}
```   

3. setter and getter of model attributes

   Stickit allows us to easily format the data before setting it in the view by using `update` function. It also use `getVal` function to getting the value from view. 

   Since I don't set value directly in the model, I never need to use `onSet` and `events` attributes. 


