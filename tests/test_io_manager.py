from config.io_manager import read_pool_model, write_pool_model
from config.io_manager import read_config, write_config
from config.admin import Admin
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


# Tests for io_manager.read_pool_model()

def test_io_read_pool_model_correct():
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
    handle = StringIO(str(pool_json).replace("'", '"'))

    pool_model = read_pool_model(handle, date(2022, 1, 1))
    pool_json["reservations"] = []

    assert PoolModel.to_json(pool_model) == pool_json
    assert pool_model.current_day == date(2022, 1, 1)


# Tests for io_manager.write_config()

def test_io_write_config_correct():
    handle = StringIO()
    config_json = {
        "current_day": {
            "day": 12,
            "month": 3,
            "year": 2023
        }
    }

    write_config(handle, Admin.from_json(config_json))
    saved_json = ast.literal_eval(handle.getvalue())

    assert config_json == saved_json


# Tests for io_manager.read_config()

def test_io_read_config_correct():
    config_json = {
        "current_day": {
            "day": 12,
            "month": 3,
            "year": 2023
        }
    }

    handle = StringIO(str(config_json).replace("'", '"'))
    admin = read_config(handle)

    assert Admin.to_json(admin) == config_json
