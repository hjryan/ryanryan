from flask import Flask, render_template, url_for
app = Flask(__name__)

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

if __name__ == '__main__':
	app.run(debug=True)