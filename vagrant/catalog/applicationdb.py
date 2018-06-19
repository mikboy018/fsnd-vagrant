""" 

Application database helper.

Contains functions to Create/Read/Update/Delete Items/Users/Categories from catalog.db


"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from build_db import Items, Categories, Users, Base

# Create session, connect to DB

engine = create_engine('sqlite:///catalog.db')
DBSession  = sessionmaker(bind = engine)
session = DBSession()

def show_categories()

	print("Show all categories --- Main Page")

def add_categories(int admin_id)

	print("Add a category, if admin user")

def remove_categories()

	print("Remove selected category, if admin user")

def show_items(int category_id):

	print("Show items")

def add_items(int category_id):

	print("Add items")

def remove_items(int category_id, int item_id)

	print("Remove selected item")

