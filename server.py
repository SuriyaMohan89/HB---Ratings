"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, url_for)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/users/<int:user_id>")
def user_info(user_id):
    """Show user information."""

    user = User.query.get(user_id)

    return render_template("user_info.html", user=user)


@app.route("/register", methods=["GET"])
def register_form():
    """Show user registration form."""

    return render_template("register_form.html")

@app.route("/register", methods=["POST"])
def register_process():
    """Process user registration form."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not User.query.filter(User.email == email).first():
        user = User(email=email, password=password)

        db.session.add(user)
        db.session.commit()
        flash("Successfully Registered")

    else:
        flash("Email already registered. Please Login")

    return redirect('/')


@app.route('/login',methods=["GET"])
def login_form():
    """Show Login page"""

    return render_template("login_form.html")


@app.route('/login',methods = ["POST"])
def login_process():
    """Processes user Login form"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter((User.email == email) & (User.password == password)).first()

    if user:
        session["user_id"] = user.user_id
        flash("Successfully logged in!")

        return redirect(url_for('user_info', user_id=user.user_id))

    else:
        flash("Login details incorrect!")

        return redirect('/login')


@app.route('/logout')
def logout():
    """Log out the user."""

    session.pop("user_id", None)
    flash("You've been logged out!")
    
    return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
