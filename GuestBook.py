from flask import Flask
import shelve
from flask import Flask, request, render_template, redirect, escape, Markup
import time

DATA_FILE = 'GuestBook.dat'
app = Flask(__name__)


def save_data(name, comment, create_at):
    datebase = shelve.open(DATA_FILE)

    if 'greeting_list' not in datebase:
        greeting_list = []
    else:
        greeting_list = datebase['greeting_list']

    greeting_list.insert(0, {
        'name': name,
        'comment': comment,
        'create_at': create_at,
    })
    datebase['greeting_list'] = greeting_list
    datebase.close()


def load_data():
    database = shelve.open(DATA_FILE)
    greeting_list = database.get('greeting_list',[])
    database.close()
    return greeting_list


@app.route('/')
def index():
    greeting_list = load_data()
    return render_template('index.html', greeting_list = greeting_list)

@app.route('/post', methods=['POST'])
def post():
    name = request.form.get('name')
    comment = request.form.get('comment')
    create_at = request.form.get('create_at')

    save_data(name, comment, create_at)
    return redirect('/')

@app.template_filter('nl2br')
def nl2br_filters(s):
    return escape(s).replace('/n', Markup('</br>'))

@app.template_filter('datetime_fmt')
def datetime_fmt(dt):
    return dt.strftime('%Y/%m/%d %H:%M:%S')

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)



