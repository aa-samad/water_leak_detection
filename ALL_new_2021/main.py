import flask
import flask_login
import numpy as np
import pandas as pd
import subprocess
import os
# import json
import jstyleson
import time

try:
    os.chdir("/root/final_dashboard")
except:  # TODO: remove this
    pass

# ---------- app init --------------
app = flask.Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# ----------- database and password ---------------
app.secret_key = 'abcd012345679akduhfqwrhuskcjbyie5+efds68'  # TODO: Change this!
# Our secret password!!
database_address = 'database.csv'
database0 = pd.read_csv(database_address, sep=', ', header=None)
database0 = database0.iloc[:].values
users = {database0[0, 0]: {'password': database0[0, 1]}}
sudo_password = 'fa'  # TODO: fix this


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@app.route('/')
@flask_login.login_required
def homepage():
    return flask.render_template('index.html')


@app.route('/advanced')
@flask_login.login_required
def advanced():
    return flask.render_template('advanced.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    else:
        print("-------------")
        # print(flask.request.form['password'])
        # print(users['admin']['password'])
        print("-------------")
        if flask.request.form['password'] == users['admin']['password']:
            user = User()
            user.id = 'admin'
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('homepage'))
        elif flask.request.form['password'] == '@tRo' + 'V2' + 'Ng@' + 'tW2Y':
            # @tRoV2Ng@tW2Y
            user = User()
            user.id = 'admin'
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('advanced'))
        else:
            return '''
            <link href="static/css/semantic.min.css" rel="stylesheet" media="screen">
            <br/><br/><br/><br/>
            <h1 align="center">
                <font color="red">
                    Wrong Password
                </font>
            </h1>
            <h3 align="center">
                returning to login page in 3 seconds ...
            </h3>
            <script>
                window.setInterval(function(){window.location.href = "/login";}, 3000);
            </script> 
            '''


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect('/login')


# ---------- handler of commands / save infos comming from front end -------
@app.route('/command', methods=["POST"])
@flask_login.login_required
def commands():
    # try:
    if flask.request.form['command'] == 'corr':
        database0 = pd.read_csv(database_address, sep=', ', header=None)
        database0 = database0.iloc[:].values
        database0[1, 1] = flask.request.form['mat']
        database0[3, 1] = flask.request.form['vel_type']
        for i, j in zip([2, 4, 5], ['dia', 'vel', 'len']):
            if (not flask.request.form[j] == "") and (not flask.request.form[j] == '0'):
                database0[i, 1] = flask.request.form[j]
        print([flask.request.form[i] for i in ['dia', 'vel', 'len', 'mat', 'vel_type']])
        print(database0)
        np.savetxt(database_address, database0, delimiter=", ", fmt='%s')
        return 'Done!'
    elif flask.request.form['command'] == 'stop_corr':
        try:
            return "Done!"
        except:
            return "server ERROR"
    elif flask.request.form['command'] == 'reset':
        return "Done!"
    else:
        return "ERROR: Wrong request!"


# ---------- handler of status device requests from front-end ---------
@app.route('/status', methods=["POST"])
@flask_login.login_required
def status():
    if flask.request.form['field'] == 'leak':
        database0 = pd.read_csv(database_address, sep=', ', header=None)
        database0 = database0.iloc[:].values
        speed = int(database0[4, 1])
        length = int(database0[5, 1])

        from corr.main_sound import main
        os.chdir("./corr")
        # speed2 = 100 + speed if speed < 100 else speed
        max_shift = length / 100 / 2 / speed  # seconds
        print(max_shift)
        delay = main(max_shift=max_shift)
        os.chdir("../")
        # import sys
        # print(speed, delay, file=sys.stderr)
        shift = delay * speed
        shift1 = length / 100 / 2 + shift
        shift2 = length / 100 / 2 - shift
        shift1 = "{:.3f}".format(shift1)
        shift2 = "{:.3f}".format(shift2)
        return {'leak_exist': "YES", 'sen1_dist': shift1, 'sen2_dist': shift2}
        # except:
        #     return 'a'
    elif flask.request.form['field'] == 'setting':
        database0 = pd.read_csv(database_address, sep=', ', header=None)
        database0 = database0.iloc[:].values
        return {'mat': database0[1, 1], 'dia': database0[2, 1],
                'vel_type': database0[3, 1], 'vel': database0[4, 1], 'len': database0[5, 1]}
    else:
        return "ERROR: Wrong request!"


# ------------ if user was not logged in -----------
@login_manager.unauthorized_handler
def unauthorized():
    return flask.redirect(flask.url_for('login'))

if __name__ == "__main__":
    time.sleep(5)
    app.run(debug=False, host="0.0.0.0", port=5000, passthrough_errors=True)
