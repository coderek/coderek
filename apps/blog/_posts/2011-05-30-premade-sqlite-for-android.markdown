---
layout: post
title: "premade sqlite for android"
date: 2011-05-30 11:00 +0800
comments: true
categories: android
---

reference: [http://www.reigndesign.com/blog/using-your-own-sqlite-database-in-android-applications/](http://www.reigndesign.com/blog/using-your-own-sqlite-database-in-android-applications/)

我的项目里需要做一个数据库储存很多节点信息。显然如果在runtime的时候从原始数据文件载入到数据库会相当耗时，我采取的方法是事先在电脑上生成一个.db的sqlite数据库文件，然后在拷贝到android 项目里面。具体做法如下：



1. 使用 sqlite database browser 创建数据库及表。

2. 创建表的时候需要有一列_id，可以创建一列或者把原有的primary key改名。这是android对数据库的要求，因为它自己的content provider需要用到这个。

3. 生成 android_metadata 表， 这个表让这个数据库被android 识别
```
   CREATE TABLE “android_metadata” (“locale” TEXT DEFAULT ‘en_US’)
   INSERT INTO “android_metadata” VALUES (‘en_US’)    保存。
```

4. 拷贝生成的.db数据库文件到项目的asset 文件夹下， 建立databaseHelper：
注意：your_package 需要是以com.xxx.xxx的形式， DB_NAME需要是xxx.db的形式。

{% include_code android_sqlite.java %}

5. 在项目activity里测试：

```
DataBaseHelper myDbHelper = new DataBaseHelper();
myDbHelper = new DataBaseHelper(this);

try {
  myDbHelper.createDataBase();
} catch (IOException ioe) {
  throw new Error(“Unable to create database”);
}

try {
  myDbHelper.openDataBase();
}catch(SQLException sqle){
  throw sqle;
}
```
