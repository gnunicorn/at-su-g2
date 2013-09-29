from airtimesignup.app import app
from airtimesignup import config


if __name__ == "__main__":
    app.run(debug=config.DEBUG)