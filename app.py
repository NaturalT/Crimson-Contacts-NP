import os
import math
import datetime
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from help import apology, login_required, geocode
#db.execute("CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'name' TEXT NOT NULL, 'username' TEXT NOT NULL, 'hash' TEXT NOT NULL, 'lat' DECIMAL UNSIGNED NOT NULL, 'long' DECIMAL UNSIGNED NOT NULL, 'status' TEXT DEFAULT 'Healthy')")

def easy_indexer(string):
        if string == 'id' :
            return 0
        elif string == 'name':
            return 1
        elif string == 'username':
            return 2
        elif string == 'hash':
            return 3
        elif string == 'lat':
            return 4
        elif string == 'long':
            return 5
        elif string == 'status':
            return 6

# Configure application
app = Flask('app')
app.secret_key = b'heyyyyyyyyy'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Configure CS50 Library to use SQLite database
db = sqlite3.connect("users.db", check_same_thread=False)
# db = da.cursor()
# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def home():

  # queries to determine risk variables
    userdetails = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))

    userdetails= userdetails.fetchall()
    infected = db.execute("SELECT * FROM users WHERE status = 'Infected' AND lat = ? AND long = ? EXCEPT SELECT * FROM users where id = ?" ,  (userdetails[0][easy_indexer('lat')], userdetails[0][easy_indexer('long')], session["user_id"]) )
    infected = infected.fetchall()
    modrisk = db.execute("SELECT * FROM users WHERE status = 'High Risk' AND lat = ? AND long = ? EXCEPT SELECT * FROM users where id = ?" ,  (userdetails[0][easy_indexer('lat')], userdetails[0][easy_indexer('long')], session["user_id"]) )
    modrisk = modrisk.fetchall()
    minorrisk = db.execute("SELECT * FROM users WHERE status = 'Minor Risk' AND lat = ? AND long = ? EXCEPT SELECT * FROM users where id = ?",(userdetails[0][easy_indexer('lat')], userdetails[0][easy_indexer('long')], session["user_id"] ) )
    minorrisk = minorrisk.fetchall()



    # determine environmental risk based on number of individuals in your vicinity of different risk rankings
    if len(infected) >= 1:
        envrisk = 'High'
    elif len(modrisk) >= 1:
        envrisk = 'Moderate'
    elif len(minorrisk) >= 1:
        envrisk = 'Minor'
    else:
        envrisk = 'Low'

    # logic to determine user risk level
    if userdetails[0][easy_indexer('status')] == 'Infected':
        personalstatus = 'Infected'
    elif userdetails[0][easy_indexer('status')] == 'High Risk':
        personalstatus = 'High Risk'
    elif userdetails[0][easy_indexer('status')] == 'Minor Risk':
        personalstatus = 'Minor Risk'
    else:
        personalstatus = 'Healthy'

    name = userdetails[0][easy_indexer('name')]
    contacts = db.execute("SELECT * FROM logs WHERE date IN (SELECT date FROM logs WHERE user_id = ?) AND lat IN (SELECT lat FROM logs WHERE user_id = ?) AND long IN (SELECT long FROM logs WHERE user_id = ?) EXCEPT SELECT * FROM logs WHERE date = ? EXCEPT SELECT * FROM logs WHERE user_id = ?"
    , (session["user_id"], session["user_id"], session["user_id"], '', session["user_id"]))

    return render_template("home.html", envrisk = envrisk, personalstatus = personalstatus, contacts = contacts, name=name)








# route for surveys
@app.route("/survey", methods=["GET", "POST"])
@login_required
def survey():
    if request.method == "POST":

        if request.form['test'] == 'Infected':
            db.execute("UPDATE users SET status = ? WHERE id = ?", (request.form['test'], session["user_id"]))
            db.commit()
            ct = datetime.datetime.now()

            #insert interaction into logs
            db.execute("INSERT INTO logs (user_id, activity, datetime, status) VALUES( ?, ?, ?, ?)", (session["user_id"], 'survey', ct, request.form['test'] ))
            db.commit()

            if  geocode(request.form['address1']) != None:

                #call API to receive coordinate information
                coordinates = geocode(request.form['address1'])
                db.execute("INSERT INTO logs (user_id, activity, date, status, lat, long) VALUES( ?, ?, ?, ?, ?, ?)", (session["user_id"], 'travel', request.form['date1'], request.form['test'], coordinates['lat'], coordinates['lon']))
                db.commit()

            if geocode(request.form['address2']) != None:

                #call API to receive coordinate information
                coordinates = geocode(request.form['address2'])
                db.execute("INSERT INTO logs (user_id, activity, date, status, lat, long) VALUES( ?, ?, ?, ?, ?, ?)", (session["user_id"], 'travel', request.form['date2'], request.form['test'], coordinates['lat'], coordinates['lon']))
                db.commit()

            if geocode(request.form['address3']) != None:


                #call API to receive coordinate information
                coordinates = geocode(request.form['address3'])
                db.execute("INSERT INTO logs (user_id, activity, date, status, lat, long) VALUES( ?, ?, ?, ?, ?, ?)", (session["user_id"], 'travel', request.form['date3'], request.form['test'], coordinates['lat'], coordinates['lon']))
                db.commit()

            return redirect('/')

        else:
            # set user status to response given on form
            db.execute("UPDATE users SET status = ? WHERE id = ?", (request.form['status'], session["user_id"]))
            db.commit()
            ct = datetime.datetime.now()

            #insert interaction into logs
            db.execute("INSERT INTO logs (user_id, activity, datetime, status) VALUES( ?, ?, ?, ?)", (session["user_id"], 'survey', ct, request.form['status'] ))
            db.commit()

            if geocode(request.form['address1']) != None:

                #call API to receive coordinate information
                coordinates = geocode(request.form['address1'])
                db.execute("INSERT INTO logs (user_id, activity, date, status, lat, long) VALUES( ?, ?, ?, ?, ?, ?)", (session["user_id"], 'travel', request.form['date1'], request.form['status'], coordinates['lat'], coordinates['lon']))
                db.commit()

            if geocode(request.form['address2']) != None:


                #call API to receive coordinate information
                coordinates = geocode(request.form['address2'])
                db.execute("INSERT INTO logs (user_id, activity, date, status, lat, long) VALUES( ?, ?, ?, ?, ?, ?)", (session["user_id"], 'travel', request.form['date2'], request.form['status'], coordinates['lat'], coordinates['lon']))
                db.commit()

            if geocode(request.form['address3']) != None:

                #call API to receive coordinate information
                coordinates = geocode(request.form['address3'])
                db.execute("INSERT INTO logs (user_id, activity, date, status, lat, long) VALUES( ?, ?, ?, ?, ?, ?)", (session["user_id"], 'travel', request.form['date3'], request.form['status'], coordinates['lat'], coordinates['lon']))
                db.commit()

            return redirect('/')



    else:
        # set user status to response given on form
        status = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
        status = status.fetchall()
        if status[0][easy_indexer('status')] != 'Infected':
            return render_template("Survey.html")
        else:
            return render_template("Survey2.html")

# second survey route
@app.route("/survey2", methods=["GET", "POST"])
@login_required
def survey2():
    if request.method == "POST":

        if request.form['recovery'] == 'Infected':
            db.execute("UPDATE users SET status = ? WHERE id = ?", ( request.form['recovery'], session["user_id"]))
            db.commit()
            ct = datetime.datetime.now()

            #insert interaction into logs
            db.execute("INSERT INTO logs (user_id, activity, datetime, status) VALUES( ?, ?, ?, ?)",( session["user_id"], 'survey', ct, request.form['recovery'] ))
            db.commit()

            if geocode(request.form['address1']) != None:

                #call API to receive coordinate information
                coordinates = geocode(request.form['address1'])
                db.execute("INSERT INTO logs (user_id, activity, date, status, lat, long) VALUES( ?, ?, ?, ?, ?, ?)",( session["user_id"], 'travel', request.form['date1'], request.form['recovery'], coordinates['lat'], coordinates['lon']))
                db.commit()

            if geocode(request.form['address2']) != None:


                #call API to receive coordinate information
                coordinates = geocode(request.form['address2'])
                db.execute("INSERT INTO logs (user_id, activity, date, status, lat, long) VALUES( ?, ?, ?, ?, ?, ?)", (session["user_id"], 'travel', request.form['date2'], request.form['recovery'], coordinates['lat'], coordinates['lon']))
                db.commit()

            if geocode(request.form['address3']) != None:

                #call API to receive coordinate information
                coordinates = geocode(request.form['address3'])
                db.execute("INSERT INTO logs (user_id, activity, date, status, lat, long) VALUES( ?, ?, ?, ?, ?, ?)", (session["user_id"], 'travel', request.form['date3'], request.form['recovery'], coordinates['lat'], coordinates['lon']))
                db.commit()

            return redirect('/')
        else:
            db.execute("UPDATE users SET status = ? WHERE id = ?",( request.form['recovery'], session["user_id"]))
            db.commit()
            ct = datetime.datetime.now()

            #insert interaction into logs
            db.execute("INSERT INTO logs (user_id, activity, datetime, status) VALUES( ?, ?, ?, ?)", (session["user_id"], 'survey', ct, request.form['recovery'] ))
            db.commit()

            if geocode(request.form['address1']) != None:

                #call API to receive coordinate information
                coordinates = geocode(request.form['address1'])
                db.execute("INSERT INTO logs (user_id, activity, date, status, lat, long) VALUES( ?, ?, ?, ?, ?, ?)", (session["user_id"], 'travel', request.form['date1'], request.form['recovery'], coordinates['lat'], coordinates['lon']))
                db.commit()

            if geocode(request.form['address2']) != None:


                #call API to receive coordinate information
                coordinates = geocode(request.form['address2'])
                db.execute("INSERT INTO logs (user_id, activity, date, status, lat, long) VALUES( ?, ?, ?, ?, ?, ?)", (session["user_id"], 'travel', request.form['date2'], request.form['recovery'], coordinates['lat'], coordinates['lon']))
                db.commit()

            if geocode(request.form['address3']) != None:

                #call API to receive coordinate information
                coordinates = geocode(request.form['address3'])
                db.execute("INSERT INTO logs (user_id, activity, date, status, lat, long) VALUES( ?, ?, ?, ?, ?, ?)", (session["user_id"], 'travel', request.form['date3'], request.form['recovery'], coordinates['lat'], coordinates['lon']))
                db.commit()

            return redirect('/')

    else:

        status = db.execute("SELECT * FROM users WHERE id = ?",( session["user_id"],))
        # if user is not infected, second survey, if infected, first survey
        if status[0]['status'] != 'Infected':
            return render_template("Survey.html")
        else:
            return render_template("Survey2.html")





@app.route("/logs")
@login_required
def logs():

    """Show history of transactions"""


    index = db.execute("SELECT * FROM logs WHERE user_id = ? EXCEPT SELECT * FROM logs WHERE activity = ?", (session["user_id"], 'travel'))

    travels = db.execute("SELECT * FROM logs WHERE user_id = ? AND activity = ?", (session["user_id"], 'travel'))



    return render_template("logs.html", index = index, travels = travels)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        #make sure database exists
        db.execute("CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'name' TEXT NOT NULL, 'username' TEXT NOT NULL, 'hash' TEXT NOT NULL, 'lat' DECIMAL UNSIGNED NOT NULL, 'long' DECIMAL UNSIGNED NOT NULL, 'status' TEXT DEFAULT 'Healthy')")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = rows.fetchall()
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][easy_indexer('hash')], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][easy_indexer("id")]

        #create logs if they do not exist
        db.execute("CREATE TABLE IF NOT EXISTS 'logs' ('id' INTEGER, 'user_id' INTEGER, 'activity' TEXT NOT NULL, 'status' TEXT DEFAULT 'Healthy', 'lat' DECIMAL UNSIGNED , 'long' DECIMAL UNSIGNED, datetime DATETIME, date TEXT DEFAULT 'N/A', PRIMARY KEY(id))")

        ct = datetime.datetime.now()

        #insert interaction into logs
        db.execute("INSERT INTO logs (user_id, activity, datetime) VALUES( ?, ?, ?)", (session["user_id"], 'login', ct))
        db.commit()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        # ensure username submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # ensure first name was submitted
        elif not request.form.get("firstname"):
            return apology("Must provide first name", 400)
        # ensure surname was submitted
        elif not request.form.get("surname"):
            return apology("must provide last name", 400)
        # ensure age was submitted
        elif not request.form.get("Age"):
            return apology("must provide age", 400)
        # ensure Country was submitted
        elif not request.form.get("country"):
            return apology("must provide country", 400)
        # ensure State/province was submitted
        elif not request.form.get("state/province"):
            return apology("must provide state/province", 400)
        # ensure City was submitted
        elif not request.form.get("city"):
            return apology("must provide city", 400)
        # ensure street address was submitted
        elif not request.form.get("street address"):
            return apology("must provide street address", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure confirmation is the same as password
        elif request.form.get("confirmation") != request.form.get("password") :
            return apology("password and confirmation must match", 400)

        # Ensure password is appropriate length of 6 or more characters (personal touch)
        elif len(request.form.get("password")) < 6:
            return apology("Password must be at least 6 characters long", 400)

        # ensure age is valid
        elif int(request.form.get("Age")) < 3 :
            return apology("You are too young for this website! (Invalid Age)", 400)


        #make sure database exists

        db.execute("CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'name' TEXT NOT NULL, 'username' TEXT NOT NULL, 'hash' TEXT NOT NULL, 'lat' DECIMAL UNSIGNED NOT NULL, 'long' DECIMAL UNSIGNED NOT NULL, 'status' TEXT DEFAULT 'Healthy')")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", ([request.form.get("username")]))
        rows = rows.fetchall()
        # print(rows.fetchall())
        # Ensure username is not taken
        if len(rows) >= 1:
            return apology("username already taken", 400)

        # concatenate address in perfect address format using .format command and user responses
        address = "{} {} {} {} {}".format(request.form.get("street address"),request.form.get("city"), request.form.get("state/province"), request.form.get("country"), request.form.get("zip") )


        #ensure valid address is given and coordinates are acquired
        if geocode(address) == None:
            return apology("Invalid Address", 400)

        #call API to receive coordinate information
        coordinates = geocode(address)
        name = "{} {}".format(request.form.get("firstname"),request.form.get("surname"))

        db.execute("INSERT INTO users (name, username, hash, lat, long) VALUES( ?, ?, ?, ?, ?)", (name, request.form.get("username"), generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8), coordinates['lat'], coordinates['lon']  ))
        db.commit()

        #create logs if they do not exist
        db.execute("CREATE TABLE IF NOT EXISTS 'logs' ('id' INTEGER, 'user_id' INTEGER, 'activity' TEXT NOT NULL, 'status' TEXT DEFAULT 'Healthy', 'lat' DECIMAL UNSIGNED , 'long' DECIMAL UNSIGNED, datetime DATETIME, date TEXT DEFAULT 'N/A', PRIMARY KEY(id))")

        ct = datetime.datetime.now()

        # Remember which user has registered

        #insert interaction into logs

        return redirect("/")

        """Register user"""

    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)