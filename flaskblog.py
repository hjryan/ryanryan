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
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/activities')
def activities():
    return render_template('activities.html', title='Activities')

if __name__ == '__main__':
	app.run(debug=True)