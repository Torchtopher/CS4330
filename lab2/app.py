from flask import Flask, redirect, url_for, request, send_file
from wtforms import Form, StringField, PasswordField, validators
import sys
import games
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import jinja2
import uuid

# don't want to type this out every time
MS_t = games.minesweeper.minesweeper.MineSweeper

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=0, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=0, max=35),
    ])
    mode = StringField('Mode', [validators.AnyOf(['login', 'register'])])


running_games = {}

# create the app
games_page = Blueprint('games', "games.minesweeper",
                        template_folder='templates')

# default to minesweeper
@games_page.route('/', defaults={'game': 'minesweeper'})
@games_page.route('/<game>/game', methods=['GET', 'POST', 'PUT'])
def handle_game(game=None):
    if request.method == 'POST':
        print("POST METHOD CALLED")
        fields = ["rows", "cols", "name"]
        # if not all fields are present, return an error
        print(f"FORM: {request.form}")
        if not all(field in request.form for field in fields):
            return {"status": "ERROR"}
        minesweeper: MS_t = games.minesweeper.factory()
        print(f"ROWS: {request.form['rows']}")
        print(f"COLS: {request.form['cols']}")
        game = minesweeper(rows=int(request.form["rows"]), cols=int(request.form["cols"]))
        game.setName(name=str(request.form["name"]))
        id = str(uuid.uuid4())
        # ------------------------------------------------------------------
        # JUST FOR TESTING, REMOVE ME LATER
        #id = "c64d1357-280f-4420-a9d7-ed0886b26ac5"
        running_games[id] = game
        print(f"ID: {id}")
        redirect_url = url_for("games.handle_game", id=id, rows=request.form["rows"], cols=request.form["cols"], name=request.form["name"])
        return redirect(redirect_url)
        #return send_file("games/minesweeper/intro.html")
    
    elif request.method == 'PUT':
        # print out url encoded id parameter
        print(f"ID: {request.form}")
        # get the url encoded id parameter
        # "GET /games/?id=c64d1357-280f-4420-a9d7-ed0886b26ac5 
        print(f"ID: {request.form.get('id')}")
        # print out json encoded action and data parameters
        print(f"ACTION: {request.json['action']}")
        act = request.json['action']
        print(f'Running Games: {running_games}')
        current_game: MS_t = running_games[request.args.get('id')] # id should be a uuid
        # return every space on the board 
        if act == "board":
            print("GETTING BOARD")
            game_over = current_game.getGameOver()
            score = current_game.getScore()
            # get all the spaces into a dictionary of (row, col): public value
            board = {} 
            for r in range(current_game.getRows()):
                for c in range(current_game.getCols()):
                    board[f"{r}, {c}"] = current_game.getSpace(r, c)
            print(f"BOARD: {board}")
            return {"status": "OK", "data": {"value": board, "game_over": game_over, "score": score}} 
        elif act == "pick":
            row, col = request.json['data']["row"], request.json['data']["col"]
            was_legal = current_game.pickSpace(row, col)
            print(f"WAS LEGAL: {was_legal}")
            # move was not legal, return an error
            if not was_legal:
                return {"status": "ERROR", "data": "Move was not legal"}
            space = current_game.getSpace(row, col)
            game_over = current_game.getGameOver()
            score = current_game.getScore()
            return {"status": "OK", "data": {"value": space, "game_over": game_over, "score": score}}
        elif act == "space":
            pass
        elif act == "score":
            return {"status": "OK", "data": current_game.getScore()}
        elif act == "time":
            return {"status": "OK", "data": current_game.time()}
        elif act == "name":
            return {"status": "OK", "data": current_game.getName()}
        else:
            return {"status": "ERROR", "data": "Invalid action"}

    elif request.method == 'GET':
        # fully render board here and then return it
        return render_template("minesweeper.j2")


    return f"hello {game}"

app = Flask(__name__)
app.register_blueprint(games_page, url_prefix='/games')

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

# @app.route('/games/minesweeper/game')
# def minesweeper_game():
#     return send_file("games/minesweeper/minesweeper.html")

@app.errorhandler(404) 
def not_found(e): 
    return send_file("static/404.html") 

# run the app
if __name__ == '__main__':
    app.run(debug=True, port=8080)