from flask import Flask, render_template, session, redirect, json
from flask.globals import request

from DB_handler import *

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = 'try_again'

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
        if not saveSearch:
            return render_template("dashboard.html", Error="Currently no worker available")
        return render_template("dashboard.html", jobList=saveSearch)
    return redirect('/signInPage')


@app.route('/searchresult', methods=['POST', 'GET'])
def searchedResults():
    if session.get('loggedin') == 'client':
        saveSearch = dbHandler.getSearchedjobs(request.form['searchText'])
        if not saveSearch:
            return render_template("dashboard.html", Error="Currently no worker available")
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
        request.form['status'], request.form['email'], request.form['password'])
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
    return render_template("login.html", fail='Invalid credentials')


@app.route('/addNewClient', methods=['POST', 'GET'])
def addNewClient():
    if request.method != 'POST':
        return redirect('/joinAsClient')
    if dbHandler.insertClient(request.form['name'], request.form['mobile'],
                               request.form['city'], request.form['email'], request.form['password']):
        return render_template('login.html', success='Registration done successfully, now log in')
    if dbHandler.isClinetExist(request.form['email']):
        return render_template("newuser.html", fail='An account with this email already exists')
    return render_template("newuser.html", fail='Invalid details')


@app.route('/updateClientInfo', methods=['POST', 'GET'])
def updateClient():
    if request.method != 'POST':
        return redirect('/clientPage')
    if dbHandler.updateClient(dbHandler.getClientId(session['email']),
                               request.form['name'], request.form['mobile'],
                               request.form['city'], request.form['email'], request.form['password']):
        session['email'] = request.form['email']
        return render_template('client.html', success='Profile updated successfully')
    return render_template('client.html', fail='Invalid details')


@app.route('/addNewWorker', methods=['POST', 'GET'])
def addNewWorker():
    if request.method != 'POST':
        return redirect('/joinAsWorker')
    if dbHandler.insertWorker(request.form['name'], request.form['mobile'],
                               request.form['title'], request.form['city'],
                               request.form['email'], request.form['password']):
        return render_template('login.html', success='Registration done successfully, now log in')
    if dbHandler.isWorkerExist(request.form['email']):
        return render_template("newaccount.html", fail='An account with this email already exists')
    return render_template("newaccount.html", fail='Invalid details')


@app.route('/addNewJob', methods=['GET', 'POST'])
def addNewJob():
    if request.method != 'POST':
        return redirect('/workerPage')
    if dbHandler.insertNewJob(dbHandler.getWorkerId(session['email']),
                               request.form['title'], request.form['rate'], request.form['desc']):
        return render_template('worker.html', success='Job Added')
    return render_template('worker.html', fail='Request Denied')


@app.route('/updateWorkerInfo', methods=['POST', 'GET'])
def updateWorker():
    if request.method != 'POST':
        return redirect('/workerPage')
    if dbHandler.updateWorker(dbHandler.getWorkerId(session['email']),
                               request.form['name'], request.form['mobile'],
                               request.form['city'], request.form['title'],
                               request.form['email'], request.form['password']):
        session['email'] = request.form['email']
        return render_template('worker.html', edit_success='Profile updated successfully')
    return render_template('worker.html', edit_fail='Update failed — check your details')


@app.route('/logOut', methods=['POST', 'GET'])
def logItOut():
    session.clear()
    return redirect('/signInPage')


@app.route('/getInfo', methods=['GET'])
def getPersonDetails():
    role = session.get('loggedin')
    if role == 'worker':
        return json.dumps(dbHandler.getWorkerInfo(session['email']))
    elif role in ('client', 'admin'):
        return json.dumps(dbHandler.getClientInfo(session['email']))
    return json.dumps([])


@app.route('/jobDetails', methods=['GET', 'POST'])
def jobDetails():
    return json.dumps(dbHandler.getJobDetails(request.args.get('id')))


@app.route('/sendHireRequest', methods=['GET', 'POST'])
def sendHiringRequest():
    if request.method != 'POST':
        return redirect('/dashboardPage')
    dbHandler.sendRequest(request.form['jid'], request.form['wid'],
                          dbHandler.getClientId(session['email']))
    return redirect('/dashboardPage')


@app.route('/requestData', methods=['GET'])
def getRequestedData():
    return json.dumps(dbHandler.getRequestedJobs(dbHandler.getClientId(session['email'])))


@app.route('/confirmData', methods=['GET'])
def getAcceptedData():
    return json.dumps(dbHandler.getConfirmJobs(dbHandler.getClientId(session['email'])))


@app.route('/requestDataForWorker', methods=['GET'])
def getRequestedDataForWorker():
    return json.dumps(dbHandler.checkRequestedJobs(dbHandler.getWorkerId(session['email'])))


@app.route('/getMyJobs', methods=['GET'])
def getMyJobs():
    return json.dumps(dbHandler.checkMyJobs(dbHandler.getWorkerId(session['email'])))


@app.route('/confirmDataForWorker', methods=['GET'])
def getConfirmDataForWorker():
    return json.dumps(dbHandler.checkConfirmJobs(dbHandler.getWorkerId(session['email'])))


@app.route('/cancelRequest', methods=['POST'])
def cancelRequest():
    if dbHandler.cancelRequest(request.form['worker_id'], request.form['job_id'], request.form['client_id']):
        return json.dumps({"msg": "Canceled"})
    return json.dumps({"msg": "Can not Cancel"})


@app.route('/deleteMyJob', methods=['POST'])
def deleteMyJob():
    if dbHandler.deletejobP(request.form['job_id']):
        return json.dumps({"msg": "Deleted"})
    return json.dumps({"msg": "Cannot Delete"})


@app.route('/closeTheJob', methods=['POST'])
def closeTheJob():
    if dbHandler.jobClose(request.form['worker_id'], request.form['job_id'],
                           request.form['client_id'], request.form['star']):
        return json.dumps({"msg": "Job is closed"})
    return json.dumps({"msg": "Job is still in progress"})


@app.route('/acceptRequest', methods=['POST'])
def acceptRequest():
    if dbHandler.acceptRequest(request.form['worker_id'], request.form['job_id'], request.form['client_id']):
        return json.dumps({"msg": "Accepted"})
    return json.dumps({"msg": "Job is not confirmed"})


# ------------------------------------------------------------------ admin
@app.route('/admin/getAllWorkers', methods=['GET'])
def getAllWorkers():
    if session.get('loggedin') != 'admin':
        return json.dumps([])
    return json.dumps(dbHandler.getAllWorkers())


@app.route('/admin/getAllClients', methods=['GET'])
def getAllClients():
    if session.get('loggedin') != 'admin':
        return json.dumps([])
    return json.dumps(dbHandler.getAllClients())


@app.route('/admin/getAllJobs', methods=['GET'])
def getAllJobs():
    if session.get('loggedin') != 'admin':
        return json.dumps([])
    return json.dumps(dbHandler.getjobs())


if __name__ == '__main__':
    app.run(debug=True)