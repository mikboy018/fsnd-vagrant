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

engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

""" Main Page / Displays Categories only"""
@app.route('/')
@app.route('/categories/')
def main():
	cat = session.query(Categories).all()
	print("Welcome to the main page!")
	return render_template('main.html', categories = cat)

""" Items Page / Displays items once the user clicks on a category """
@app.route('/categories/<int:categories_id>/', methods = ['GET','POST'])
def show_items(categories_id):
	print("Under construction... this will show items by category")
	cat = session.query(Categories).filter_by(id = categories_id).one()
	item = session.query(Items).filter_by(category_id = categories_id).all()
	return render_template('items.html', categories = cat, items = item)

""" New Items Page / allows user to add new item, or go back to categories/id page """
@app.route('/categories/<int:categories_id>/new/', methods = ['GET', 'POST'])
def new_items(categories_id):
	print("Under construction... this will allow a new item to be made")
	cat = session.query(Categories).filter_by(id = categories_id).one()
	return render_template('new_cat_item.html', category = cat)

@app.route('/categories/<int:categories_id>/new/confirmed/', methods = ['GET', 'POST'])
def new_itm(categories_id):
	if request.method == 'POST':
		cat = session.query(Categories).filter_by(id = categories_id).one()
		user = session.query(Users).one()
		item_name = request.form['item_name']
		item_desc = request.form['item_desc']
		print("adding " + item_name + " to " + cat.name)
		new_item = Items(name = item_name, description = item_desc, owners = user, category = cat)

		session.add(new_item)
		session.commit()
		cat = session.query(Categories).all()
		return render_template('main.html', categories = cat)
	else:
		Print("Something else happened... returning to main page")
		return render_template('main.html', categories = cat)

""" Remove items page / allows user to confirm removing item, if they are the owner """
@app.route('/categories/<int:categories_id>/remove/<int:items_id>/',  methods = ['GET', 'POST'])
def remove_item(categories_id, items_id):
	print("Under construction... this will allow the owner of an item to remove an item")
	cat = session.query(Categories).filter_by(id = categories_id).one()
	itm = session.query(Items).filter_by(id = items_id).one()
	return render_template('remove_items.html', categories = cat, item = itm)

@app.route('/categories/<int:categories_id>/remove/<int:items_id>/confirm/',  methods = ['GET', 'POST'])
def remove_itm(categories_id, items_id):

	cat = session.query(Categories).filter_by(id = categories_id).one()
	itm = session.query(Items).filter_by(id = items_id).one()
	print("removing " + itm.name + " from " + cat.name)
	
	session.delete(itm)
	session.commit()
	
	cat = session.query(Categories).all()
	return render_template('main.html', categories = cat)
	

""" Add new categories / Admin only """
@app.route('/categories/new/',  methods = ['GET', 'POST'])
def new_category():
	print("Unders construction... admin will be able to add category from here")
	return render_template('new_cat.html')

@app.route('/categories/new/confirmed/', methods = ['GET', 'POST'])
def new_cat():
	if request.method == 'POST':
		
		cat_name = request.form['category_name']
		print("adding: " + cat_name + " to categories")
		user = session.query(Users).one()
		category = Categories(name = cat_name, owner = user)

		session.add(category)
		session.commit()
		cat = session.query(Categories).all()
		return render_template('main.html', categories = cat)
	else:
		return render_template('new_cat.html')

""" Remove categoryies / Admin only """
@app.route('/categories/remove/<int:categories_id>/',  methods = ['GET', 'POST'])
def remove_category(categories_id):
	print("Under construction... admin will be able to remove category from here")
	cat = session.query(Categories).filter_by(id = categories_id).one()
	return render_template('remove.html', categories = cat)

@app.route('/categories/remove/<int:categories_id>/confirmed/', methods = ['GET','POST'])
def remove(categories_id):
	cat = session.query(Categories).filter_by(id = categories_id).one()
	print("removing - " + cat.name)
	session.delete(cat)
	session.commit()
	cat_list = session.query(Categories).all()
	return render_template('main.html', categories = cat_list)

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)