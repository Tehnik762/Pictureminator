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

###################################################################################
### LGBM Classifier
###################################################################################
def print_usage_lgbm():
    print("""
    Usage of 3classifiers.py:
        from 3classifiers import lgbm_model
    Usage example:
        best_model = lgbm_model(X_train, y_train, param_grid)

   Predefined examples:          
          param_lgbm = {
                'n_estimators': range(100, 400, 50), 
                'num_leaves': range(20, 40, 5), 
                'min_child_samples': range(1, 20, 2)}
    """)

param_lgbm = {
    'n_estimators': range(100, 400, 50), 
    'num_leaves': range(20, 40, 5), 
    'min_child_samples': range(1, 20, 2)}


def lgbm_model(X_train, y_train, param_lgbm):
   
    # Creating a pipeline with LightGBM
    full_pipeline_lgbm = make_pipeline(
        SimpleImputer(), 
        MinMaxScaler(), 
        lgb.LGBMClassifier()
    )

    # Parameter grid for LightGBM
    param_grid_lgbm = {
        f'lgbmclassifier__{key}': value if not isinstance(value, list) else value
        for key, value in param_lgbm.items()
    }


    # GridSearchCV for LightGBM
    search_lgbm = GridSearchCV(
        full_pipeline_lgbm,
        param_grid_lgbm,
        cv=10,
        verbose=1,
        n_jobs=multiprocessing.cpu_count() - 1
    )
    
    # Timing the fit operation
    start_time = time.time()
    search_lgbm.fit(X_train, y_train)
    end_time = time.time()
    
    total_time = end_time - start_time
    minutes = total_time // 60
    seconds = total_time % 60
    print(f"Time taken to train the model: {int(minutes)} minutes and {seconds:.2f} seconds")

    print(f"Best parameters: {search_lgbm.best_params_}")
    print(f"Best score: {search_lgbm.best_score_}")

    return search_lgbm

###################################################################################


###################################################################################
### ExtraTrees Classifier
###################################################################################
def print_usage_et():
    print("""
    Usage of 3classifiers.py:
        from 3classifiers import extratrees_model
    Usage example:
        best_model = extratrees_model(X_train, y_train, param_grid)

    Predefined examples:                 
        param_et = {
            'n_estimators': range(100, 400, 50), 
            'min_samples_split': range(2, 19, 2), 
            'min_samples_leaf': range(1, 13, 2)}
    """)


param_et = {
    'n_estimators': range(100,400,50),
    'min_samples_split': range(2,19,2),
    'min_samples_leaf': range(1,13,2),
}

def extratrees_model(X_train, y_train, param_et):
    # Creating a pipeline with ExtraTreesClassifier
    full_pipeline = make_pipeline(
        SimpleImputer(), 
        MinMaxScaler(), 
        ExtraTreesClassifier()
    )

    # Parameter grid for ExtraTreesClassifier
    param_grid = {
        f'extratreesclassifier__{key}': value if not isinstance(value, list) else value
        for key, value in param_et.items()
    }

    # GridSearchCV for ExtraTreesClassifier
    search_et = GridSearchCV(
        full_pipeline,
        param_grid,
        cv=10,
        verbose=1,
        n_jobs=multiprocessing.cpu_count() - 1
    )
    
    # Timing the fit operation
    start_time = time.time()
    search_et.fit(X_train, y_train)
    end_time = time.time()
    
    total_time = end_time - start_time
    minutes = total_time // 60
    seconds = total_time % 60
    print(f"Time taken to train the model: {int(minutes)} minutes and {seconds:.2f} seconds")

    print(f"Best parameters: {search_et.best_params_}")
    print(f"Best score: {search_et.best_score_}")

    return search_et
###################################################################################

###################################################################################
### CatBoost Classifier
###################################################################################
def print_usage_cb():
    print("""
    Usage of 3classifiers.py:
        from 3classifiers import catboost_model
    Usage example:
        best_model = catboost_model(X_train, y_train, param_grid)

    Predefined examples:                 
        param_cb = {
            'iterations': range(100, 400, 50), 
            'depth': range(4, 10, 2), 
            'l2_leaf_reg': np.logspace(-20, -19, 3)}
    """)


param_cb ={
    'iterations': range(100, 400, 50),
    'depth': range(4, 10, 2),
    'l2_leaf_reg': np.logspace(-20, -19, 3), 
}


def catboost_model(X_train, y_train, param_cb):
    # Creating a pipeline with CatBoostClassifier
    full_pipeline_catboost = make_pipeline(
        SimpleImputer(), 
        MinMaxScaler(), 
        CatBoostClassifier(verbose=0)
    )

    # Parameter grid for CatBoostClassifier
    param_grid_catboost = {
        f'catboostclassifier__{key}': value if not isinstance(value, list) else value
        for key, value in param_cb.items()
    }

    # GridSearchCV for CatBoostClassifier
    search_catboost = GridSearchCV(
        full_pipeline_catboost,
        param_grid_catboost,
        cv=10,
        verbose=1,
        n_jobs=multiprocessing.cpu_count() - 1
    )
    
    # Timing the fit operation
    start_time = time.time()
    search_catboost.fit(X_train, y_train)
    end_time = time.time()
    
    total_time = end_time - start_time
    minutes = total_time // 60
    seconds = total_time % 60
    print(f"Time taken to train the model: {int(minutes)} minutes and {seconds:.2f} seconds")
    
    print(f"Best parameters: {search_catboost.best_params_}")
    print(f"Best score: {search_catboost.best_score_}")

    return search_catboost
###################################################################################

###################################################################################
### AdaBoost Classifier
###################################################################################


def print_usage_adaboost():
    print("""
    Usage of 3classifiers.py:
        from 3classifiers import adaboost_model
    Usage example:
        best_model = adaboost_model(X_train, y_train, param_adaboost)

   Predefined examples:          
          param_adaboost = {
                'n_estimators': range(50, 400, 50), 
                'learning_rate': [0.01, 0.1, 1.0],
                'estimator__max_depth': [1, 2, 3]}
    """)

param_adaboost = {
    'n_estimators': range(50, 400, 50), 
    'learning_rate': [0.01, 0.1, 1.0],
    'estimator__max_depth': [1, 2, 3]
}

def adaboost_model(X_train, y_train, param_adaboost):
    # Creating a pipeline with AdaBoost
    full_pipeline_adaboost = make_pipeline(
        SimpleImputer(), 
        MinMaxScaler(), 
        AdaBoostClassifier(estimator=DecisionTreeClassifier())
    )

    # Parameter grid for AdaBoost
    param_grid_adaboost = {
        f'adaboostclassifier__{key}': value if not isinstance(value, list) else value
        for key, value in param_adaboost.items()
    }

    # GridSearchCV for AdaBoost
    search_adaboost = GridSearchCV(
        full_pipeline_adaboost,
        param_grid_adaboost,
        cv=10,
        verbose=1,
        n_jobs=multiprocessing.cpu_count() - 1
    )
    
    # Timing the fit operation
    start_time = time.time()
    search_adaboost.fit(X_train, y_train)
    end_time = time.time()
    
    total_time = end_time - start_time
    minutes = total_time // 60
    seconds = total_time % 60
    print(f"Time taken to train the model: {int(minutes)} minutes and {seconds:.2f} seconds")

    print(f"Best parameters: {search_adaboost.best_params_}")
    print(f"Best score: {search_adaboost.best_score_}")

    return search_adaboost
###################################################################################