from checkvat import get_vat_info
from flask import Flask, render_template, jsonify
app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)