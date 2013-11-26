from yaml import load, YAMLError

DEBUG = True
DATABASE_URL = "sqlite:///test.db"
SESSION_SECRET = "asdfadsfadlkfj9ur4q32oi5uafp[nlv"
PAYMENT_URL = "/payment/fake?callback={}"


# Read yaml file
with open('airtime.yml', 'r') as f:
    try:
        airtime = load(f)
    except YAMLError as exc:
        print("Error in airtime.yml configuration file:{}".format(exc))


try:
    from local_config import *
except ImportError:
    print("Loading without local config")
