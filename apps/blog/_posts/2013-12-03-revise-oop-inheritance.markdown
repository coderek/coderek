---
layout: post
title: "Revise OOP - Inheritance"
date: 2013-12-03 19:40 +0800
comments: true
categories: programming
---

OOP language is used to model all kinds of objects in universe. With different  levels of abstraction, there are certain hierachical relationships among the objects. Inheritance is used to describe such relationships. Inheritance is a key concept of OOP. All the OOP langauges have some kind of built in inheritance. 



For example, all **Ruby** objects inherits `Object` class; `Object` class inherits `Kernel` module and `BasicObject` class.

## why care about it?

1.  Code can be reused.   
    Common attributes and methods of objects can be collected to form a parent class.
2.  Class behaviors can be overriden and extended according to specific needs.   
    This can be useful when using third parting libraries.

Inheritance always create new subtypes or supertypes. A dynamic type system is need to manage all. This will be covered by my next post. 

## how does it work?

All classical OOP languages have built in keywords for inheritance. In **Ruby**, this is super easy. But let's look at **Javascript** instead. As it's prototype-based and inheritance can be a bit tricky: 

``` javascript
// constructor for animal
var Animal = function (name) {
  this.name = name;
};
Animal.prototype.walk = function () {
  console.log(this.name+" is walking.");
}

// constructor for dog -> animal
var Dog = function (name, age) {
  // call parent constructor
  this.constructor.prototype.constructor.apply(this, arguments);
  this.age = age;
};
// copy a parent's prototype and assign to sub class
Dog.prototype = Object.create(Animal.prototype);

Dog.prototype.bark = function () {
  console.log("bark bark, I am "+this.age+" years old.");
};

var animal = new Animal("animal");
var dog = new Dog("dog", 19);

console.log(animal instanceof Dog);    // false
console.log(animal instanceof Animal); // true
console.log(dog instanceof Dog);    // true
console.log(dog instanceof Animal); // true
```

A major constraint of most implementations of inheritance is that they can inherit from only one parent. Obviously, this does not resemble the real life scenarios, where a `Dog` can be both `Animal` and `Pet`, for example. 

This is the major criticism of inheritance. 
The followings will demonstrate how languages circumvent the restrictions of single inheritance while still achieve the same benefits.

### mixins
**Mixins** can be viewed as groups of shared functions between objects. One common example is Utility functions. Class can include the functions in the class definitions hence inherit their functionalities. One distinction of mixins in dynamic languages is that the included functions can automatically inherit the scope of the host object and gain access to object's variables and methods.

### open class
Open class is a feature of dynamic langauges. The class definition can be changed after it's been defined. This can be used to extend the class without inheriting it.  

Here is how **Ruby** use **mixin** and **open class**: 

``` ruby
# mixin
module Intelligient
  def do_math
    "#{@name}: calculating 1+1"
  end
end

# mixin
module Emotional
  def cry
    "#{@name}: cries..."
  end
end

class Animal
  # inherit both
  include Intelligient
  include Emotional

  attr_reader :name
  def initialize name
    @name = name
  end
end

dog = Animal.new ("dog")
puts dog.do_math
puts dog.cry
puts "#{dog.name} can bark? #{dog.respond_to? :bark}" # false

# open class
class Animal
  def bark
    "#{@name}: bark bark"
  end
end

# after modify the class, the `dog` object can bark now. 
puts "#{dog.name} can bark? #{dog.respond_to? :bark}" # true

# check types
puts dog.is_a? Intelligient # true
puts dog.is_a? Emotional    # true
puts dog.is_a? Animal       # true
```

A few things can be observed here. **Ruby** uses **module** to create **mixins**. Thus **mixins** cannot be instantiated. After including **mixins** `dog` object has the characteristics of 3 types now, namely `Intelligent`, `Emotional` and `Animal`. This is **multiple inheritance** created using **mixins**. Open calss can be used to add new object behavior, even though the objects have already been initialized. However, the side effect is the potential unwanted overriding of existing methods. **Open class** is also called **monkey patch** when it's not used carefully. 

Now **Javascript**:

```javascript
// require underscorejs

var log = function (msg) {
  console.log(msg);
};
// mixin 1
var Intelligient = {
  do_math: function () {
    return this.name + " calculating 1+1";
  },
};
// mixin 2
var Emotional = {
  cry: function () {
    return this.name + " cries..."
  }
};

var Animal = function (name) {
  this.name = name;
};

var dog = new Animal("dog");
// mixins
// also can extend Animal.prototype so mixins will apply to all animals 
_.extend(dog, Intelligient, Emotional);

log(dog.do_math());
log(dog.cry());
log(dog.name + " can bark? " + (dog.bark == undefined));

// open class
Animal.prototype.bark = function () {
  return this.name + " bark bark";
};

log(dog.name + " can bark? " + (dog.bark == undefined));

log(dog instanceof Animal);       // true
log(dog instanceof Intelligient); // error
log(dog instanceof Emotional);    // error
```
Here, I used **underscoreJS**'s `extend` method to inherit from **mixins**.It's almost the same as **Ruby** except the type of the object. Since I create **mixins** as plain object, it does not have a constructor type. But I can easily use **duck typing** to decide the type of the object. This is not a big deal in dynamic language.

Let's look at **Java**.

**Java** doesn't have the concept of **mixins** and **open class**. Once the class is defined, there is no way to modify it.

I have to create a sub class which inherits the parent class and modify from inside the sub class. **Java** also has the qualifier `final`, `protected` and `private` to control the accessibility of the internals of parent class. So when inheriting, sub class only gets what are needed and will not have access nor be able to override any `private` or `final` data or methods in parent. This makes **Java** safer than most dynamic languages.

**Java** uses composition over inheritance. Composition can be seen as a variant of **mixin**. It's a way of adding new behavior by creating **delegate** object inside the main object. 

For example: 

Here I want to create a `controller` which comprises printing functions and scanning functions.

```java
class Test {
  
  abstract class Printer {
    TaskCallback callback;
    public void setCallback(TaskCallback _callback) {callback = _callback;}
    abstract public void print(); // define the behavior
  }

  abstract class Scanner {
    TaskCallback callback;
    public void setCallback(TaskCallback _callback) {callback = _callback;}
    abstract public void scan(); // define the behavior
  }

  interface TaskCallback {
    public void done(Printer p);
    public void done(Scanner p);
  }

  // one implementation of printer
  class ThreeDPrinter extends Printer {
    public void print () {
      System.out.println("print a 3D iron man!");
      callback.done(this);
    }
  }

  // one implementation of scanner
  class ThreeDScanner extends Scanner {
    public void scan() {
      System.out.println("scan a 3D iron man!");
      callback.done(this);
    }
  }

  // main class 
  class Controller implements TaskCallback {
    private Printer printer; // printer delegate
    private Scanner scanner; // scanner delegate

    public Controller(Printer _printer, Scanner _scanner) {
      printer = _printer;
      scanner = _scanner;
      printer.setCallback(this);
      scanner.setCallback(this);
    }

    public void doTask() {
      printer.print();
      scanner.scan();
    }

    public void done(Scanner s) {
      System.out.println("Received: scanner done!");
    }

    public void done(Printer p) {
      System.out.println("Received: printer done!");
    }
  }

  public void test () {
    Printer p = new ThreeDPrinter();
    Scanner s = new ThreeDScanner();
    Controller c = new Controller(p, s);
    c.doTask();
  }

  public static void main(String[] args) {
    Test t = new Test();
    t.test();
  }
}

```

### delegations

iOS developers promote the idea of delegates to handle UI events or specific tasks with separate classes.

It's not so obvious for newbie Android/Java developers like myself at first, so what I did was to create an activity that implements quite a number of event listeners and do all handlings inside the activity, so it ends up with a whole chunk of un-reusable code.

### interfaces

Though a **Java** class can have only one parent, it can implement many **interfaces**. By implementing multiple interfaces, a class can exhibit behaviors of multiple types. This is a way of **multiple inheritance** and it can be very useful together with polymorphism. 


## Summary

In **Java**, a class has to inherit a class to modify it's behavior. So inheritance is still a very important way of extending functions in such languages. In order to gain the flexibility, I have to carefully structure my program into components so that each component's functions can be shared. 

Is inheritance necessary for dynamic language? The answer is probably yes. Though I can use **mixins** to model inheritance, mixins don't maintain states, i.e. they don't have instance variables. And inheriting a class makes the code look much cleaner. I haven't written enough **Ruby** or **Javascript** to fully appreciate its power yet. Maybe it also makes the code look more logical? I am not sure, just my guesses.
