#!/usr/bin/env python

"""

Web Application for the Catalog Project

Uses applicationdb.py for Create/Read/Update/Delete functions.

"""

from flask import Flask, flash, request, redirect, url_for, render_template, jsonify

from applicationdb import (show_categories, add_categories, remove_categories, show_items, add_items, remove_items)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from build_db import Items, Categories, Users, Base

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

""" Main Page / Displays Categories only"""
@app.route('/')
@app.route('/categories/')
def main():
	cat = session.query(Categories).all()
	print("Welcome to the main page!")
	return render_template('main.html', Categories = cat)

""" Items Page / Displays items once the user clicks on a category """
@app.route('/categories/<int:categories_id>/', methods = ['GET','POST'])
def show_items(categories_id):
	print("Under construction... this will show items by category")
	cat = session.query(Categories).filter_by(id = categories_id).one()
	item = session.query(Items).filter_by(category_id = categories_id).all()
	return render_template('items.html', categories = cat, items = item)

""" New Items Page / allows user to add new item, or go back to categories/id page """
@app.route('/categories/<int:categories_id>/new/', methods = ['GET', 'POST'])
def new_items():
	print("Under construction... this will allow a new item to be made")
	return "New Item"

""" Remove items page / allows user to confirm removing item, if they are the owner """
@app.route('/categories/<int:categories_id>/remove/<int:items_id>/',  methods = ['GET', 'POST'])
def remove_item():
	print("Under construction... this will allow the owner of an item to remove an item")
	return "Remove Item"

""" Add new categories / Admin only """
@app.route('/categories/new/',  methods = ['GET', 'POST'])
def new_category():
	print("Unders construction... admin will be able to add category from here")
	return "New Category"

""" Remove categoryies / Admin only """
@app.route('/categories/remove/<int:categories_id>/',  methods = ['GET', 'POST'])
def remove_category():
	print("Under construction... admin will be able to remove category from here")
	return "Remove Category"

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)