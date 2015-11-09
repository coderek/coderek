---
layout: post
title: "Enum in swift"
date: 2015-06-05 20:03:59 -0400
comments: true
categories: Swift
---


Enum is a very powerful construct in swift. It is all you can expect from a normal enum type in any
traditional language and more. Here I use several use cases to illustrate the usage of enum in swift.

### Simple enumeration

```

enum Status {
    case Active
    case Paused
    case Done
}

```

### Simple enumeration with raw values

```

enum Status: String {
    case Active = "Active"
    case Paused = "Paused"
    case Done = "Done"
}

let s = Status.Active

println("\(s.rawValue)") // Active

```

In the example above, raw values must be of the same type, which is declared in the enum name line.
Raw values are constants. It's the most concrete enumeration that can be specified. Enum in swift
also support something called associated values. It is essentially a more generic enumeration that
differentiate cases by type signatures.


### Enumeration with union types

```
enum Resource {
    case INDEX()
    case GET(id: Int)
    case UPDATE(id: Int, params: [String: AnyObject?])
    case POST(params: [String: AnyObject?])
}
```

Here is a enumeration of RESTful resource methods. Each of the requests takes in different set of
parameters. The cases are different from each other by the number of parameters and its order and
types. So we can test the case by doing the followings:


### Fetching associated values from enum
```
let method = Resource.GET(id: 1)

switch method {
    case .INDEX():
        println("this is an index method")
    case .GET(let id):
        println("this is an get method")
    default:
        println("this is a default method")
}
```

Note that in the case testing, I use `let` to get the value out of the method. This means that the
value is actually stored in the case instance. So we may have same case with differnt values. This
is where enum shows it's power. It can be used for defining union types. Each case assignment
creates a new object which stores the value of that case type.

However if I print out the method object, its type will be `(Enum value)`. Unlike enum with raw
values which comes with a predefined property called `rawValue` to return the constant value of the
case, enum with associate values does not have rawValues.

Here is a tricky part. Remember enum is essentially a type/class in swift. It can define methods.
Thus, we can do something like this.

### Define methods on enum type
```
enum Resource {
    case INDEX()
    case GET(id: Int)
    case UPDATE(id: Int, params: [String: AnyObject?])
    case POST(params: [String: AnyObject?])

    func getId() -> Int? {
        swtch self {
            case let .GET(id):
                return id
            case let .UPDATE(id):
                return id
            default:
                return nil
        }
    }
}

let myResouce = Resource.GET(1)
let myResouceId = myResouce.getId() // 1
```

To unleash its full potential, we can use protocol together with enum. Taken from alamofire library:

### Comply protocol, making clean APIs 
```
public protocol URLRequestConvertible {
    /// The URL request.
    var URLRequest: NSURLRequest { get }
}

enum Router: URLRequestConvertible {
    static let baseURLString = "http://example.com"
    static let perPage = 50

    case Search(query: String, page: Int)

    // MARK: URLRequestConvertible

    var URLRequest: NSURLRequest {
        let (path: String, parameters: [String: AnyObject]?) = {
            switch self {
                case .Search(let query, let page) where page > 1:
                    return ("/search", ["q": query, "offset": Router.perPage * page])
                case .Search(let query, _):
                return ("/search", ["q": query])
            }
        }()

        let URL = NSURL(string: Router.baseURLString)!
        let URLRequest = NSURLRequest(URL: URL.URLByAppendingPathComponent(path))
        let encoding = Alamofire.ParameterEncoding.URL
        return encoding.encode(URLRequest, parameters: parameters).0
    }
}
```

This Router enum is used as `URLRequestConvertible` object, while exposing different **APIs** for
searching. This is a better way of making a normal class with methods overloading each other.

This is a more advanced example.

```
enum Router: URLRequestConvertible {
    static let baseURLString = "http://example.com"
    static var OAuthToken: String?

    // APIs exposed - commented by derek zeng
    case CreateUser([String: AnyObject])
    case ReadUser(String)
    case UpdateUser(String, [String: AnyObject])
    case DestroyUser(String)

    var method: Alamofire.Method {
        switch self {
        case .CreateUser:
            return .POST
        case .ReadUser:
            return .GET
        case .UpdateUser:
            return .PUT
        case .DestroyUser:
            return .DELETE
        }
    }

    var path: String {
        switch self {
        case .CreateUser:
            return "/users"
        case .ReadUser(let username):
            return "/users/\(username)"
        case .UpdateUser(let username, _):
            return "/users/\(username)"
        case .DestroyUser(let username):
            return "/users/\(username)"
        }
    }

    // MARK: URLRequestConvertible

    var URLRequest: NSURLRequest {
        let URL = NSURL(string: Router.baseURLString)!
        let mutableURLRequest = NSMutableURLRequest(URL: URL.URLByAppendingPathComponent(path))
        mutableURLRequest.HTTPMethod = method.rawValue

        if let token = Router.OAuthToken {
            mutableURLRequest.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        switch self {
        case .CreateUser(let parameters):
            return Alamofire.ParameterEncoding.JSON.encode(mutableURLRequest, parameters: parameters).0
        case .UpdateUser(_, let parameters):
            return Alamofire.ParameterEncoding.URL.encode(mutableURLRequest, parameters: parameters).0
        default:
            return mutableURLRequest
        }
    }
}
Alamofire.request(Router.ReadUser("mattt")) // GET /users/mattt
```

I think this is a very ingenious usage of enum. Pretty interesting.

