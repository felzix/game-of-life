from datetime import datetime, timedelta
from flask import flash, jsonify, redirect, render_template, request
from flask.ext.wtf import Form
import pickle
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo

from game_of_life_web_server import (
    app,
    auth,
    board,
    last_board_update,
    redis_client,
    tick_period)
from game_of_life_web_server.model import User
from game_of_life_common import constants


class SignUpForm(Form):
    username = StringField('Desired username?', [DataRequired()])
    password = PasswordField(
        'Desired password?',
        [DataRequired(),
         EqualTo('confirm_pw', message='Passwords must match')])
    confirm_pw = PasswordField('Confirm password:')
    submit = SubmitField('Sign Up')

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.from_redis(redis_client, self.username.data)
        if user is not None:
            self.username.errors.append('Username already taken')
            return False

        return True


class LoginForm(Form):
    username = StringField('Username?', [DataRequired()])
    password = PasswordField('Password?', [DataRequired()])
    submit = SubmitField('Log In')

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.from_redis(redis_client, self.username.data)
        if user is None:
            self.username.errors.append('Username does not exist')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        return True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html', form=SignUpForm())


@app.route('/signup', methods=['POST'])
def signup_post():
    form = SignUpForm(request.form)
    if form.validate():
        User(username=form.username.data, password=form.password.data).to_redis(redis_client)
        flash('Welcome!')
        return redirect('/login')
    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET"])
def login():
    return render_template('login.html', form=LoginForm())


@app.route('/login', methods=['POST'])
def login_post():
    form = LoginForm(request.form)
    if form.validate():
        return redirect('/gol')
    else:
        flash('Wrong username and/or password!')
        return render_template('login.html', form=form)


@app.route('/gol')
@auth.login_required
def gol():
    assert board, 'Board not initialized'
    assert tick_period, 'Tick period not initialized'
    return render_template(
        'gol.html',
        width=board.width,
        height=board.height,
        tile_size=constants.TILE_SIZE,
        tick_period=tick_period,
    )


@app.route('/gol/state', methods=['GET'])
@auth.login_required
def gol_state_get():
    if datetime.now() - last_board_update >= timedelta(milliseconds=tick_period.__subject__):
        # TODO error handling if pickled object differs, requiring web server reload
        board.__subject__ = pickle.loads(redis_client.get(constants.REDIS_KEY_BOARD))
    return jsonify(tiles=board.tiles, iteration=board.iteration)


@app.route('/gol/state', methods=['PUT'])
@auth.login_required
def gol_state_put():
    x = request.form.get('x')
    y = request.form.get('y')
    print 'STATE PUT: {},{}'.format(x, y)
    redis_client.rpush(constants.REDIS_KEY_ADDITIONS, '{},{}'.format(x, y))
    return 'OK'


@app.route('/gol/state', methods=['DELETE'])
@auth.login_required
def gol_state_delete():
    x = request.args.get('x')
    y = request.args.get('y')
    print 'STATE DELETE: {},{}'.format(x, y)
    redis_client.rpush(constants.REDIS_KEY_REMOVALS, '{},{}'.format(x, y))
    return 'OK'


@app.route('/gol/running', methods=['PUT'])
@auth.login_required
def gol_running_state():
    new_running_state = request.form.get('new_running_state')
    redis_client.set(constants.REDIS_KEY_RUNNING_STATE, new_running_state)
    return 'OK'