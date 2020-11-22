from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
from db_con import get_db
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gilq34uiufgo39qwo7867854ww'

user = {
    'userID' : "User ID", #int, autoincrement, not NULL, PK
    'firstName': "First Name", #varchar, not NULL
    'lastName': "Last Name", #varchar, not NULL
    'localeName' : "Locale Name" #this should be from a diff table lol
}

@app.route('/')
def index():
    return render_template('index.html', title='User Page', user=user)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/add-activity-locale', methods=['GET'])
def addActLoc():
    db = get_db()
    cur = db.cursor()
    actID = request.args.get('activityName')
    localeID = request.args.get('localeName')
    if actID and localeID:
        cur.execute("INSERT INTO ActivitiesLocales (activityID, localeID) VALUES (?, ?)", 
            (actID, localeID))
    db.commit()
    db.close()
    return redirect('/activities')

@app.route('/add-activity', methods=['GET'])
def addActivity(activityName=None):
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
    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    data = cur.execute("""SELECT * FROM Activities""").fetchall()
    actLocals = cur.execute("SELECT * FROM ActivitiesLocales").fetchall()
    locs = cur.execute("SELECT * FROM Locales").fetchall()
    actUsers = cur.execute("SELECT * FROM ActivitiesUsers").fetchall()
    db.commit()
    db.close()
    return render_template('activities.html', title='Activities', 
        data=data, 
        actloc=actLocals, 
        locs=locs, 
        actUsers=actUsers)

@app.route('/add-walk', methods=['GET'])
def addWalk(walkName=None):
    db = get_db()
    cur = db.cursor()
    userID = 1 # fix me
    origin = 1 # fix me
    walkName = request.args.get('walkName')
    destination = request.args.get('destination')
    if userID and destination:
        # cur.execute("UPDATE Users (localeID) SET localeID = (?) WHERE userID = (?)", 
        #      (destination, userID)) # does this work? find out
        added = cur.execute("INSERT INTO Walks (walkName, origin, destination, userID) VALUES (?, ?, ?, ?)", (walkName, origin, destination, userID,))
    db.commit()
    db.close()
    return redirect('/walks')

@app.route('/walks')
def walks():
    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    data = cur.execute("""SELECT * FROM Walks""").fetchall()
    locales = cur.execute("SELECT * FROM Locales LEFT JOIN Users ON Locales.localeID = Users.LocaleID WHERE Users.LocaleID IS NULL").fetchall() # only locales no one is at
    db.commit()
    db.close()
    return render_template('walks.html', title='Walks', locales=locales, data=data)

@app.route('/add-locale', methods=['GET'])
def addLocale(localeName=None):
    db = get_db()
    cur = db.cursor()
    localeName = request.args.get('localeName')   
    if localeName:
        added = cur.execute("INSERT INTO Locales (localeName) VALUES (?)", (localeName,))
    db.commit()
    db.close()
    return redirect('/locales')

@app.route('/locales')
def locales():
    db = get_db()
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    data = cur.execute("""SELECT Locales.localeID, Locales.localeName, Users.userID FROM Locales LEFT JOIN Users ON Users.localeID = Locales.localeID""").fetchall()
    db.commit()
    db.close()
    return render_template('locales.html', title='Locales', data=data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    db = get_db()
    cur = db.cursor()
    firstName = {form.firstName.data}
    lastName = {form.lastName.data}
    localeName = {form.localeName.data}
    localeID = cur.execute("""SELECT localeID FROM Locales WHERE localeName = (?)""", (localeName,)).fetchall()
    # additional validations needed --
    # use locales data to check if locale already exists
    # if so, is someone there? don't let them register there

    # otherwise, add locale
    def addLocale(localeName=None):
    db = get_db()
    cur = db.cursor()
    localeName = request.args.get('localeName')   
    if localeName:
        added = cur.execute("INSERT INTO Locales (localeName) VALUES (?)", (localeName,))
    db.commit()
    db.close()

    if form.validate_on_submit():
        flash(f"{form.firstName.data}'s account created!", 'success')
        added = cur.execute("INSERT INTO Users (firstName, lastName, localeID) VALUES (?, ?, ?)", (firstName, lastName, localeID,))
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.firstName.data == 'hotdog' and form.password.data == 'password':
            flash(f'Welcome {form.firstName.data}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful! Please try again.', 'danger')
    return render_template('login.html', title='Log In', form=form)

@app.route('/reset-db')
def reset_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('setup-queries.sql', mode='r') as file:
            db.cursor().executescript(file.read())
        db.commit()
    return "Database Reset"

if __name__ == '__main__':
    app.run(debug=True)