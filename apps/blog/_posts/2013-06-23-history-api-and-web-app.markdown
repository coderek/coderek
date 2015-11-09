---
layout: post
title: "history API and web apps"
date: 2013-06-23 13:05 +0800
comments: true
categories:
  - backbonejs
  - html5
---

Using HTML5's history API is very common in today's web apps. It defines native methods in browser to let developers to manage page urls and bind events with url changes without forcing full page reload.

Before HTML5 history API, anchor link with `#` post-fix address is used as a workaround. When user clicks anchor link, the the page recognize that the canonical url is the same as url requested except the portion after `#` and then default to look for an element with `id` matching the post-fix in the current page and scroll the page to that element. Developer building web apps usually override the default behavior to do something else, e.g. rendering another page. Because the anchor link is just a normal link, it's automatically managed by browser history. 

The major shortcomings of this workaround is the use of `#` sign. It's not search engine friendly; it makes url look ugly. Other problem is the lack of control over the browser history stack.



History API is exact solution for this. Details of the spec can be found [here](https://developer.mozilla.org/en-US/docs/Web/Guide/API/DOM/Manipulating_the_browser_history). Due to its use of ordinary url, the ajax request and normal web link will be indistinguishable. As a result, there are 2 new interesting ways of constructing web applications.

**Not-so-fat web app**

This class of web app is not so fat. Most of the app logic are done at the server side. Server side renders the page or sub-page. The client is responsible just for the displaying. The prime example is Ruby on Rails. 


Rails 4.0 implements a default feature called turbolinks. It turns every link to ajax link, which will fetch the content without layout. Underlying, it uses concepts similar to [PJax](https://github.com/defunkt/jquery-pjax). Due the how the rails apps are structured, most apps do not need any major modifications to enjoy the speed of turbolinks. 

This is an example of Pjax to demonstrate the concept.

```ruby
require 'sinatra'

module Pjax
  class App < Sinatra::Base
    ... 

    get '/' do
      erb :index, :layout => !pjax?
    end

    get '/:page.html' do
      erb :"#{params[:page]}", :layout => !pjax?
    end

    helpers do
      def title(str)
        if pjax?
          "<title>#{str}</title>"
        else
          @title = str
          nil
        end
      end

      def pjax?
        env['HTTP_X_PJAX']
      end
    end
  end
end
```

The request to pjax application will have a `HTTP_X_PJAX` header to denote the different type of request. If it's not present, it will be consider as a fresh request, the response will return the rendered view with layout. Otherwise, only the concerning portion of the page will be rendered.   


**Fat web app**

Fat web app is responsible for all the template rendering and logic computing and navigations. The server side is only minimally serving API request and validate the user inputs. 

In this case, **server side will direct all the relevant urls to the `index.html` ** which is to bootstrap the application. Internally at the web app, it will have a robust routing system to render the page. All the anchor links inside the page is hijacked unless it's exempted by some special attribute. 

```javascript

// in page link handling
// hijack all in page anchor links, unless [data-bypass] is present

$(window.document).on('click', 'a[href]:not([data-bypass])', function(e) {
  if (!e.metaKey && !e.ctrlKey && !e.shiftKey) {
    var protocol = this.protocol + '//';
    var href = this.href;
    href = href.slice(protocol.length);
    href = href.slice(href.indexOf("/") + 1);

    if (href.slice(protocol.length) !== protocol) {
      e.preventDefault();

      // let the backbone router to handle
      Backbone.history.navigate(href, true);
    }
  }
});

```

### summary

The first way of using history API represent the evolution of old fashion web page style development in the era of web app development. It's the hybrid of both world with the benefits of both. But as the web app get's more and more complicated, there may have tons of sub pages needed to be rendered. Rendering at client side will eventually be a need.

And as browser become more powerful, it makes sense to shift more and more weight to the client.Thus the second method makes more sense to me. It defines clearly the resposibilities of client and server. There is only minimum overlap. It makes the architecture scalable.
