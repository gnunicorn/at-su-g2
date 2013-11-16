from flask import Flask, render_template, jsonify, session, request, url_for, redirect
from flask.ext.login import LoginManager
from flask.ext.browserid import BrowserID

from airtimesignup.database import db_session
from airtimesignup.checkvat import get_vat_info

from airtimesignup.user_management import get_user_from_browserid, get_user_by_id


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


@app.route("/packages/<string:package>")
def show_package(package):
    return render_template('packages/{0}.html'.format(package))


@app.route("/checkvat/<string:vat>")
def checkvat(vat):
    valid, info = get_vat_info(vat)
    if not valid:
        jsonify({"valid": False})
    return jsonify({"valid": True,
                    "name": info.name,
                    "country": info.countryCode,
                    "vatNumber": info.vatNumber,
                    "address": info.address
                    })


# This should go into a config file
app.secret_key = 'ChangeThis'

login_manager = LoginManager()
login_manager.user_loader(get_user_by_id)
login_manager.init_app(app)

browser_id = BrowserID()
browser_id.user_loader(get_user_from_browserid)
browser_id.init_app(app)
