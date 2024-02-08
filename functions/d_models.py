import joblib

def loadModels():
    blinked = joblib.load("./models/blinked_final.model")
    not_good = joblib.load("./models/not_good_final.model")
    superb = joblib.load("./models/superb_final.model")
    regular = joblib.load("./models/regular_final.model")

    return {
        "blinked": [blinked, 2],
        "not_good": [not_good, 1],
        "superb": [superb, 3],
        "regular": [regular, 2]
    }