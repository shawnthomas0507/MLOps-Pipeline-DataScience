import os 
import sys 
from networksecurity.entity.artifact_entity import DataTransformationArtifact,ClassificationMetricArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils.utils import read_yaml,write_yaml,save_numpy_array_data,save_object,load_object,load_numpy_array_data,evaluate_models

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier
)
import mlflow
import dagshub
dagshub.init(repo_owner='shawnthomas0507', repo_name='networksecurity', mlflow=True)


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
        
    

    def track_mlflow(self,best_model,classificationmetric):

        with mlflow.start_run():
            f1_score=classificationmetric.f1_score
            precision_score=classificationmetric.precision_score
            recall_score=classificationmetric.recall_score


            mlflow.log_metric("fi_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,"model")

    def train_model(self,X_train,y_train,X_test,y_test):
        models={
                "Random Forest":RandomForestClassifier(verbose=1),
                "Logistic Regression":LogisticRegression(verbose=1),
                "Gradient Boosting":GradientBoostingClassifier(verbose=1),
                "AdaBoost":AdaBoostClassifier(),
                "Decision Tree":DecisionTreeClassifier()
            }

        params={
                "Random Forest":{
                    "n_estimators":[8,16]
                },
                "Logistic Regression":{
                },
                "Gradient Boosting":{
                    "learning_rate":[0.1,0.01],
                    "subsample":[0.6,0.7],
                    "n_estimators":[8,16]
                },
                "AdaBoost":{
                    "n_estimators":[8,16],
                    "learning_rate":[0.1,0.01]
                },
                "Decision Tree":{
                    'criterion':['gini','entropy'],
                }
            }

        model_report:dict=evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                param=params
            )
        
        best_model_score=max(sorted(model_report.values()))

        best_model_name=list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]

        best_model=models[best_model_name]

        y_train_pred=best_model.predict(X_train)

        class_metric_train=get_classification_score(y_train_pred,y_train)



        self.track_mlflow(best_model,class_metric_train)


        y_test_pred=best_model.predict(X_test)
        class_metric_test=get_classification_score(y_test_pred,y_test)

        preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)

        save_object(self.model_trainer_config.trained_model_file_path,obj=Network_Model)

        save_object("final_model/model.pkl",best_model)
        

        model_trainer_artifact=ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            trained_metric_artifact=class_metric_train,
            test_metric_artifact=class_metric_test
        )

        return model_trainer_artifact


        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)

            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e