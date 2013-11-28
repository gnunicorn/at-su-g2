#* encoding=utf-8
from flask import (Flask, render_template, jsonify, request,
                   session, redirect, url_for, json)
from flask.ext.login import LoginManager, current_user, login_required
from flask.ext.browserid import BrowserID

from airtimesignup.user_management import (get_user_by_id,
                                           get_user_from_browserid)
from airtimesignup.database import db_session
from airtimesignup.checkvat import get_vat_info
from airtimesignup.models import Order
from airtimesignup import config

import urllib2

import math

app = Flask(__name__, static_folder='../static')


## HELPER FUNCTIONS
def _extract_extras(context):
    return dict([(key, config.airtime["Extras"][key]['options'][int(context[key])])
                 for key in config.airtime["Extras"].keys()
                 if key in context])


def _currency_data(currency):
    if currency:
        return filter(lambda x: x['label'] == currency,
                      config.airtime['Currencies'])[0]
    else:
        return config.airtime['Currencies'][0]

def _package_data(package):
    return filter(lambda x: x['label'] == package,
                      config.airtime['Packages'])[0]


def check_domain_available(domain):
    if not config.airtime["APIs"]["domain_check"]:
        return True

    naked_url = config.airtime["APIs"]["domain_check"]
    url = naked_url.format(domain)
    try:
        if json.loads(urllib2.urlopen(url).read())["available"]:
            return True
    except Exception as exc:
        print("Error checking domain: {}".format(exc))
        return False


def require_checkout_context(func):
    def wrapped(*args, **kwargs):
        if "checkout_context" not in session \
           or not session["checkout_context"]:
            return redirect("/packages")
        return func(*args, **kwargs)
    wrapped.func_name = func.func_name
    return wrapped


@app.route("/prepare_checkout", methods=["POST"])
def prepare_checkout():
    session["checkout_context"] = ctx = _extract_extras(request.form)
    ctx["package"] = _package_data(request.form.get("package",
                                                    config.airtime['Packages'][0]['label']))
    ctx["currency"] = _currency_data(request.form.get('currency', None))
    return redirect(url_for("checkout"))


@app.route("/checkout", methods=['GET'])
@require_checkout_context
def checkout():
    context = dict(session["checkout_context"])
    keys = filter(lambda x: "price" in context[x], context.keys())
    total = sum([context[x]["price"][context["currency"]["label"]] for x in keys])
    context["sum_total"] = total
    context["vat"] = math.ceil(total * 19) / 100.0
    context["total"] = math.ceil(total * 119) / 100.0
    return render_template('checkout.html', **context)


@app.route("/confirm", methods=['POST'])
@require_checkout_context
@login_required
def confirm():
    order = Order(user_id=current_user.id, state="to_confirm")

    if request.form.get("bill-selector") == "vat":
        valid, info = get_vat_info(request.form.get("vat-nr"))
        if not valid:
            return redirect(url_for(".checkout"))

        order.address = "{0}\n{1}".format(info.name, info.address)
        order.vat_addr = "{0}{1}".format(info.countryCode, info.vatNumber)

    elif request.form.get("address"):
        order.address = request.form.get("address")
    else:
        # FIXME: give good user message
        return redirect(url_for(".checkout"))

    if check_domain_available(request.form.get("domain")):
        order.domain = request.form.get("domain")
    else:
        # FIXME: give good user message
        return redirect(url_for(".checkout"))

    ctx = session["checkout_context"]
    currency = ctx["currency"]

    keys = filter(lambda x: "price" in ctx[x], ctx.keys())
    sum_total = sum([ctx[x]["price"][currency["label"]] for x in keys])
    if order.vat_addr:
        order.total = sum_total
    else:
        order.vat = math.ceil(sum_total * 19) / 100.0
        order.total = sum_total + order.vat

    order.details = json.dumps(ctx)
    db_session.add(order)
    db_session.commit()

    return render_template("confirm.html", sum_total=sum_total, order=order, **ctx)


@app.route("/payment", methods=['POST'])
@require_checkout_context
def start_payment():
    order = Order.query.get(request.form["order_id"])
    if not order or order.state not in ("to_confirm", "in_payment"):
        raise ValueError()

    order.state = "in_payment"
    db_session.add(order)
    db_session.commit()

    callback_url = url_for(".payment_callback",
                           payment_id=order.id, _external=True)
    return redirect(config.PAYMENT_URL.format(callback_url))


@app.route("/payment/fake")
def fake_payment():
    return redirect(request.args["callback"])


@app.route("/payment/<string:payment_id>/callback/")
def payment_callback(payment_id):
    # FIXME: needs to check against the third-party
    order = Order.query.get(payment_id)
    if not order or order.state != "in_payment":
        raise ValueError()

    order.state = "paid"
    db_session.add(order)
    db_session.commit()

    paid_callback = config.airtime["APIs"]["paid_callback"]
    details = json.loads(order.details)
    if paid_callback:
        for key in ("created", "updated", "domain", "state", "address",
                    "vat_addr", "currency", "total", "total_vat"):
            details[key] = getattr(details, key)

        req = urllib2.Request(paid_callback, json.dumps(details),
                              {'Content-Type': 'application/json'})
        urllib2.urlopen(req).read()

    return render_template("end_confirm.html", order=order, **details)    



@app.route("/update_currency", methods=['POST'])
def update_currency():
    return redirect(url_for("show_packages",
                            currency=request.form.get('currency')))

@app.route("/packages")
def show_packages():
    session["checkout_context"] = {}
    return render_template('packages.html',
                           packages=config.airtime['Packages'],
                           currencies=config.airtime['Currencies'],
                           selected_currency=_currency_data(request.args.get('currency',
                                                                            None)))


@app.route("/packages/<string:package>")
def show_package(package):
    return render_template('/packages/package.html',
                           package=_package_data(package),
                           extras=config.airtime['Extras'],
                           currency=_currency_data(request.args.get('currency',
                                                                    None)))


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


@app.route("/checkdomain/<string:domain>")
def checkdomain(domain):
    return jsonify({"valid": check_domain_available(domain)})


# default fallback
@app.route("/<string:template>")
def show_template(template):
    return render_template(template + '.html')


#### APP CONFIGURATION

## Database teardown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# This should go into a config file
app.secret_key = config.SESSION_SECRET
app.add_url_rule("/", endpoint='/', redirect_to="/packages")

# Add Login Management
login_manager = LoginManager()
login_manager.user_loader(get_user_by_id)
login_manager.init_app(app)

browser_id = BrowserID()
browser_id.user_loader(get_user_from_browserid)
browser_id.init_app(app)
