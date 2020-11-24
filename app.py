from flask import Flask, render_template, url_for, flash, redirect, request
from db_con import get_db
import time
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gilq34uiufgo39qwo7867854ww'

# experience should be based on who y'are
user = {
    'userID' : 0,
    'firstName': "First Name",
    'lastName': "Last Name",
    'localeName' : "Locale Name"
}

@app.route('/')
def index():
    time.sleep(1)
    print(user)
    if user['userID'] == 0:
        return redirect('/login')
    else:
        db = get_db()
        cur = db.cursor()
        
        activities = cur.execute("""SELECT Activities.activityName FROM ActivitiesUsers LEFT JOIN Activities ON Activities.activityID = ActivitiesUsers.activityID WHERE ActivitiesUsers.UserID = (?) """, [user['userID']]).fetchall()
        return render_template('index.html', title='User Page', user=user, activities=activities)

@app.route('/home')
def home():
    time.sleep(1)
    print(user)
    return render_template('home.html')

@app.route('/add-activity-locale', methods=['GET'])
def addActLoc():
    time.sleep(1)
    print(user)
    db = get_db()
    cur = db.cursor()

    # get user input
    activityID = request.args.get('activityName')
    localeID = request.args.get('localeName')
    if activityID and localeID:
        cur.execute("INSERT INTO ActivitiesLocales (activityID, localeID) VALUES (?, ?)", 
            (activityID, localeID))
    db.commit()
    db.close()
    return redirect('/activities')

@app.route('/add-activity-user', methods=['GET'])
def addActivityUser():
    time.sleep(1)
    print(user)
    db = get_db()
    cur = db.cursor()

    # get user input
    activityID = request.args.get('activityID')
    
    # restrict adds to only new relationships
    existingRelationship = (cur.execute("SELECT activityID FROM ActivitiesUsers WHERE activityID = (?) AND userID = (?)", (activityID, user['userID'])).fetchone())
    if existingRelationship is None:
        # add ActivityUser
        cur.execute("INSERT INTO ActivitiesUsers (activityID, userID) VALUES (?, ?)", 
            (activityID, user['userID']))
        # find activity name (for pop-up)
        activityName = cur.execute("""SELECT activityName FROM Activities WHERE activityID = (?) """, [activityID]).fetchone()[0]
        flash(f"Enjoy {activityName}!", 'success')
    else:
        # if existingRelationship exists, skip add and show error
        flash('Our records show you are already registered for this activity', 'danger')
    db.commit()
    db.close()
    return redirect('/')  

@app.route('/add-activity', methods=['GET'])
def addActivity(activityName=None):
    time.sleep(1)
    print(user)
    db = get_db()
    cur = db.cursor()
    activityName = request.args.get('activityName')
    if activityName:
        added = cur.execute("INSERT INTO Activities (activityName) VALUES (?)", (activityName,))
    db.commit()
    db.close()
    return redirect('/activities')

@app.route('/activities')
def activities():
    time.sleep(1)
    print(user)
    if user['userID'] == 0:
        return redirect('/login')

    else:
        db = get_db()
        db.row_factory = sqlite3.Row
        cur = db.cursor()

        # get global user data
        userID = user['userID']
        localeName = user['localeName']
        # get localeID based on localeName
        localeID = (cur.execute("SELECT localeID FROM Locales WHERE localeName = (?)", [localeName]).fetchone())[0]


        # get activities & locales data -- all
        activities = cur.execute("""SELECT * FROM Activities""").fetchall()
        locales = cur.execute("SELECT * FROM Locales").fetchall()
        
        # get activities M:M data -- restricted by locale & user
        # restrict activities available to book to those in your locale which you aren't already doing
        activitiesInYourLocale = cur.execute("""SELECT Activities.activityID, Activities.activityName FROM ActivitiesLocales LEFT JOIN Activities ON Activities.activityID = ActivitiesLocales.activityID LEFT JOIN ActivitiesUsers ON Activities.activityID = ActivitiesUsers.activityID WHERE ActivitiesLocales.localeID = (?) AND ActivitiesUsers.userID is NULL""", [localeID]).fetchall()
        # restrict activities locales available for deletion to only those in your locale
        activitiesLocales = cur.execute("SELECT Activities.activityName FROM ActivitiesLocales LEFT JOIN Activities ON ActivitiesLocales.activityID = Activities.activityID WHERE ActivitiesLocales.localeID = (?)", (localeID,)).fetchall()
        # restrict activities users available for deletion to only yours
        activitiesUsers = cur.execute("SELECT Activities.activityName, Users.firstName FROM ActivitiesUsers LEFT JOIN Activities ON ActivitiesUsers.activityID = Activities.activityID LEFT JOIN Users on Users.userID = ActivitiesUsers.userID WHERE ActivitiesUsers.userID = (?)", (userID,)).fetchall()
        
        db.commit()
        db.close()
        return render_template('activities.html', title='Activities', 
            activities=activities, 
            activitiesLocales=activitiesLocales, 
            locales=locales, 
            activitiesUsers=activitiesUsers,
            activitiesInYourLocale=activitiesInYourLocale)

@app.route('/add-walk', methods=['GET'])
def addWalk(walkName=None):
    time.sleep(1)
    print(user)
    db = get_db()
    cur = db.cursor()

    # get global user data
    userID = user['userID']
    originLocaleName = user['localeName']

    # get localeID based on localeName
    originID = (cur.execute("SELECT localeID FROM Locales WHERE localeName = (?)", [originLocaleName]).fetchone())[0]
    
    # get user input
    walkName = request.args.get('walkName')
    destination = request.args.get('destination')

    # update user's localeID
    cur.execute("UPDATE Users SET localeID = (?) WHERE userID = (?)", (destination, userID,))
    
    # update global user data
    localeName = (cur.execute("SELECT localeName FROM Locales WHERE localeID = (?)", [destination]).fetchone())[0]
    user['localeName'] = localeName
    
    # add historical walk data to Walks table
    cur.execute("INSERT INTO Walks (walkName, origin, destination, userID) VALUES (?, ?, ?, ?)", (walkName, originID, destination, userID,))

    # TO DO: going for a walk should also either:
        # insert all of your current Activities in the ActivitiesLocales table (the activities you're doing need to now exist in your new locale)
        # delete your current entries in ActivitiesUsers
    
    db.commit()
    db.close()
    return redirect('/walks')

@app.route('/walks')
def walks():
    time.sleep(1)
    print(user)
    if user['userID'] == 0:
        return redirect('/login')

    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    # get all walks data
    data = cur.execute("""SELECT Walks.walkID, Walks.walkName, LO.localeName AS origin, LD.localeName AS destination, Users.firstName as walker FROM Walks LEFT JOIN Locales LO ON Walks.origin = LO.LocaleID LEFT JOIN Locales LD ON Walks.destination = LD.LocaleID LEFT JOIN Users on Walks.userID = Users.userID""").fetchall()

    # get empty locales list (destination options)
    destinations = cur.execute("SELECT * FROM Locales LEFT JOIN Users ON Locales.localeID = Users.LocaleID WHERE Users.LocaleID IS NULL").fetchall()
    
    db.commit()
    db.close()
    return render_template('walks.html', title='Walks', destinations=destinations, data=data)

@app.route('/add-locale', methods=['GET'])
def addLocale(localeName=None):
    time.sleep(1)
    print(user)
    db = get_db()
    cur = db.cursor()

    # get user input
    localeName = request.args.get('localeName')   
    
    # add to Locales table
    cur.execute("INSERT INTO Locales (localeName) VALUES (?)", (localeName,))
    
    db.commit()
    db.close()
    return redirect('/locales')

@app.route('/locales')
def locales():
    time.sleep(1)
    print(user)
    if user['userID'] == 0:
        return redirect('/login')

    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    # get locales data
    locales = cur.execute("""SELECT Locales.localeID, Locales.localeName, Users.firstName FROM Locales LEFT JOIN Users ON Users.localeID = Locales.localeID""").fetchall()
    
    db.commit()
    db.close()
    return render_template('locales.html', title='Locales', locales=locales)

@app.route('/complete-registration', methods=['GET'])
def completeRegistration(firstName=None, lastName=None, localeName=None):
    time.sleep(1)
    print(user)
    # reset global user data
    user['userID'] = 0
    user['firstName'] = "First Name"
    user['lastName'] = "Last Name"
    user['localeName'] = "Locale Name"

    db = get_db()
    cur = db.cursor()

    # save values provided by user
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    localeName = request.args.get('localeName') 

    # check that locale doesn't already exist, in which case skip create
    localeID = (cur.execute("SELECT localeID FROM Locales WHERE localeName = (?)", [localeName]).fetchone())
    if localeID is None:
        # create user's locale
        cur.execute("INSERT INTO Locales (localeName) VALUES (?)", (localeName,))
        localeID = (cur.execute("SELECT localeID FROM Locales WHERE localeName = (?)", [localeName]).fetchone())[0]
    else:
        # if localeID exists, skip create
        localeID = localeID[0]
        
    # check that no one is currently at provided locale
    userID = (cur.execute("SELECT userID FROM Users WHERE localeID = (?)", [localeID]).fetchone())
    if userID is None:
        # add user
        cur.execute("INSERT INTO Users (firstName, lastName, localeID) VALUES (?, ?, ?)", (firstName, lastName, localeID,))
        # update this lil dictionary which is used in the user's home page
        user['userID'] = (cur.execute("SELECT userID FROM Users WHERE firstName = (?) AND lastName = (?) AND localeID = (?)", (firstName, lastName, localeID,)).fetchone())[0]
        user['firstName'] = firstName
        user['lastName'] = lastName
        user['localeName'] = localeName
        flash(f"{firstName}'s account created!", 'success')
        db.commit()
        db.close()
        return redirect('/')
    else:
        flash('Registragion unsuccessful! Locale is not available. Please try again.', 'danger')
    
    db.commit()
    db.close()
    return redirect('/register') 

@app.route('/register', methods=['GET'])
def register(localeName=None):
    time.sleep(1)
    print(user)
    return render_template('register.html', title='Register')

@app.route('/complete-login', methods=['GET'])
def completeLogin(localeName=None):
    time.sleep(1)
    print(user)
    # reset global user data
    user['userID'] = 0
    user['firstName'] = "First Name"
    user['lastName'] = "Last Name"
    user['localeName'] = "Locale Name"

    db = get_db()
    cur = db.cursor()

    # get user input
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    localeName = request.args.get('localeName')
    
    # find localeID for associated localeName, show error if doesn't exist
    localeID = (cur.execute("SELECT localeID FROM Locales WHERE localeName = (?)", [localeName]).fetchone())#[0]
    if localeID is None:
        flash('Login unsuccessful! Locale does not exist. Please try again.', 'danger')
        return redirect('/login')
    localeID = localeID[0]
    
    # find userID for associated firstName, lastName, and localeID, show error if doesn't exist
    userID = (cur.execute("SELECT userID FROM Users WHERE firstName = (?) AND lastName = (?) AND localeID = (?)", (firstName, lastName, localeID,)).fetchone())
    if userID is None:
        flash('Login unsuccessful! A user with these characteristics does not exist. Please try again.', 'danger')
        return redirect('/login')
    userID = userID[0]

    # if values provided by user match those for userID found, log in
    if firstName == (cur.execute("SELECT firstName FROM Users WHERE userID = (?)", [userID]).fetchall())[0][0] and lastName == (cur.execute("SELECT lastName FROM Users WHERE userID = (?)", [userID]).fetchall())[0][0] and localeID == (cur.execute("SELECT localeID FROM Users WHERE userID = (?)", [userID]).fetchall())[0][0]:
        # update this lil dictionary which is used in the user's home page
        user['userID'] = (cur.execute("SELECT userID FROM Users WHERE firstName = (?) AND lastName = (?) AND localeID = (?)", (firstName, lastName, localeID,)).fetchone())[0]
        user['firstName'] = firstName
        user['lastName'] = lastName
        user['localeName'] = localeName
        flash(f"Welcome back, {firstName}!", 'success')
        db.commit()
        db.close()
        return redirect('/')

    # other scenario I haven't thought of (maybe delete, maybe exists)
    else:
        flash('Login unsuccessful! Please try again.', 'danger')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    time.sleep(1)
    print(user)
    return render_template('login.html', title='Log In')

@app.route('/reset-db')
def reset_db():
    time.sleep(1)
    print(user)
    with app.app_context():
        db = get_db()
        with app.open_resource('setup-queries.sql', mode='r') as file:
            db.cursor().executescript(file.read())
        db.commit()
    print("Database Reset")

    # reset global user data
    user['userID'] = 0
    user['firstName'] = "First Name"
    user['lastName'] = "Last Name"
    user['localeName'] = "Locale Name"

    return redirect('/login')

@app.route('/logout')
def logout():
    time.sleep(1)
    print(user)

    # reset global user data
    user['userID'] = 0
    user['firstName'] = "First Name"
    user['lastName'] = "Last Name"
    user['localeName'] = "Locale Name"

    return redirect('/login')

# Auto-closes db connection at the end of each request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(user, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)