import os
import joblib
import pandas as pd


def sort_files(data, model, folder, source_fld="sort", debug=False,*args, **kwargs):
    """
    Function to sort images depending on the model
    Model will be searched in folder models with extension .model
    :param data: dataframe
    :param model:
    :param folder:
    :param args:
    :param kwargs:
    :return:
    """
    try:
        if debug: print(f"Loading model {model}.model")
        model = joblib.load(f"models/{model}.model")
    except Exception as e:
        print(f"Model {model} not found!")
        return 0
    filenames = data.pop("filename").to_list()

    if debug: print(f"Sorting {len(filenames)} images")
    predict = model.predict(data)
    data["filename"] = filenames
    for i in range(len(filenames)):
        if predict[i] == 1:
            try:
                if filenames[i] in os.listdir(source_fld):
                    os.rename(source_fld + "/" + filenames[i], f"{folder}/{filenames[i]}")
                    if debug: print(f"{filenames[i]} moved to {folder}")
                data = data.loc[data["filename"] != filenames[i]]
            except Exception as e:
                print(f"{filenames[i]} - {e} - {type(e)}")
    if debug: print(f"{len(data)} images left")
    return data
