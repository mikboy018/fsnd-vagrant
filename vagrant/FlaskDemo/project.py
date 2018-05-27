from flask import Flask, render_template, request, redirect, url_for, flash, jsonify # import flask libraries
app = Flask(__name__) # create instance of this app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False}) # add connect args to alleviate ProgrammingError
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Make an API Endpoint (GET Request) - all items by restaurant id
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def RestaurantInfoJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in items])

# Make an API Endpoint (GET Request) - list item by restaurant & menu ids
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def MenuItemInfoJSON(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItems=[items.serialize])

@app.route('/') # decorators to determine code based on route
@app.route('/restaurants')
def ListRestaurants():
    restaurant = session.query(Restaurant).all()
    for r in restaurant:
        items = session.query(MenuItem).filter_by(restaurant_id = r.id)
    return render_template('menu.html', restaurant = r, items = items) # only returns last entry

@app.route('/restaurants/<int:restaurant_id>/')
def RestaurantInfo(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurants/<int:restaurant_id>/newitems', methods=['GET', 'POST'])
def NewMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New Item Created: " + newItem.name)
        return redirect(url_for('RestaurantInfo', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edititem', methods=['GET', 'POST'])
def EditMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    oldname = item.name
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        session.add(item)
        session.commit()
        flash("Item " + oldname + " updated to " + item.name)
        return redirect(url_for('RestaurantInfo', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = item)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/deleteitem', methods=['GET', 'POST'])
def DeleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['button']:
            session.delete(item)
            session.commit()
            flash("Removed " + item.name)
            return redirect(url_for('RestaurantInfo', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = item)


if __name__ == '__main__':  #  other files will be 'name'
    app.secret_key = '12345' # should be a secret password, entering luggage combo instead, for flash messages
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000) # tells vagrant to listen on all public IP add