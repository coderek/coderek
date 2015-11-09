---
layout: post
title: "styling in android"
date: 2013-02-11 09:46 +0800
comments: true
categories: android
---

Android Development team tries to make styling applications as easy as styling a web page. We can change the look and feel of every element within the application. For example, the background of textbox, the background of action bar, or the shape of a button. The android styling also has the feature of heirachical inheritance of styles. If the application use one style, while the activity use another, the activity's will overwrite the applications. This rule applies up to every view group and single element. This allows easy reuse of styles. The developer only needs to overwrite the style needed. 



The major source of reference about styling is at [here](http://developer.android.com/guide/topics/ui/themes.html). But it doesn't give out a detail documentation on which style applies to which element. Instead, it only gives two system styling files that contains whole bunch of xmls for major system styles, that is holo and holo white. The links is [styles.xml](https://android.googlesource.com/platform/frameworks/base/+/refs/heads/master/core/res/res/values/styles.xml) and [themes.xml](https://android.googlesource.com/platform/frameworks/base/+/refs/heads/master/core/res/res/values/themes.xml). I need to dig into the lines and try out several styles before I can find the one needed. Though it's a bit troublesome, but it's not difficult at all.  



My current task is to style the action bar as well as the tab bar. Basically, I want:

* make action bar background green
* make tab bar background black
* make tab bar underliner green

Here is the effect. 

![Styling ActionBar](/images/styling_actionbar.png)

Because I want the most of my background to be dark, thus, the first thing I do is to set the Holo theme through out the applications. Normally, I can just use Holo Theme by configuring it as my application theme. But in order to easily inherit the default theme. I define application style of my own which inherit the Holo theme: 

```xml
<!-- styles.xml -->
<style name="store" parent="@android:style/Theme.Holo">
</style>

<!-- set theme for the application in AndroidManifest.xml -->
<application android:theme="@style/store" >

```

After setting the base style, I need to set the sub-style for the activity. This is the tabbed activity I want to style. There may be other activities in the same application that having different sub-style. But all of them should inherit from the `store` style.

```xml
<!-- for tabbed activity -->
<style name="store.main">
    <item name="android:actionBarStyle">@style/store_actionbar</item>
    <item name="android:actionBarTabStyle">@style/store_tabView</item>
</style>

<!-- set theme for activity in AndroidManifest.xml -->
<activity android:theme="@style/store.main" >
</activity>
```

Here I use `store.main` to indicate that I want to inherit `store` style. Thus, it also inherit `Theme.Holo`. Then, I have 2 items inside the style which is responsible for overwriting the action bar and tabs' style.

I have to define these two myself. But I don't know what attributes I should overwrite. By looking through the [theme.xml](https://android.googlesource.com/platform/frameworks/base/+/refs/heads/master/core/res/res/values/themes.xml) and [styles.xml](https://android.googlesource.com/platform/frameworks/base/+/refs/heads/master/core/res/res/values/styles.xml), I found the default definition for the two. 

- To overwrite the background color of action bar, I just need to inherit the `@android:style/Widget.Holo.ActionBar` and set the `android:background` to my color.

- To overwrite the background color of action bar tabs, I need to inherit the `@android:style/Widget.Holo.ActionBar.TabView` and set the `android:background` to my color. 

The first one is easy, just define a color in `colors.xml` and use that color, done. The second one is a bit tricky. 

Since, the tab bar is button, it has at least two states, in which different backgrounds are displayed. How to achieve this using one `android:background` attribute? 

By digging the source xmls in SDK, it turns out that I need to define a drawable that has different layers using xml. 

```xml

<!-- /res/drawable/tab_indicator.xml -->

<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android" >
    <!-- Non focused states -->
    <item android:state_focused="false" android:state_selected="false" android:state_pressed="false" android:drawable="@drawable/tab_unselected_holo" />
    <item android:state_focused="false" android:state_selected="true"  android:state_pressed="false" android:drawable="@drawable/tab_selected_holo" />

    <!-- Focused states -->
    <item android:state_focused="true" android:state_selected="false" android:state_pressed="false" android:drawable="@drawable/tab_unselected_holo" />
    <item android:state_focused="true" android:state_selected="true"  android:state_pressed="false" android:drawable="@drawable/tab_selected_holo" />

    <!-- Pressed -->
    <!--    Non focused states -->
    <item android:state_focused="false" android:state_selected="false" android:state_pressed="true" android:drawable="@drawable/tab_unselected_holo" />
    <item android:state_focused="false" android:state_selected="true"  android:state_pressed="true" android:drawable="@drawable/tab_selected_holo" />

    <!--    Focused states -->
    <item android:state_focused="true" android:state_selected="false" android:state_pressed="true" android:drawable="@drawable/tab_unselected_holo" />
    <item android:state_focused="true" android:state_selected="true"  android:state_pressed="true" android:drawable="@drawable/tab_selected_holo" />

</selector>
```
This is adapted from the `<android-sdk>/platforms/android-14/data/res/drawable/tab_indicator_holo.xml` . To make it easy, instead of 4 states, I just use 2 images to define 2 states. Then in the `tab_unselected_holo` drawable, I define like this,  

```xml
<!-- /res/drawable/tab_unselected_holo.xml -->
<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android" >
    <!-- Bottom Line -->
    <item>
        <shape android:shape="rectangle">
            <solid android:color="@android:color/holo_green_dark" />
        </shape>
    </item>

    <!-- Tab color -->
    <item android:bottom="2dip">
        <shape android:shape="rectangle">
            <solid android:color="@color/background_holo_dark" />
        </shape>
    </item>
</layer-list>
```

Basically, this is a layered images consisting a green background with full height and a dark foreground with full height minus 2 dip.

Similarly for the `tab_selected_holo`, just need to make the foreground shorter.  Done.

This is something new to me as I never know xml can define drawables like this. 

Andriod's philosophy of design is similar to that of web programming nowadays. As I also do Rails and Backbone, I can see their similarities in both styling and layouts. The idea is to try to reuse most of the codes and segregate layout into sections for responsiveness. I like this approch very much, that's why I see the better future for android instead of rigidly controlled iOS.



