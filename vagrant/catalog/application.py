#!/usr/bin/env python

"""

Web Application for the Catalog Project

Uses applicationdb.py for Create/Read/Update/Delete functions.

"""

from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, make_response
from flask import session as login_session

from applicationdb import (show_categories, add_categories, remove_categories, show_items, add_items, remove_items)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import random, string, requests

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

import httplib2

import json

from build_db import Items, Categories, Users, Base

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

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
	if 'email' not in login_session:
		user_id = "no value"
	else:
		user_id = getUserID(login_session['email'])
	is_admin = getUserAdminAccess(user_id)
	return render_template('main.html', categories = cat, is_admin = is_admin)

""" Items Page / Displays items once the user clicks on a category """
@app.route('/categories/<int:categories_id>/', methods = ['GET','POST'])
def show_items(categories_id):
	print("Under construction... this will show items by category")
	cat = session.query(Categories).filter_by(id = categories_id).one()
	item = session.query(Items).filter_by(category_id = categories_id).all()
	if 'email' not in login_session:
		user_id = "no value"
	else:
		user_id = getUserID(login_session['email'])
	is_admin = getUserAdminAccess(user_id)
	return render_template('items.html', categories = cat, items = item, user_id = user_id, is_admin = is_admin)

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

# State token creation - taken from in-class examples
@app.route('/login/')
def show_login():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) 
					for x in xrange(32))
	login_session['state'] = state
	#return "session: %s" % login_session['state']
	return render_template('login.html', STATE = state)

# Google Connect
@app.route('/gconnect', methods = ['POST'])
def gconnect():
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	code = request.data

	try:
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope = '')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade auth code'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	
	# access token check
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response
	
	# verify token is for intended user
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps('Token id mismatch'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	
	# Verify token client id
	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps('Token Client ID mismatch'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	
	# Check if user already logged in
	stored_access_token = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_access_token is not None and gplus_id == stored_gplus_id:
		reponse = make_response(json.dumps('Already logged on'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	
	# Store access token in session for later use
	login_session['access_token'] = credentials.access_token
	login_session['gplus_id'] = gplus_id
	
	# Get user info
	user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(user_info_url, params = params)
	
	data = answer.json()
	
	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']
	
	# add provider
	login_session['provider'] = 'google'

	# check if user exists / prompt account creation
	user_id = getUserID(data["email"])
	if not user_id:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	output = ''
	output += '<h1> Hi, ' + login_session['username'] + '</h1>'
	output += '<img src="' + login_session['picture'] + 'style =  "width: 300px; height: 300px;">'
	flash("You are logged in as: %s" % login_session['username'])

	return output

@app.route('/logoff/')
def sign_out():

	access_token = login_session.get('access_token')

	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	login_session.clear()


	output = ''
	output += ' <h3> Signing Out, Please Wait </h3>'
	output += '<script>setTimeout(function(){'
	output += 'window.location.href="/categories";'
	output += '}, 4000);</script>'
	return output


def createUser(login_session):
    newUser = Users(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'], admin = False)
    
    session.add(newUser)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(Users).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except:
        return None

def getUserAdminAccess(userid):
	try:
		user = session.query(Users).filter_by(id = userid).one()
		if user.admin == True:
			return True
		else: 
			return False
	except:
		print("No user found")
		return False

if __name__ == '__main__':
	app.secret_key = 'in8_Zp8k5yLKpA-LUFJ0unNi'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)