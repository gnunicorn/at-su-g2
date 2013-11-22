
DEBUG = True
DATABASE_URL = "sqlite:///test.db"
SESSION_SECRET = "asdfadsfadlkfj9ur4q32oi5uafp[nlv"

try:
    from local_config import *
except ImportError:
    print("Loading without local config")
