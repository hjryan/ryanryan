from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, LocalesForm
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

@app.route('/walks')
def walks():
    return render_template('walks.html', title='Walks')

@app.route('/locales')
def locales():
    form = LocalesForm()
    return render_template('locales.html', title='Locales', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"{form.firstName.data}'s account created!", 'success')
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