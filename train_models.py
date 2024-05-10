import time
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
import multiprocessing
import joblib
from sklearn.feature_selection import RFECV
import classifiers_3 as c3

logging.basicConfig(level=logging.INFO, filename='train.log', filemode='w')
initial_time = time.time()
logging.info(f"Starting at {initial_time}")
test = pd.read_csv("./images/test/test.csv")
filenames = test.pop("filename")

from_labels = ["blinked", "docs", "not_good", "regular", "screenshots", "screenshots_ph", "superb"]

for label in from_labels:
    main_class_pd = pd.read_csv("./images/" + label + "/" + label + ".csv")
    main_class_pd[label] = 1

    others = {}
    for label2 in from_labels:
        if label2 != label:
            others[label2] = pd.read_csv("./images/" + label2 + "/" + label2 + ".csv")
            others[label2][label] = 0
    others = pd.concat(others.values(), ignore_index=True)
    whole_docs = pd.concat([others, main_class_pd],
                           ignore_index=True)
    whole_docs = whole_docs.drop(columns=["filename"])
    whole_docs = whole_docs.fillna(0)
    y = whole_docs.pop(label)
    X_train, X_test, y_train, y_test = train_test_split(whole_docs, y, test_size=0.15, random_state=42)
    search_scr = c3.extratrees_model(X_train, y_train, c3.param_et)
    search_cb = c3.catboost_model(X_train, y_train, c3.param_cb)
    search_lgbm = c3.lgbm_model(X_train, y_train, c3.param_lgbm)
    search_ab = c3.adaboost_model(X_train, y_train, c3.param_adaboost)

    best_score_et = search_scr.best_score_
    best_score_lgbm = search_lgbm.best_score_
    best_score_catboost = search_cb.best_score_
    best_score_adaboost = search_ab.best_score_

    # Create a list to display the results
    results = [
        ('ExtraTrees', best_score_et),
        ('LightGBM', best_score_lgbm),
        ('CatBoost', best_score_catboost),
        ('AdaBoost', best_score_adaboost)
    ]
    logging.info(f"Results for {label}: {results}")
    # Print the results in a tabular format
    print(f"{'Classifier':<15}{f'Best Score - {label}'}")
    for name, score in results:
        print(f"{name:<15}{score:.4f}")

    results = [search_scr, search_lgbm,
               search_cb, search_ab]

    results_with_identifiers = [
        (search_scr, 'scr'),
        (search_lgbm, 'lgbm'),
        (search_cb, 'cb'),
        (search_ab, 'ab')
    ]

    classifier_mapping = {
        'scr': 'ExtraTrees',
        'lgbm': 'LightGBM',
        'cb': 'CatBoost',
        'ab': 'AdaBoost'
    }

    named_steps_estimator = {
        'scr': 'extratreesclassifier',
        'lgbm': 'lgbmclassifier',
        'cb': 'catboostclassifier',
        'ab': 'adaboostclassifier'
    }

    best_model, best_identifier = results_with_identifiers[0]

    for model, identifier in results_with_identifiers[1:]:
        if model.best_score_ > best_model.best_score_:
            best_model = model
            best_identifier = identifier

    # Use best_identifier to get the classifier name from the mapping
    classifier_name = classifier_mapping.get(best_identifier, 'Unknown')
    nsteps = named_steps_estimator.get(best_identifier)

    prediction = best_model.predict(test)

    result = pd.DataFrame()
    result['filename'] = filenames
    result['prediction'] = prediction

    result.loc[(result.prediction == 1) & (result.filename.str.contains(label)), "metric"] = "true"
    result.loc[(result.prediction == 0) & (result.filename.str.contains(label)), "metric"] = "FN"
    result.loc[(result.prediction == 0) & (~result.filename.str.contains(label)), "metric"] = "not true"
    result.loc[(result.prediction == 1) & (~result.filename.str.contains(label)), "metric"] = "FP"

    print(f"Confusion Matrix for {label} classifier: ")
    print(result.groupby("metric").count())

    logging.info(f"Confusion Matrix for {label} classifier: ")
    logging.info(result.groupby("metric").count())

    best_estimator = best_model.best_estimator_
    search_RFE = RFECV(best_estimator.named_steps[nsteps], cv=10, scoring="accuracy",
                       n_jobs=multiprocessing.cpu_count() - 1, verbose=3)
    search_RFE.fit(X_train, y_train)

    prediction = search_RFE.predict(test)

    result = pd.DataFrame()
    result['filename'] = filenames
    result['prediction'] = prediction

    result.loc[(result.prediction == 1) & (result.filename.str.contains(label)), "metric"] = "true"
    result.loc[(result.prediction == 0) & (result.filename.str.contains(label)), "metric"] = "FN"
    result.loc[(result.prediction == 0) & (~result.filename.str.contains(label)), "metric"] = "not true"
    result.loc[(result.prediction == 1) & (~result.filename.str.contains(label)), "metric"] = "FP"

    print(f"Confusion Matrix for {label} classifier after RFE: ")
    print(result.groupby("metric").count())

    logging.info(f"Confusion Matrix for {label} classifier after RFE: ")
    logging.info(result.groupby("metric").count())

    model_path = f"./models/{label}_final_{classifier_name}.model"
    joblib.dump(search_RFE, model_path)

    print(f"Model saved successfully at {model_path}")

end_time = time.time()
total_time = end_time - initial_time
minutes = total_time // 60
seconds = total_time % 60
hours = minutes // 60
minutes = minutes % 60
print(f"Time taken to train the model: {int(hours)} hours, {int(minutes)} minutes and {seconds:.2f} seconds")