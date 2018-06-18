Item Catalog

Udacity Fullstack Web Developer Nanodegree Project

By: Mike Boyer
Boyer.Mike.E@gmail.com
http://mikboy018.github.io / https://github.com/mikboy018

18 Jun 2018


Background:

The goal of this assignment is to develop an application that provides a list of items within various categories as well as provide a user registration/authentication system. Registered users will be able to post, edit, and delete items.


Tables / Structure:


Table layout is as follows.

1. Items
2. Users
3. Categories


1. Items

Consists of:

	i. id (primary key)
	ii. Category (foreign key)
	iii. Name (text)
	iv. Description (text)
	v. Owner (foreign key)

2. Users

Consists of:

	i. id (primary key)
	ii. Name (text)
	iii. Login Email (text)
	iv. Admin (boolean)


3. Categories

Consists of:

	i. id (primary key)
	ii. Name (text)
	iii. Owner (foreign key), will be the admin


Authentication / Registration:

This app will use authentication via Google plus. One person (my account), will be designated admin.

Registration will occur separate from signing in. If there is no account, the user will see a register and login buttons in the navigation bar. Without registering (or logging in with a registered account), they will be a guest.




