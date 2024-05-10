from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from catboost import CatBoostClassifier
from sklearn.pipeline import Pipeline
import lightgbm as lgb
import multiprocessing
import numpy as np
import time

param_lgbm = {
    'n_estimators': range(100, 400, 50),
    'num_leaves': range(20, 40, 5),
    'min_child_samples': range(1, 20, 2)}

param_et = {
    'n_estimators': range(100,400,50),
    'min_samples_split': range(2,19,2),
    'min_samples_leaf': range(1,13,2),
}


param_cb ={
    'iterations': range(100, 400, 50),
    'depth': range(4, 10, 2),
    'l2_leaf_reg': np.logspace(-20, -19, 3),
}

param_adaboost = {
    'n_estimators': range(50, 400, 50),
    'learning_rate': [0.01, 0.1, 1.0],
    'estimator__max_depth': [1, 2, 3]
}

def print_usage(classifier_type, param_grid):
    print(f"""
    Usage of 3classifiers.py:
        from 3classifiers import {classifier_type}_model
    Usage example:
        best_model = {classifier_type}_model(X_train, y_train, param_grid)

   Predefined examples:          
          param_{classifier_type} = {param_grid}
    """)


def train_model(X_train, y_train, param_grid, classifier_type, classifier):
    full_pipeline = make_pipeline(
        SimpleImputer(),
        MinMaxScaler(),
        classifier
    )

    param_grid_updated = {
        f'{classifier_type}__{key}': value if not isinstance(value, list) else value
        for key, value in param_grid.items()
    }

    search = GridSearchCV(
        full_pipeline,
        param_grid_updated,
        cv=10,
        verbose=1,
        n_jobs=multiprocessing.cpu_count() - 1
    )

    start_time = time.time()
    search.fit(X_train, y_train)
    end_time = time.time()

    total_time = end_time - start_time
    minutes = total_time // 60
    seconds = total_time % 60
    print(f"Time taken to train the model: {int(minutes)} minutes and {seconds:.2f} seconds")
    print(f"Best parameters: {search.best_params_}")
    print(f"Best score: {search.best_score_}")

    return search


def lgbm_model(X_train, y_train, param_lgbm):
    print_usage('lgbm', param_lgbm)
    return train_model(X_train, y_train, param_lgbm, 'lgbmclassifier', lgb.LGBMClassifier())


def extratrees_model(X_train, y_train, param_et):
    print_usage('extratrees', param_et)
    return train_model(X_train, y_train, param_et, 'extratreesclassifier', ExtraTreesClassifier())


def catboost_model(X_train, y_train, param_cb):
    print_usage('catboost', param_cb)
    return train_model(X_train, y_train, param_cb, 'catboostclassifier', CatBoostClassifier(verbose=0))


def adaboost_model(X_train, y_train, param_adaboost):
    print_usage('adaboost', param_adaboost)
    return train_model(X_train, y_train, param_adaboost, 'adaboostclassifier',
                       AdaBoostClassifier(estimator=DecisionTreeClassifier()))
