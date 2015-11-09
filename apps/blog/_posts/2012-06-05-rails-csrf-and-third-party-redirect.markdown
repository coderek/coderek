---
layout: post
title: "rails CSRF and third party redirect"
date: 2012-06-05 15:52 +0800
comments: true
published: false
categories: rails security
---

今天帮同事解决了一个rails的问题。

这是一个网上会员服务网站。每个准会员要先填写资料，然后交费成为正式会员。

我们用session来存储他填写的资料，然后redirect到第三方的网站（我们用的是eNets）付款。成功付款后，eNets会redirect用户到我们事先给他们的一个付款成功的链接页面完成交易。前面的步骤都很好，就是当eNets转到我们的页面的时候，用户储存的session都不见了。

一开始我怀疑是eNets那边post到我们服务器的时候没有附上session id。我查看了eNets Post到我们服务器的request，cookie里的session id并没有变动，跟浏览器里储存的一模一样。那么肯定是服务器那边的session出问题了。通过log，我发现所有的session值都是空的。那么这个session肯定是被invalidated了。

我上网查看了一下rails的安全措施，发现它的每个form都会附带上一个token，这个token是为了防止cross site request forgery(csrf)。rails的controller会检查每个post的请求里的token，看认不认识这个token。不认识或者根本就没有的话，本次的session会直接删除掉。
所以这个解释了为什么eNets发过来的请求会找不到session了。
参考这个页面，在controller最顶端加入了

`protect_from_forgery :except => :paymentsuccess`

session就可以继续了。