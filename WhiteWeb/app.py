#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, redirect, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
from WhiteWeb.forms import LoginForm, RegisterForm
from WhiteWeb.models import User, load_user
import os
from WhiteWeb import app, db
from flask_login import login_user,login_required,logout_user, current_user
from flask_bcrypt import Bcrypt
import pyrebase #library to access firebase

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

db.create_all()
hash= Bcrypt(app)

firebase_config = {                                      #api configurations
    'apiKey': "AIzaSyDGwptgJRet0hxRzER2J_ws9gqAXOQZ3f4",
    'authDomain': "whiteweb-2ca0e.firebaseapp.com",
    'databaseURL': "https://whiteweb-2ca0e.firebaseio.com",
    'projectId': "whiteweb-2ca0e",
    'storageBucket': "whiteweb-2ca0e.appspot.com",
    'messagingSenderId': "98773813262"
}

firebase = pyrebase.initialize_app(firebase_config) #firebase handler

firebase_db = firebase.database() #firebase database handler


@app.route('/')
def home():
    user = current_user
    return render_template('pages/placeholder.home.html',user = user)

@app.route('/reports')
@login_required
def reports():
    user = current_user
    drivers = firebase_db.child("DriversInformation").get().val()
    return render_template('pages/reports.html',drivers = drivers, user = user)

@app.route('/about')
def about():
    user = current_user
    return render_template('pages/placeholder.about.html', user=user)

@app.route('/victims')
@login_required
def victims():
    user = current_user
    victims = firebase_db.child("RidersInformation").get().val() #will change RidersInformation to VictimsInformation
    return render_template('pages/victims.html', user = user, victims = victims)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if(form.is_submitted()):
        user = User.query.filter_by(name= form.name.data).first()
        if(user.check_password(form.password.data)):
            login_user(user)
            next= request.args.get('next')
            print(next)
            if next == None or not next[0]=='/':
                next = url_for('home')
            return redirect(next)

    return render_template('forms/login.html', form=form)

@app.route('/map')
@login_required
def map():
    user = current_user
    drivers = firebase_db.child('Drivers').get().val()
    driver_locations_lat = []
    driver_locations_lng = []
    for i in drivers:
        driver_locations_lat.append(drivers[i]['l'][0])
        driver_locations_lng.append(drivers[i]['l'][1])
    print(driver_locations_lat,driver_locations_lng)
    return render_template('pages/map.html',
                           user = user,
                            driver_locations_lat=driver_locations_lat,
                            driver_locations_lng=driver_locations_lng,
                            length = len(drivers))

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    print(form.email.data)
    if(form.is_submitted()): #form.validate_on_submit() always returning false, even without any FlaskForm validators
        print(form.validate_on_submit())
        user= User(name = form.name.data, password = hash.generate_password_hash(form.password.data), email = form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('forms/register.html', form=form)


"""
@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)
"""
# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

@app.route('/logged_out')
@login_required
def logout():
    print("logged out")
    logout_user()
    return redirect(url_for('login'))

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
