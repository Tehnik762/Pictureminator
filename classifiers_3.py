from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import GridSearchCV
from catboost import CatBoostClassifier
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
        best_model = lgbm_model(X_train, y_train, best_param)
    
    Ensure you have the following parameters ready before calling lgbm_model:
    - X_train: Training features
    - y_train: Training labels
    - best_param: Dictionary of parameters for LightGBM

   Predefined examples:          
          best_param_lgbm = {
                'n_estimators': range(100, 400, 50), 
                'num_leaves': range(20, 40, 5), 
                'min_child_samples': range(1, 20, 2)}
    """)

best_param_lgbm = {
    'n_estimators': range(100, 400, 50), 
    'num_leaves': range(20, 40, 5), 
    'min_child_samples': range(1, 20, 2)}


def lgbm_model(X_train, y_train, best_param_lgbm):
   
    # Creating a pipeline with LightGBM
    full_pipeline_lgbm = make_pipeline(
        SimpleImputer(), 
        MinMaxScaler(), 
        lgb.LGBMClassifier()
    )

    # Parameter grid for LightGBM
    param_grid_lgbm = {
        f'lgbmclassifier__{key}': value if not isinstance(value, list) else value
        for key, value in best_param_lgbm.items()
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
        best_model = extratrees_model(X_train, y_train, best_param)
    
    Ensure you have the following parameters ready before calling extratrees_model:
    - X_train: Training features
    - y_train: Training labels
    - best_param: Dictionary of parameters for ExtraTreesClassifier

    Predefined examples:                 
        best_param_et = {
            'n_estimators': range(100, 400, 50), 
            'min_samples_split': range(2, 19, 2), 
            'min_samples_leaf': range(1, 13, 2)}
    """)


best_param_et = {
    'n_estimators': range(100,400,50),
    'min_samples_split': range(2,19,2),
    'min_samples_leaf': range(1,13,2),
}

def extratrees_model(X_train, y_train, best_param_et):
    # Creating a pipeline with ExtraTreesClassifier
    full_pipeline = make_pipeline(
        SimpleImputer(), 
        MinMaxScaler(), 
        ExtraTreesClassifier()
    )

    # Parameter grid for ExtraTreesClassifier
    param_grid = {
        f'extratreesclassifier__{key}': value if not isinstance(value, list) else value
        for key, value in best_param_et.items()
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
        best_model = catboost_model(X_train, y_train, best_param)
    
    Ensure you have the following parameters ready before calling catboost_model:
    - X_train: Training features
    - y_train: Training labels
    - best_param: Dictionary of parameters for CatBoostClassifier

    Predefined examples:                 
        best_param_cb = {
            'iterations': range(100, 400, 50), 
            'depth': range(4, 10, 2), 
            'l2_leaf_reg': np.logspace(-20, -19, 3)}
    """)


best_param_cb ={
    'iterations': range(100, 400, 50),
    'depth': range(4, 10, 2),
    'l2_leaf_reg': np.logspace(-20, -19, 3), 
}


def catboost_model(X_train, y_train, best_param_cb):
    # Creating a pipeline with CatBoostClassifier
    full_pipeline_catboost = make_pipeline(
        SimpleImputer(), 
        MinMaxScaler(), 
        CatBoostClassifier(verbose=0)
    )

    # Parameter grid for CatBoostClassifier
    param_grid_catboost = {
        f'catboostclassifier__{key}': value if not isinstance(value, list) else value
        for key, value in best_param_cb.items()
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