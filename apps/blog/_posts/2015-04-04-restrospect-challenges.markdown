---
layout: post
title: "restrospect: challenges and learnings"
date: 2015-04-04 00:56:25 -0400
comments: true
categories: 
 - Software Engineering
---

<small>
Disclaimer: I don't show any IP related material here. Here are just some general concepts that I can bring me for the rest of my career.
</small>

It has been a busy year for me. Looking back for what I've done, it is quite impressive. 

{% img /images/github.png %}

There should be commits throughout the year, but I mistakenly used a wrong ID to commit code, thus those commits are not considered part of this chart.

Here are some other stats:

<table>
    <tr>
        <td width="100px">Duration</td>
        <td width="100px">13 months</td>
    </tr>
    <tr>
        <td>JavaScripts</td>
        <td>20444 LOC</td>
    </tr>
    <tr>
        <td>SCSS </td>
        <td>5848 LOC</td>
    </tr>
</table>

<br>

This is a UX intensive project. Over the duration of the development, we had two redesigns of the user interface, and countless logic changes. It is a Backbone project with helps of many other frameworks and libraries. In particular, I've incorporated ReactJS in the last few month to solve the scalability issue. 

Look at the JavsScript Libraries used in the project:

{% img /images/vendor_libs.png %}

I would say it may not be as big as any web project in big companies like Slack, but it is big enough to teach me many lessions. 

The core of Software engineering is to solve complexities of software. So here are the complexities of
this project. For each one listed here, I recount a few problems and solution if there is any.

1. **Organizational complexity**  
    Too many files and too many dependencies. This is all about software architecture. There is no authorative template for
    working with large scale JavaScript Project. When I design the project, the general
    principle I followed is __multi-tier__ and __component based__. What this mean is that, I modularize
    code based on it's sole function with minimal dependencies on others. The required dependecies
    is also uni-directional from bottom to up. There are sometimes needs for global objects. But I
    tried to minimize/localize them to prevent global pollution. One such example I am happy to
    mention is the message channels. I have a handful of global channels that deliver messages
    across tiers. At same time, I also have page channel that is inherited by all components within
    the page.   

    At the beginning of the project, I tried to come up with my own way to organize components. My
    idea is to group all code that is related to a particular function in the same folder. These
    codes include templates, stylesheets and scripts; idea similar to the [web
    components](http://webcomponents.org/) but I have to wire all files individually. The benefits
    of doing this is that it's easy to
    find the files based on it's function. And since all business-related folders are group
    according to business hierachy, it's very easy to locate folders. 

    On the technical part, I am very thankful for choosing [Brunch](http://brunch.io/) to be my project manager. It by
    default, provide commonJS utilities that allow me to modularize files in an easy and intuitive
    way. Its compilation pipeline allows me to easily integrate json, jsx, hbs files as commonJS
    modules. This greatly reduces the organizational complexity.

2. **Business logic complexity**  
    At the beginning, we know what we want to create. But nobody knows how to get there. Thus, the
    first thing we do is try to duplicate the existing functions on another project which has been in
    existence for many years. We try to extract the good parts from the model project and improve
    upon it. But that's merely for the front end. It means we have to be compatible with the
    old system at back. If I can comment on the API side of this new project, I would just say one word,
    that is 'mess'. That's a reasonable comment, because the API side is written using nodeJS and backed by
    MongoDB, it's challenging to come up with good design that is modular. And we had some
    problems with Mongoose as well. It's kind of limited given our use case. 

    But anyway, on the front end I think the biggest challenge is the data validation. Data
    validation is tricky because when we have a big form for instance, there can be a lot of
    inter-dependencies between the data we collected. Very often, we have to express this 
    inter-dependencies in the UI such that user knows what are expected. At model level, we have to
    implement validation rules that exactly match the busniess logic. I know we have to do it on the
    server side again. But since API side is a mess, I can't expect any reuse of the code. 

    Data validation also includes data type checking. This is the part I think I didn't do well.
    Currently, all data fetched from UI is in string type. When I have to do some post-processing, I
    need to convert it to the correct data type first. Especially this involves complex type like
    `moment` object.

    Another problem worth mentioning is the timezone. Our busniess crosses timezones. Timezone is
    complex because it's not always
    [predictable](http://www.creativedeletion.com/2015/03/19/persisting_future_datetimes.html), i.e. it can be changed by government in the future. For
    existing ones, we have daylight saveing timezone which changes at certain time of the year. This
    is hard to manage when we have to specify start/end dates. We have to consider the
    timezone of each date. A good way is to just use City instead of offset. So `moment.timezone`
    library will figure out which offset to apply based on city. But moment.timezone data also has
    its [limitation](http://momentjs.com/timezone/docs/#/data-utilities/filter-years/). An extreme case we had is that, when specifying day parts, we have to slice
    0000~2400 into different parts, it's super complex to specify timezone for individual part on
    the UI. 

3. **UI complexity**  
    UI is the soul of single page application. Without good UI, it's pointless to make it a
    JavaScript intensive app. So what are the challenges. 

    First is the UI foundation. I have to say our app is still page based. In most common case, each
    page represent a campaign. When opening a campaign page, we need to add a tab link in the
    sidebar to allow user to navigate between recently opened pages. When the page is not campaign,
    it can be settings page, profile page etc. So a page based system is needed. The system also
    need to support routing. It should be extensible such that adding new type of page is very easy.
    It should have a way to communicate with its content view when event happened, e.g. onRoute,
    onShow. This is important because, some UI in the page may need to re-render.

    Next is the filtering views. This also include searching. Views are normally bound with collections.
    Thus, changes made in either collection or view, should be reflected in one another. Filtering
    is tricky because it often involves API call. The collection/model needs to be in-sync with
    server, thus, if the server send filtered collection, the collection on the client side will
    lose some of the models. Luckily, Backbone.Paginator project solves this issue elegantly.
    Because of them, we can have a very powerful dashboard page that can filter through models
    without changing them.

    Another is the responsiveness. For any UI component, we have to think about how it's displayed
    on screens of different size. We have used Bootstrap Responsive utilities extensively. We
    specify different classes for components to control their visibility, width and position. 

    Data binding is also very challenging. App users often report bugs abot some views that are not
    updated after they change things. I have to wire events listeners precisely for each view
    object. This can be complex when models are inter-dependent. The problem of using Backbone View
    is that, I have to control the granularity of the view hierachy and re-render the most granular
    view on event change. It's so hard to know how granular it needs to be. When view hierachy grows
    big, things will break. This is why I bring in ReactJS. It can figure out the view rendering
    itself. All I need to do is to setup events in one place and render the whole React hierachy
    whenever it needs to. 

4. **Development complexity**  
    We have several deployment environemnts. For each environemnt, I have to generate different
    config and source code for it. For excample, the API endpoint has to be different for each one
    of them because different database is used. For production environemnt, I have to minify and
    uglify all the JavaScripts. This is something like applications written in C/C++, where you have
    to generate Application Binary that is ready to be executed by the OS. However, web development
    differs in that while in development we don't have to re-compile everything for every source
    change. We can have a development environemnt, such that a running watcher task constantly generate
    compiled file in a temporary folder. Note that this is different from deployed folder which is
    meant to be checked into source control and versioned. 

    There is a process involved in here. I use Jake Task to manage the process. So every time, I
    begin to develop code, I'll run `Jake` in the command line. It will start default task which is
    to grab development environment config and use `brunch` to compile and watch source code into a folder called
    `generated-public`. A local dev node server is runn to serve those compile assets files. In
    staging and production, the assets files are served using PHP scripts and pre-filtered by Apache
    server. 
    
    We use a CI tool called Strider on staging server to manage our deployment process. Essentially, it implements an API hook to respond to push event from GitHub. The API will run scripts written
    by me to compile, commit and push the tag to the GitHub. 

    Then on the production server, I just need to fetch git tags and checkout the version tag to
    complete the deployment. The tagged build is not merged into any git branch to prevent
    pollution.


#### There are things that we haven't had a solution yet.

##### Testing
Automation test for UI is always hard. I had attempted to write selenium tests, but quickly find it
hard to keep with the changes. If we can have one developer writing test full time, it will be much
reasonable. 

Instead of test on UI, test on models is a more feasible task. I can test model level things like,
validators, duration funcitons, data aggregators. I try to extract functions as much as
possible. I have a function module, where each function has no dependency. Testing those functions
is a pretty good idea. Sadly, I can't find any time to do it.  

##### Code reuse
Since our server side is written in NodeJS and client side uses commonJS system, sharing code with
both sides should be an easy task. However, we never really consider this option seriously. In my
opinion, the greater benefit of sharing code is to make things consistent. This is important to
software reliability.

#### To summarize

Things listed here are not complete. If I want to go into details, maybe I have to write another 2 or 3
articles of this length. I feel sometime, the problems I solve here is not as simple as I solved in
my previous jobs. It can be an engineering problem, it can also be a algorithm problem. Very often,
I need to have a comprehensive understanding on the protocols, systems or whatever before making a
decision. So exprience also plays a role here.

To me, learning new things and solving big problems are 2 most fulfilling things for doing project.
This project indeed taught me a lot. It's more than a web project. I am sure things I learned here
will be useful in the future, no matter what I do. 

