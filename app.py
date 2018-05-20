import json
import math
import random
import string
from datetime import datetime

import httplib2
import requests
import time
from flask import Flask, render_template, request, flash, redirect, url_for, make_response
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker, scoped_session

from database_setup import Base, Category, Item, User

# Flask Init
app = Flask(__name__)
app.secret_key = "SECRET_KEY"
app.debug = True

# SqlAlchemy Init
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
session = scoped_session(sessionmaker(bind=engine))

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']

user: User = None


@app.route('/login')
def showLogin():
    updateUser()
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, user=user)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State Parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 501)
        response.headers['Content-Type'] = 'application/json'

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

    login_session['credentials'] = credentials.to_json()
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    updateUser()

    flash("<big>You are now logged in as {}</big>".format(login_session['username']))
    return redirect(url_for('displayCatalog'))


def updateUser():
    global user
    try:
        user = session.query(User).filter_by(name=login_session['username']).one()
    except:
        user = User(name="Please Log In", picture=url_for('static', filename="img/profile.png"))


@app.route('/gdisconnect')
def gdisconnect():
    try:
        credentials = json.loads(login_session.get('credentials'))
    except:
        flash("An Error Occured.")
        return redirect(url_for('displayCatalog'))

    access_token = credentials['access_token']
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    # print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % credentials['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        # del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['credentials']
        global user
        user = None
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/', methods=['GET', 'POST'])
@app.route('/catalog', methods=['GET', 'POST'])
def displayCatalog():
    if request.method == 'GET':
        categories = session.query(Category).order_by(asc(Category.name))
        return render_template('catalog.html', categories=categories)

    elif request.method == 'POST':
        global user
        if user is not None:
            if login_session.get('credentials') is not None:
                category_name = request.form['name']
                if request.form['picuri']:
                    picuri = request.form['picuri']
                else:
                    picuri = url_for('static', filename='img/athlete-beach-bodybuilder-305239.jpg')
                session.add(Category(name=category_name, picture=picuri, user=user))
                session.commit()
                return redirect(url_for('displayCatalog'))
            else:
                flash("<big>Bummer! There's authentication error. Please try refreshing/logging in again.</big>")
                return redirect(url_for('displayCatalog'))
        else:
            flash(
                "<strong class='flash-message'>You are currently unauthorized to do this. Please <a href='{}'>sign in</a> to continue.</strong>".format(
                    url_for('showLogin')))
            return redirect(url_for('displayCatalog'))


@app.route('/catalog/<string:catalog_name>/', methods=['GET', 'POST'])
def displayCategoryContents(catalog_name):
    if request.method == 'POST':
        global user
        if user is not None:
            newItem = Item(
                creationtime=datetime.now(),
                category=session.query(Category).filter_by(name=catalog_name).one(),
                user=user)
            if request.form['name']:
                newItem.name = request.form['name']
            else:
                return

            if request.form['description']:
                newItem.description = request.form['description']
            else:
                newItem.description = "No description provided."

            if request.form['picuri']:
                newItem.picture = request.form['picuri']
            else:
                newItem.picture = url_for('static', filename='img/athlete-beach-bodybuilder-305239.jpg')

            session.add(newItem)
            session.commit()
            flash("Item {} created.".format(newItem.name))
        else:
            flash(
                "<strong class='flash-message'>You are currently unauthorized to do this. Please <a href='{}'>sign in</a> to continue.</strong>".format(
                    url_for('showLogin')))
        return redirect(url_for('displayCategoryContents', catalog_name=catalog_name))

    else:
        category = session.query(Category).filter_by(name=catalog_name).one()
        items = session.query(Item).filter_by(category=category)
        return render_template('itemslist.html', items=items, catalog_name=catalog_name)


@app.route('/catalog/<string:catalog_name>/<string:item_name>/', methods=['GET', 'POST'])
def displayItemDetails(catalog_name, item_name):
    if request.method == 'POST':
        if user is not None:
            editedItem: Item = session.query(Item).filter_by(name=item_name).one()
            if request.form['name']:
                editedItem.name = request.form['name']
            if request.form['description']:
                editedItem.description = request.form['description']
            if request.form['category']:
                category = session.query(Category).filter_by(id=request.form['category']).one()
                editedItem.category = category
            session.add(editedItem)
            session.commit()
            # flash('Menu Item Successfully Edited')
            return redirect(url_for('displayCategoryContents', catalog_name=catalog_name))
        else:
            flash("<big>Authentication error occurred. Try refreshing the page/logging in again.</big>")
            return redirect(url_for('displayCategoryContents', catalog_name=catalog_name))

    else:
        # Categories needed for editing the item details and displaying in drop down menu
        categories = session.query(Category).all()
        catalog = session.query(Category).filter_by(name=catalog_name).one()
        item = session.query(Item).filter_by(name=item_name, category=catalog).one()
        itemslist = session.query(Item).filter_by(category=catalog)
        return render_template('itemdetail.html', categories=categories, category=catalog, current_item=item,
                               items=itemslist)


@app.route('/<string:category_name>/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    if request.method == 'POST':
        if user is not None:
            category = session.query(Category).filter_by(name=category_name).one()
            session.delete(session.query(Item).filter_by(name=item_name, category=category).one())
            session.commit()
        else:
            flash(
                "<strong class='flash-message'>You are currently unauthorized to do this. Please <a href='{}'>sign in</a> to continue.</strong>".format(
                    url_for('showLogin')))
        return redirect(url_for('displayCatalog'))
    else:
        return "Sorry! We don't accept 'GET' requests. :/"


@app.route('/recents/')
def displayRecents():
    categories = session.query(Category).order_by(asc(Category.name))
    recents = session.query(Item).order_by(desc(Item.creationtime))
    return render_template('recent.html', categories=categories, recents=recents, current_time=datetime.now())


def calculateTimeElapsed(creation_time):
    return int(math.floor(time.time() - creation_time.timestamp()))


# Set this function as global to use in Jinja Template
app.jinja_env.globals.update(calculate_elapsed_time=calculateTimeElapsed)

if __name__ == '__main__':
    app.run(debug=False)
