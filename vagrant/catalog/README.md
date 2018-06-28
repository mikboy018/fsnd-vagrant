Item Catalog

Udacity Fullstack Web Developer Nanodegree Project

By: Mike Boyer
Boyer.Mike.E@gmail.com
http://mikboy018.github.io / https://github.com/mikboy018

27 Jun 2018


Background:

The goal of this assignment is to develop an application that provides a list of items within various categories as well as provide a user registration/authentication system. Registered users will be able to post, edit, and delete items.

Uses 'Bangers' Font from google - https://fonts.google.com/specimen/Bangers

Instructions:

In order to run, complete the following steps:
1. 
2.
3.
4.
5.
6.


Tables / Structure:

Table layout is as follows.

1. Items
2. Users
3. Categories


1. Items

Consists of:

	i. id (primary key)
	ii. name (text)
	iii. description (text)
	iv. category_id (foreign key with categories table)
	v. owner_id (foreign key with users table)

2. Users

Consists of:

	i. id (primary key)
	ii. name (text)
	iii. email (text)
	iv. picture (text)
	iv. admin (boolean)


3. Categories

Consists of:

	i. id (primary key)
	ii. name (text)
	iii. owner_id (foreign key)


Authentication / Registration:

This app will use authentication via Google plus. One person (my account), will be designated admin. If you would like to change the admin, enter the desired credentials in populated_db.py, with admin = True.

Registration will occur automatically if a new user tries to log in. If there is no account, the user will see a login button in the header. Without logging in, they will be a guest, and have no permissions (outside of read functions).




