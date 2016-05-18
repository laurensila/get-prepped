"""Disaster Prep/Awareness."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Territory, Disaster, connect_to_db, db
from sqlalchemy import func, orm


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    counties = ['candyland']

    # counties = Disaster.get_counties

    return render_template("homepage.html", counties=counties)

@app.route("/disaster_results")
def user_list():
    """Results of Disaster Query."""

    #do a slice on the dates so it cuts off the "time"
    #re-format date to read as MM-DD-YYYY

    return render_template("disaster_results.html")

@app.route('/sign-up', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("new_user_form.html")

@app.route('/signed-up', methods=['POST'])
def register_process():
    """Process Signup."""

    # Get form variables
    email = request.form["email"]
    name = request.form["name"]
    password = request.form["password"]
    territory = request.form["territory"]
    county = request.form["county"]

    new_user = User(name=name, email=email, password=password, territory=territory, county=county)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    return redirect("/profile/%s" % new_user.user_id)

@app.route("/profile/<int:user_id>")
def user_detail(user_id):
    """Show info about user."""

    user = User.query.get(user_id)
    return render_template("user_profile.html", user=user)

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

if __name__ == "__main__":
    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(debug=True)
