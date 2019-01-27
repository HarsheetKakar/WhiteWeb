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

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

db.create_all()
hash= Bcrypt(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
    #use flask login manager instead of this
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    user= current_user
    return render_template('pages/placeholder.home.html',user=user)


@app.route('/about')
def about():
    user=current_user
    return render_template('pages/placeholder.about.html', user=user)


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
