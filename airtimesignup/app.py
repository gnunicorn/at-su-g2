#* encoding=utf-8
from flask import (Flask, render_template, jsonify, request,
                   session, redirect, url_for)
from flask.ext.login import LoginManager
from flask.ext.browserid import BrowserID

from yaml import load, YAMLError

from airtimesignup.user_management import (get_user_by_id,
                                           get_user_from_browserid)
from airtimesignup.database import db_session
from airtimesignup.checkvat import get_vat_info
from airtimesignup import config

import math

app = Flask(__name__, static_folder='../static')


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    if request.method == "POST":
        session["checkout_context"] = {
            "package": airtime['Packages'][request.form.get("package", "starter")],
            "expert_support": airtime['Extras']["expert_support"].get(request.form.get("expert_support", ""), ""),
            "extra_streaming": airtime['Extras']["extra_streaming"].get(request.form.get("extra_streaming", ""), ""),
        }
        return redirect(url_for("checkout"))

    if not "checkout_context" in session or not session["checkout_context"]:
        return redirect("/packages")

    context = session["checkout_context"]
    total = sum([context[x]["price"]
                for x in ('package', 'expert_support', 'extra_streaming')
                if context.get(x, None)])
    context["sum_total"] = total
    context["vat"] = math.ceil(total * 19) / 100.0
    context["total"] = math.ceil(total * 119) / 100.0
    return render_template('checkout.html', **context)


@app.route("/")
@app.route("/packages")
def show_packages():
    session["checkout_context"] = {}
    return render_template('packages.html',
                           packages=airtime['Packages'])


@app.route("/packages/<string:package>")
def show_package(package):
    return render_template('packages/{0}.html'.format(package),
                           package=airtime['Packages'][package],
                           extras=airtime['Extras'])


@app.route("/checkvat/<string:vat>")
def checkvat(vat):
    valid, info = get_vat_info(vat)
    if not valid:
        return jsonify({"valid": False})
    return jsonify({"valid": True,
                    "name": info.name,
                    "country": info.countryCode,
                    "vatNumber": info.vatNumber,
                    "address": info.address
                    })


# default fallback
@app.route("/<string:template>")
def show_template(template):
    return render_template(template + '.html')


#### APP CONFIGURATION

## Database teardown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Read yaml file
with open('airtime.yml', 'r') as f:
    try:
        airtime = load(f)
    except yaml.YAMLError, exc:
        print "Error in airtime.yml configuration file:", exc

# This should go into a config file
app.secret_key = config.SESSION_SECRET

# Add Login Management
login_manager = LoginManager()
login_manager.user_loader(get_user_by_id)
login_manager.init_app(app)

browser_id = BrowserID()
browser_id.user_loader(get_user_from_browserid)
browser_id.init_app(app)
