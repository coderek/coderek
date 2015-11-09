---
layout: post
title: "About Cache"
date: 2014-08-07 19:57:23 -0400
comments: true
categories:
---

In the realm of web app development, caching means accelerating the serving of page requests by storing some files or data in the user's device (protected by user agent) so the user agent doesn't need to download from the server every time. 

There are 2 important questions regarding this simple definition.

1. how does the user agent decide which request/reponse to store?
2. how does the user agent know if a response is changed on the server side? 

Ideally, the user agent should automatically remember all request/response by creating a table. So the subsequent requests will receive the same response as it has for the first time from the user agent. So this can save maximum traffic. Of course, it can't be right, because some responses can be changed at server side after some time. And some request is never meant to be remembered, for example, POST requets as they can change server states..

So instead of letting user agent remembering all requests, we, web developers have to tell the user agent what and how.

To answering question 1:

We use `cache-control` header in the server response to tell user agents whether to cache a request. 

`Cache-Control: no-cache` never cache a request. Ususally, if you disable the cache from chrome, it will send this header for every request.

`Cache-Control: max-age=3600` This means the user agent can cache the response for 60 minutes, before invalidating it. During this 60 minutes, the user agent doesn't have to contact the server to check its validity. 

`Cache-Control: max-age=0` usually this is sent from **client**, it means, the client will always send a request to server to validate the cache. This is end-to-end validation. All intermediate node between client and server should not change this attribue.

`Cache-Control: must-revalidate` means a cache need always validate. This is similar to `max-age=0` except the server send this header to the user agent. 

How does the server validate the request? This leads to the second question above.

To answering question 2:

For response with `max-age` set, the user agent will calculate the expire time based on the time the response is received and store the expire time in the cache table. The name of the value is `if-modified-since`. Normally, if the user agent's current time is earlier than `if-modified-since` time, it will not query the server. If `max-age=0` is present in the request header, then it will send `if-modified-since` header to the server. Server will then compare the state of the response based on the time. 

Another way to validate the cache is using `etag`. `etag` is a value other than time that can identify a response. It can be a hash of file, a version number. It's much more flexible than the time base validation. It can also be used to do things other than caching. For example, to prevent the overwriting of the same resources when it's open in multiple user agents. 

`etag` is sent by the server for the first time, and remembered by the user agent. User agent then send it as `if-none-match` to the server to validate.

I think`etag` should have higher priority than `if-modified-since` as it's more specific than just time. But in reality they are regarded equally. Client side needs to have all specified validations pass in order to use the cache. However, I suggest we only specify one. 

If the cache is valid, the server must return a 304 without body to indicate the cache can be used. Otherwise, it will process the request as if there is no cache.


======

A note about `etag` in apache server:

Apache server never returns a 304 for `etag` validation if `deflate` compression module is enabled. This is caused by the inconsistency of compression and decompression of headers and body. This is a [known](https://issues.apache.org/bugzilla/show_bug.cgi?id=39727) bug.
