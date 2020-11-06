from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'gilq34uiufgo39qwo7867854ww'

posts = [
	{
	'author': 'Hot Dog',
	'title': 'blog post 1',
	'content': 'akjkgjskjgtkwtg',
	'date_posted': 'April 20, 2018'
	},
	{
	'author': 'Hit Dig',
	'title': 'blog post 3000',
	'content': 'dflkfa',
	'date_posted': 'December 20, 2018'
	}
]

@app.route('/')
def index():
	return render_template('index.html', title='User Page')

@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/activities')
def activities():
    return render_template('activities.html', title='Activities')

@app.route('/walks')
def walks():
    return render_template('walks.html', title='Walks')

@app.route('/locales')
def locales():
    return render_template('locales.html', title='Locales')

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Log In', form=form)

if __name__ == '__main__':
	app.run(debug=True)