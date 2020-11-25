from flask import Flask, render_template, url_for, flash, redirect, request, session
from db_con import get_db
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'gilq34uiufgo39qwo7867854ww'


@app.route('/')
def index():
    # open connection
    db = get_db()
    cur = db.cursor()

    # if the database is down, reset it
    if not cur.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' 
        AND name='{Users}';
        """):

        return redirect('/reset-db')

    # if there is no current session, send user to login
    if session == {}:
        return redirect('/login')
    else:
        
        # get list of user's activities by name for display
        activities = cur.execute("""
            SELECT Activities.activityName 
            FROM ActivitiesUsers 
            LEFT JOIN Activities 
            ON Activities.activityID = ActivitiesUsers.activityID 
            WHERE ActivitiesUsers.UserID = (?)
            """, [session['userID']]).fetchall()
        
        # close connection
        db.commit()
        db.close()

        return render_template(
            'index.html', 
            title='User Page', 
            user=session, 
            activities=activities)


@app.route('/home')
def home():
    
    # this is the index page
    return render_template('home.html')


@app.route('/add-activity-locale', methods=['GET'])
def addActLoc():

    # open connection
    db = get_db()
    cur = db.cursor()

    # get user input
    activityID = request.args.get('activityName')
    localeID = request.args.get('localeName')
    
    # inset input into ActivitiesLocales
    if activityID and localeID:
        cur.execute("""
            INSERT INTO ActivitiesLocales (activityID, localeID) 
            VALUES (?, ?)""", 
            (activityID, localeID))
    
    # close connection
    db.commit()
    db.close()

    return redirect('/activities')


@app.route('/add-activity-user', methods=['GET'])
def addActivityUser():
    
    # open connection
    db = get_db()
    cur = db.cursor()

    # get user input
    activityID = request.args.get('activityID')
    
    # check if user is already doing activity
    existingRelationship = (cur.execute("""
        SELECT activityID 
        FROM ActivitiesUsers 
        WHERE activityID = (?) 
        AND userID = (?)
        """,(activityID, session['userID'])).fetchone())

    # if not,
    if existingRelationship is None:

        # add ActivityUser
        cur.execute("""
            INSERT INTO ActivitiesUsers (activityID, userID) 
            VALUES (?, ?)
            """,(activityID, session['userID']))

        # find activity name (for pop-up)
        activityName = cur.execute("""
            SELECT activityName 
            FROM Activities W
            HERE activityID = (?) 
            """,[activityID]).fetchone()[0]

        flash(f"Enjoy {activityName}!", 'success')
    
    # if existingRelationship exists, skip add and show error
    else:
        flash('Our records show you are already registered for this activity', 'danger')
    
    # close connection
    db.commit()
    db.close()

    return redirect('/')  


@app.route('/add-activity', methods=['GET'])
def addActivity(activityName=None):

    # open connection
    db = get_db()
    cur = db.cursor()
    
    # get user input
    activityName = request.args.get('activityName')

    # innsert user input to Activities
    if activityName:
        cur.execute("""
            INSERT INTO Activities (activityName) 
            VALUES (?)
            """,(activityName,))

    # close connection
    db.commit()
    db.close()

    return redirect('/activities')


@app.route('/activities')
def activities():

    # if there is no current session, send user to login
    if session == {}:
        return redirect('/login')

    # open connection
    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    # get localeID based on localeName
    localeID = (cur.execute("""
        SELECT localeID 
        FROM Locales 
        WHERE localeName = (?)
        """, [session['localeName']]).fetchone())[0]

    # get activities & locales data -- all
    activities = cur.execute("""
        SELECT * 
        FROM Activities
        """).fetchall()
    locales = cur.execute("""
        SELECT * 
        FROM Locales
        """).fetchall()
    
    # get activities M:M data -- restricted by locale & user
    # restrict activities available to book to those in the current user's locale which they aren't already doing
    activitiesInYourLocale = cur.execute("""
        SELECT 
        Activities.activityID, 
        Activities.activityName 
        FROM ActivitiesLocales 
        LEFT JOIN Activities 
        ON Activities.activityID = ActivitiesLocales.activityID 
        LEFT JOIN ActivitiesUsers ON Activities.activityID = ActivitiesUsers.activityID 
        WHERE ActivitiesLocales.localeID = (?) 
        AND (ActivitiesUsers.userID <> (?) OR ActivitiesUsers.userID IS NULL)
        """,(localeID, session['userID'],)).fetchall()

    # restrict activities locales available for deletion to only those in the current user's locale
    activitiesLocales = cur.execute("""
        SELECT Activities.activityName 
        FROM ActivitiesLocales 
        LEFT JOIN Activities 
        ON ActivitiesLocales.activityID = Activities.activityID 
        WHERE ActivitiesLocales.localeID = (?)
        """,(localeID,)).fetchall()

    # restrict activities users available for deletion to only the current user's
    activitiesUsers = cur.execute("""
        SELECT 
        Activities.activityName, 
        Users.firstName 
        FROM ActivitiesUsers 
        LEFT JOIN Activities 
        ON ActivitiesUsers.activityID = Activities.activityID 
        LEFT JOIN Users ON Users.userID = ActivitiesUsers.userID 
        WHERE ActivitiesUsers.userID = (?)
        """,(session['userID'],)).fetchall()
    
    # close connection
    db.commit()
    db.close()

    return render_template(
        'activities.html', 
        title='Activities', 
        activities=activities, 
        activitiesLocales=activitiesLocales, 
        locales=locales, 
        activitiesUsers=activitiesUsers,
        activitiesInYourLocale=activitiesInYourLocale)


@app.route('/add-walk', methods=['GET'])
def addWalk(walkName=None):

    # open connection
    db = get_db()
    cur = db.cursor()

    # get session data
    userID = session['userID']
    originLocaleName = session['localeName']

    # get current localeID based on localeName
    originID = (cur.execute("""
        SELECT localeID 
        FROM Locales 
        WHERE localeName = (?)
        """,[originLocaleName]).fetchone())[0]
    
    # get user input
    walkName = request.args.get('walkName')
    destination = request.args.get('destination')

    # get destination localeID based on localeName (for session data)
    localeName = (cur.execute("""
        SELECT localeName 
        FROM Locales 
        WHERE localeID = (?)
        """, [destination]).fetchone())[0]

    # update user's localeID
    cur.execute("""
        UPDATE Users 
        SET localeID = (?) 
        WHERE userID = (?)
        """,(destination, userID,))
    
    # update session data
    session['localeName'] = localeName
    
    # add historical walk data to Walks table
    cur.execute("""
        INSERT INTO Walks (walkName, origin, destination, userID) 
        VALUES (?, ?, ?, ?)
        """,(walkName, originID, destination, userID,))

    # TO DO: going for a walk should also either:
        # insert all of your current Activities in the ActivitiesLocales table (the activities you're doing need to now exist in your new locale)
        # delete your current entries in ActivitiesUsers
    
    # close connection
    db.commit()
    db.close()

    return redirect('/walks')


@app.route('/walks')
def walks():

    # if there is no current session, send user to login
    if session == {}:
        return redirect('/login')

    # open connection
    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    # get all walks data
    data = cur.execute("""
        SELECT 
        Walks.walkID, 
        Walks.walkName, 
        LO.localeName AS origin, 
        LD.localeName AS destination, 
        Users.firstName as walker 
        FROM Walks 
        LEFT JOIN Locales LO ON Walks.origin = LO.LocaleID 
        LEFT JOIN Locales LD ON Walks.destination = LD.LocaleID 
        LEFT JOIN Users on Walks.userID = Users.userID
        """).fetchall()

    # get empty locales list (destination options)
    destinations = cur.execute("""
        SELECT * 
        FROM Locales 
        LEFT JOIN Users ON Locales.localeID = Users.LocaleID 
        WHERE Users.LocaleID IS NULL
        """).fetchall()
    
    # close connection
    db.commit()
    db.close()
    
    return render_template(
        'walks.html', 
        title='Walks', 
        destinations=destinations, 
        data=data)


@app.route('/add-locale', methods=['GET'])
def addLocale(localeName=None):
    
    # open connection
    db = get_db()
    cur = db.cursor()

    # get user input
    localeName = request.args.get('localeName')   
    
    # add to Locales table
    cur.execute("""
        INSERT INTO 
        Locales (localeName) 
        VALUES (?)
        """, (localeName,))
    
    # close connection
    db.commit()
    db.close()

    return redirect('/locales')


@app.route('/locales')
def locales():
    
    # if there is no current session, send user to login
    if session == {}:
        return redirect('/login')

    # open connection
    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    # get locales data
    locales = cur.execute("""
        SELECT 
        Locales.localeID, 
        Locales.localeName, 
        Users.firstName 
        FROM Locales 
        LEFT JOIN Users 
        ON Users.localeID = Locales.localeID
        """).fetchall()
    
    # close connection
    db.commit()
    db.close()

    return render_template(
        'locales.html', 
        title='Locales', 
        locales=locales)


@app.route('/complete-registration', methods=['GET'])
def completeRegistration(firstName=None, lastName=None, localeName=None):
    
    # reset session data
    session.clear()

    # open connection
    db = get_db()
    cur = db.cursor()

    # get user input
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    localeName = request.args.get('localeName') 

    # check that locale doesn't already exist, in which case skip create
    localeID = (cur.execute("""
        SELECT localeID 
        FROM Locales 
        WHERE localeName = (?)
        """, [localeName]).fetchone())

    if localeID is None:
        # create user's locale
        cur.execute("""
            INSERT INTO Locales (localeName) 
            VALUES (?)
            """, (localeName,))
        localeID = (cur.execute("""
            SELECT localeID 
            FROM Locales 
            WHERE localeName = (?)
            """, [localeName]).fetchone())[0]
    else:
        # if localeID exists, skip create
        localeID = localeID[0]
        
    # check that no one is currently at provided locale
    userID = (cur.execute("""
        SELECT userID 
        FROM Users 
        WHERE localeID = (?)
        """, [localeID]).fetchone())
    if userID is None:
        # add user
        cur.execute("""
            INSERT INTO Users (firstName, lastName, localeID) 
            VALUES (?, ?, ?)
            """, (firstName, lastName, localeID,))
        # update session data
        session['userID'] = (cur.execute("""
            SELECT userID 
            FROM Users 
            WHERE firstName = (?) 
            AND lastName = (?) 
            AND localeID = (?)
            """, (firstName, lastName, localeID,)).fetchone())[0]
        session['firstName'] = firstName
        session['lastName'] = lastName
        session['localeName'] = localeName
        flash(f"{firstName}'s account created!", 'success')

        # close connection
        db.commit()
        db.close()

        return redirect('/')

    else:
        flash('Registragion unsuccessful! Locale is not available. Please try again.', 'danger')
    
    # close connection
    db.commit()
    db.close()

    return redirect('/register') 


@app.route('/register', methods=['GET'])
def register(localeName=None):
    return render_template('register.html', title='Register')


@app.route('/complete-login', methods=['GET'])
def completeLogin(localeName=None):
    # reset session data
    session.clear()

    # open connection
    db = get_db()
    cur = db.cursor()

    # get user input
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    localeName = request.args.get('localeName')
    
    # find localeID for associated localeName, show error if doesn't exist
    localeID = (cur.execute("""
        SELECT localeID 
        FROM Locales 
        WHERE localeName = (?)
        """, [localeName]).fetchone())
    if localeID is None:
        flash('Login unsuccessful! Locale does not exist. Please try again.', 'danger')
        db.commit()
        db.close()
        return redirect('/login')
    localeID = localeID[0]
    
    # find userID for associated firstName, lastName, and localeID, show error if doesn't exist
    userID = (cur.execute("""
        SELECT userID 
        FROM Users 
        WHERE firstName = (?) 
        AND lastName = (?) 
        AND localeID = (?)
        """, (firstName, lastName, localeID,)).fetchone())
    if userID is None:
        flash('Login unsuccessful! A user with these characteristics does not exist. Please try again.', 'danger')
        db.commit()
        db.close()
        return redirect('/login')
    userID = userID[0]

    # if values provided by user match those for userID found, log in
    if firstName == (cur.execute("""
        SELECT firstName 
        FROM Users 
        WHERE userID = (?)
        """, [userID]).fetchall())[0][0] and lastName == (cur.execute("""
        SELECT lastName 
        FROM Users 
        WHERE userID = (?)
        """, [userID]).fetchall())[0][0] and localeID == (cur.execute("""
        SELECT localeID 
        FROM Users 
        WHERE userID = (?)""", [userID]).fetchall())[0][0]:
        
        # update session data
        session['userID'] = (cur.execute("""
            SELECT userID 
            FROM Users 
            WHERE firstName = (?) 
            AND lastName = (?) 
            AND localeID = (?)
            """, (firstName, lastName, localeID,)).fetchone())[0]
        
        session['firstName'] = firstName
        session['lastName'] = lastName
        session['localeName'] = localeName
        
        flash(f"Welcome back, {firstName}!", 'success')
        
        # close connection
        db.commit()
        db.close()
        
        return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Log In')


@app.route('/reset-db')
def reset_db():
    
    with app.app_context():
        db = get_db()
        with app.open_resource('setup-queries.sql', mode='r') as file:
            db.cursor().executescript(file.read())
        db.commit()
    print("Database Reset")

    # reset session data
    session.clear()

    # close connection
    db.close()

    return redirect('/login')


@app.route('/logout')
def logout():
    
    # reset session data
    session.clear()
    
    return redirect('/login')


# # Auto-closes db connection at the end of each request
# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(user, '_database', None)
#     if db is not None:
#         db.close()


if __name__ == '__main__':
    app.run(debug=True)