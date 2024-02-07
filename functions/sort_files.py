import pandas as pd
import joblib

def sort_files(data, model, folder, *args, **kwargs):
    """
    Function to sort images depending on the model
    Model will be searched in folder models with extension .model
    :param data:
    :param model:
    :param folder:
    :param args:
    :param kwargs:
    :return:
    """
    try:
        model = joblib.load(f"./models/{model}.model")
    except Exception as e:
        print(f"Model {model} not found!")
        return 0


