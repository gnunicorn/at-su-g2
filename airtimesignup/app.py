from flask import Flask, render_template, jsonify, session, request, url_for, redirect
from airtimesignup.database import db_session
from airtimesignup.checkvat import get_vat_info

app = Flask(__name__, static_folder='../static')


## Database teardown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/")
def show():
    return render_template('index.html')

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    if 'username' in session:
        return render_template('checkout.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('checkout'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('checkout'))

@app.route("/packages/<string:package>")
def show_package(package):
    return render_template('packages/{0}.html'.format(package))


@app.route("/checkvat/<string:vat>")
def checkvat(vat):
    valid, info = get_vat_info(vat)
    if not valid:
        jsonify({"valid": False})
    return jsonify({
            "valid": True,
            "name": info.name,
            "country": info.countryCode,
            "vatNumber": info.vatNumber,
            "address": info.address
        })


# This should go into a config file
app.secret_key = 'ChangeThis'
