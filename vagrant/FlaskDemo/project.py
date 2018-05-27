from flask import Flask # import flask libraries
app = Flask(__name__) # create instance of this app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False}) # add connect args to alleviate ProgrammingError
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/') # decorators to determine code based on route
@app.route('/restaurants')
def ListRestaurants():
    restaurants = session.query(Restaurant).all()
    output = ''
    for r in restaurants:
        output += r.name
        output += '<br /><br /'
        items = session.query(MenuItem).filter_by(restaurant_id = r.id)
        for i in items:
            output += '  - ' + i.name + ': ' + i.price
            output += '<br />'
        output += '<br/>'
    return output

@app.route('/restaurants/<int:restaurant_id>/')
def RestaurantInfo(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    output = ''
    output += restaurant.name
    for i in items:
        output += ' - ' + i.name + ': ' + i.price + '<br />'
        output += i.description
        output += '<br />'
    return output

@app.route('/restaurants/<int:restaurant_id>/newitems')
def NewMenuItem(restaurant_id):
    return 'Placeholder: create new menu item'

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edititem')
def EditMenuItem(restaurant_id, menu_id):
    return 'Placeholder: edit menu items'


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/deleteitem')
def DeleteMenuItem(restaurant_id, menu_id):
    return 'Placeholder: delte menu items'


if __name__ == '__main__':  #  other files will be 'name'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000) # tells vagrant to listen on all public IP add