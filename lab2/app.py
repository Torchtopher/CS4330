from flask import Flask, redirect, url_for, request, send_file
from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=0, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=0, max=35),
    ])
    mode = StringField('Mode', [validators.AnyOf(['login', 'register'])])

app = Flask(__name__)

# add a route
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        
        if not form.validate():
            print(f"{form.errors}")
            return "ERROR"
        print(f"MODE: {form.mode.data}")
        print(f"USERNAME: {form.username.data}")
        print(f"PASSWORD: {form.password.data}")
        # why you pass a function name as a string is beyond me lol
        return redirect(url_for('minesweeper_intro'))
    else:
        return send_file("static/login.html")

@app.route('/games/minesweeper')
def minesweeper_intro():
    return send_file("games/minesweeper/intro.html")

# make route accept url parameters

@app.route('/games/minesweeper/game')
def minesweeper_game():
    return send_file("games/minesweeper/minesweeper.html")

@app.errorhandler(404) 
def not_found(e): 
    return send_file("static/404.html") 

# run the app
if __name__ == '__main__':
    app.run(debug=True, port=8080)