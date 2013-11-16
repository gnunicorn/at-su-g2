
DEBUG = True
DATABASE_URL = "sqlite:///test.db"
SESSION_SECRET = "asdfadsfadlkfj9ur4q32oi5uafp[nlv"

PACKAGES = {
    "starter": {
        "name": "Starter",
        "price": 24.95
    },
    "plus": {
        "name": "Plus",
        "price": 49.95
    },
    "premium": {
        "name": "Premium",
        "price": 79.95
    },
    "enterprise": {
        "name": "Enterprise",
        "price": 149.95
    }
}

EXTRAS = {
    "extra_streaming": {
        "silver": {
            "name": "Silver Streaming",
            "price": 17.48
        },
        "gold": {
            "name": "Gold Streaming",
            "price": 32.48
        },
        "premium": {
            "name": "Premium Streaming",
            "price": 49.95
        }

    },
    "expert_support": {
        "silver": {
            "name": "Silver",
            "price": 99.95
        },
        "gold": {
            "name": "Gold",
            "price": 249.95
        },
        "platinum": {
            "name": "Platinum",
            "price": 499.95
        }

    }
}

try:
    from local_config import *
except ImportError:
    print("Loading without local config")