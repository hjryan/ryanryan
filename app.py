from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from db_con import get_db

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

@app.route('/activities')
def activities():
    return render_template('activities.html', title='Activities')

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