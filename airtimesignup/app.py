from flask import Flask, render_template, jsonify
from airtimesignup.database import db_session
from airtimesignup.checkvat import get_vat_info

app = Flask(__name__)


## Database teardown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/")
def show():
    return render_template('index.html')

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