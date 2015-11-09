---
layout: post
title: "Revise OOP - Encapsulation"
date: 2013-11-24 16:16 +0800
comments: true
categories: programming
---

In OOP, objects consist of data and methods. Data can be used to describe the states of the object while methods can be used to change the states of the objects. 

Encapsulation is also called data hiding. It's the abstraction an object introduces to hide away data from outside, so that the user of the object cannot access the internals of the object directly other than using its exposed methods. 



## why care about it?

There are several benefits to encapsulate the data:

1. Hide away the data that is non-important to the users of the object but important to the workings of the object. 
    1. avoid messing up the internal states of the objects
    2. let developers know only the necessities
2. Allow the object creator to define a consistent interface to access the members of an object, so whenever the internal mechanism or naming changes it won't affect the use of the objects. 

Simply put, it allows to write elegant and secure code.

## how does it work?

In **Ruby** it works like this 

``` ruby
# encapsulation

class Animal
  def initialize name
    @name = name 
  end

  def name 
    @name
  end
end

animal = Animal.new "dog"
puts animal.name # "dog"
```

`@` sign marks the instance variable. In **Ruby**, all instance variables are inaccessible directly from the instantiated object. There must be an method defined to read and write the instance variable. But for the sub class there is no such restrictions. **Ruby** also offers convinient methods `attr_reader`, `attr_writer` and `attr_accessor` to generate methods for you. Hence, the above example can be shortened:

``` ruby
# encapsulation (shortened)
class Animal
  attr_reader :name
  def initialize name
    @name = name
  end
end
animal = Animal.new "dog"
puts animal.name # "dog"
```

In **Java**, it is slightly different. The members of an object can be decorated using qualifiers. E.g. `public`, `private`, `protected`. `public` qualifier allows the member to be accessed directly. But this is generally considered as unsafe and thus discouraged. The JavaBean convensions enforce the use of `private` members and a set of `setter` and `getter` are to be defined for them. 

``` java
class Animal {
  private String name;

  public String getName() {return name;}

  public void setName(String _name) {name = _name;}

  public static void main(String[] args) {
    Animal a = new Animal();
    a.setName("dog");
    System.out.println(a.getName()); // "dog"
  }  
}
```

In **Javascript**, the notion of encapsulation is somewhat arbitrary. 

Functions in **Javascript** create a scope or closure. Variables is only accessible within the closure. However, every function invocation create a function object which can have methods attached to it. Those function can be used as a way to access privately scoped variables. For example: 

``` javascript
Animal = function (_name) {
  var name = _name; // private variable
  this.getName = function () {return name;};
  this.setName = function (_name) {name = _name;};
}
a = new Animal("dog");
a.getName(); // "dog"
```

Good thing is the `name` variable is entirely hidden away. 

The problems of this method are:

1. it will be like **Java**, which creates a lot of `getter` and `setter`, this is troublesome and not scalable
2. when the function is used as an object constructor, the accessors defined inside constructor will be copied to all the objects memory space. This is a waste of memory

A probably better way is:  
``` javascript
// inspired by BackboneJS
Animal = function () {
  this.attributes = {};
}
Animal.prototype.get = function (name) {
  return this.attributes[name];
}
Animal.prototype.set = function (name, val) {
  this.attributes[name] = val;
}
dog = new Animal;
dog.set("name", "dog");
dog.get("name"); // "dog"
```

It creates generic `get` and `set` methods, thus save a lot of keystrokes as well as memories.

However, one can still access and change `dog.attributes`.

In ECMAScript 5, a concept of `property` is defined. An object can define properties that can be configured. The configrable attributes include:

1. value          -> value of property
2. writable       -> whether the property can be modified
3. enumerable     -> whether the property can be see in for..in loop
4. configurable   -> whether the property can be deleted or attributes can be changed

By setting writable and configurable to `false`, the property can be prevented from modifications.

``` javascript
// inspired by JS Definitive Guide 6th Edition
var p = {};
Object.defineProperty(p, "x", {
  value: 1.0, 
  writable: false, 
  enumerable: false, 
  configurable: false
});
p.x // 1.0
p.x = 2
p.x // 1.0
```

One thing about the object property, though the propery value cannot be changed, it doesn't hide the data entirely. The property value can still be poked. And given the lengthy property definition, the previous prototypal methods may be a better option.  

## Summary

Encapsulation is just one of many programming paradigms. It's not unique to OOP language. In C, this has be been used extensively. Here I have covered 3 typical main stream OOP languages. Though the implementaion of encapsulation is different but the fundamental idea is same for all. After understanding this, I can make better decsions when I design objects.
