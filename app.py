from flask import Flask, render_template, session, redirect, json
from flask.globals import request
import re

from DB_handler import *

app = Flask(__name__)
app.config.from_object("config")

app.secret_key = 'try_again'

# SQLITE CONNECTION
dbHandler = DBHandler(app.config["DB_PATH"])


@app.route('/')
def start():
    session.clear()
    return render_template("index.html")


@app.route('/signInPage')
def signInPage():
    session.clear()
    return render_template("login.html")


@app.route('/joinAsClient')
def clintSingUpPage():
    return render_template("newuser.html")


@app.route('/joinAsWorker')
def workerSingUpPage():
    return render_template("newaccount.html")


@app.route('/adminPage')
def adminPage():
    if session.get('loggedin') == 'admin':
        return render_template("admin.html")
    return redirect('/signInPage')


@app.route('/dashboardPage')
def dashboardPage():
    if session.get('loggedin') == 'client':
        saveSearch = dbHandler.getjobs()
        if saveSearch == []:
            return render_template("dashboard.html", Error="Currently no worker available")
        else:
            return render_template("dashboard.html", jobList=saveSearch)
    return redirect('/signInPage')


@app.route('/searchresult', methods=['POST', 'GET'])
def searchedResults():
    if session.get('loggedin') == 'client':
        saveSearch = dbHandler.getSearchedjobs(request.form['searchText'])
        if saveSearch == []:
            return render_template("dashboard.html", Error="Currently no worker available")
        else:
            return render_template("dashboard.html", jobList=saveSearch)
    return redirect('/signInPage')


@app.route('/workerPage')
def workerPage():
    if session.get('loggedin') == 'worker':
        return render_template("worker.html")
    return redirect('/signInPage')


@app.route('/clientPage')
def clientPage():
    if session.get('loggedin') == 'client':
        return render_template("client.html")
    elif session.get('loggedin') == 'admin':
        return render_template("admin.html")
    return redirect('/signInPage')


@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method != 'POST':
        return redirect('/signInPage')

    validation = dbHandler.validation(
        request.form['status'],
        request.form['email'],
        request.form['password']
    )

    if validation:
        session['id'] = validation

        if request.form['status'] == "As Client":
            if dbHandler.isAdmin(request.form['email']):
                session['loggedin'] = 'admin'
                session['email'] = request.form['email']
                return redirect('/adminPage')
            else:
                session['loggedin'] = 'client'
                session['email'] = request.form['email']
                return redirect('/dashboardPage')

        elif request.form['status'] == "As Worker":
            session['loggedin'] = 'worker'
            session['email'] = request.form['email']
            return redirect('/workerPage')

    else:
        return render_template("login.html", fail='Invalid credentials')


@app.route('/addNewClient', methods=['POST', 'GET'])
def addNewClient():
    if request.method != 'POST':
        return redirect('/joinAsClient')

    if dbHandler.insertClient(
        request.form['name'],
        request.form['mobile'],
        request.form['city'],
        request.form['email'],
        request.form['password']
    ):
        return render_template('login.html', success='Registration done successfully, now log in')

    else:
        if dbHandler.isClinetExist(request.form['email']):
            return render_template("newuser.html", fail='An account with this email already exists')
        else:
            return render_template("newuser.html", fail='Invalid details')


@app.route('/updateClientInfo', methods=['POST', 'GET'])
def updateClient():
    if request.method != 'POST':
        return redirect('/clientPage')

    if dbHandler.updateClient(
        dbHandler.getClientId(session['email']),
        request.form['name'],
        request.form['mobile'],
        request.form['city'],
        request.form['email'],
        request.form['password']
    ):
        session['email'] = request.form['email']
        return render_template('client.html', success='Profile updated successfully')

    else:
        return render_template('client.html', fail='Invalid details')


@app.route('/addNewWorker', methods=['POST', 'GET'])
def addNewWorker():
    if request.method != 'POST':
        return redirect('/joinAsWorker')

    if dbHandler.insertWorker(
        request.form['name'],
        request.form['mobile'],
        request.form['title'],
        request.form['city'],
        request.form['email'],
        request.form['password']
    ):
        return render_template('login.html', success='Registration done successfully, now log in')

    else:
        if dbHandler.isWorkerExist(request.form['email']):
            return render_template("newaccount.html", fail='An account with this email already exists')
        else:
            return render_template("newaccount.html", fail='Invalid details')


@app.route('/logOut', methods=['POST', 'GET'])
def logItOut():
    session.clear()
    return redirect('/signInPage')


if __name__ == '__main__':
    app.run(debug=True)