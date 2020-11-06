from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gilq34uiufgo39qwo7867854ww'

user = {
    'firstName': "First Name"
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
    return render_template('locales.html', title='Locales')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.firstName.data}!', 'success')
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

if __name__ == '__main__':
    app.run(debug=True)