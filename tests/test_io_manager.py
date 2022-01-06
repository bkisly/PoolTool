from config.io_manager import write_pool_model
from io import StringIO
from model.pool_model import PoolModel
from datetime import date
import ast


# Tests for io_manager.write_pool_model()

def test_io_write_pool_model_correct():
    handle = StringIO()
    pool_json = {
        "name": "MyPool",
        "lanes_amount": 5,
        "working_hours": {
            "0": {
                "begin": {
                    "hour": 9,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 0
                }
            },
            "1": {
                "begin": {
                    "hour": 10,
                    "minute": 0
                },
                "end": {
                    "hour": 18,
                    "minute": 30
                }
            },
        },
        "price_list": [
            {
                "service": 0,
                "day": 0,
                "hours_range": {
                    "begin": {
                        "hour": 9,
                        "minute": 0
                    },
                    "end": {
                        "hour": 18,
                        "minute": 0
                    }
                },
                "price": {
                    "zl": 2,
                    "gr": 50
                }
            },
            {
                "service": 1,
                "day": 0,
                "hours_range": {
                    "begin": {
                        "hour": 9,
                        "minute": 0
                    },
                    "end": {
                        "hour": 18,
                        "minute": 0
                    }
                },
                "price": {
                    "zl": 2,
                    "gr": 50
                }
            },
            {
                "service": 0,
                "day": 1,
                "hours_range": {
                    "begin": {
                        "hour": 10,
                        "minute": 0
                    },
                    "end": {
                        "hour": 18,
                        "minute": 30
                    }
                },
                "price": {
                    "zl": 2,
                    "gr": 50
                }
            },
            {
                "service": 1,
                "day": 1,
                "hours_range": {
                    "begin": {
                        "hour": 10,
                        "minute": 0
                    },
                    "end": {
                        "hour": 18,
                        "minute": 30
                    }
                },
                "price": {
                    "zl": 2,
                    "gr": 50
                }
            },
        ]
    }

    pool_model = PoolModel(pool_json, date.today())
    pool_json["reservations"] = []

    write_pool_model(handle, pool_model)
    saved_dict = ast.literal_eval(handle.getvalue())

    assert saved_dict == pool_json
