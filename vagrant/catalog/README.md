# Item Catalog

## Udacity Fullstack Web Developer Nanodegree Project

By: Mike Boyer
Boyer.Mike.E@gmail.com
http://mikboy018.github.io / https://github.com/mikboy018

30 Jun 2018


## Background:
 
The goal of this assignment is to develop an application that provides a list of items within various categories as well as provide a user registration/authentication system. Registered users will be able to post, edit, and delete items.

Uses 'Bangers' Font from google - https://fonts.google.com/specimen/Bangers

## Requirements:

* Vagrant (See instructions below)
* [VirtualBox](https://www.virtualbox.org/ "VirtualBox")
* Chrome

## Instructions:

In order to run, complete the following steps:
1. Make sure Chrome is installed.
2. Retrieve from GitHub [here](https://github.com/mikboy018/fsnd-vagrant "Project on GitHub")
3. Setup Vagrant: [(instructions here)](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0 "Udacity Vagrant Instructions")
4. In the Command Terminal, build the database with `python build_db.py`
5. Populate the database with sample entries, and declare an admin with `python populate_db.py`, and enter name/email when prompted.
6. Launch the application with `python application.py`
7. In Chrome, Navigate to LocalHost:5000
8. Follow the links, be sure to log in to add items. In order to add categories (or remove ANY items), you must log in with the email used when running `python populate_db.py`


## Tables / Structure:

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


## Authentication / Registration:

This app will use authentication via Google plus. One person will be designated admin upon running `python populate_db.py` in step 5 of the instructions.

Registration will occur automatically if a new user tries to log in. If the user is not logged in, the user will see a login button in the header. Without logging in, they will be a guest, and have no permissions (outside of read functions). Once logged in, the user can add items to any category. Upon adding an item, they are the owner. Only owners or the admin may remove items. If the user is designated as 'Admin' they may remove/add any items/categories.

## JSON Info

For convenience, links to JSON info provided on each page. By design, no owner information is provided.




