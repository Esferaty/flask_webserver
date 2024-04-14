from flask import Flask, render_template, request, redirect, url_for, session
from sqlite4 import SQLite4
from config import rights
app = Flask(__name__)
app.secret_key = 'arcadia'
database = SQLite4("database.db")
database.connect()


@app.route('/', methods=['GET'])
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'],
                               user=session['user'], rights=rights)
    else:
        return render_template('index.html')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        login = request.form.get('username')
        pswd = str(request.form.get('password'))
        query = database.select('users', ['password_hash'], f'username = "{login}"')
        if pswd == str(query[0][0]):
            session['username'] = login
            session['user'] = list(database.select('users', None, f'username = "{login}"')[0])
        return redirect(url_for('index'))
    return render_template('sign_in.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        login = str(request.form.get('username'))
        pswd = str(request.form.get('password'))
        email = str(request.form.get('email'))
        query = database.select('users', None, f'username = "{login}"')
        if query:
            return redirect(url_for('sign_up'))
        else:
            database.insert('users', {'username': login,
                                      'email': email,
                                      'password_hash': pswd,
                                      'rights': 1})
            return redirect(url_for('index'))
    return render_template('sign_up.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)