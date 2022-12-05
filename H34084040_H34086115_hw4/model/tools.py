import numpy as np
import pandas as pd
# Scoring functions
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

#split to train data and label data
def prep(train,test):
    train = train.drop(['Unnamed: 0'],axis=1)
    test = test.drop(['Unnamed: 0'],axis=1)
    x = train.loc[:, train.columns != 'Exited']
    y = train.Exited
    order = x.columns.to_list()
    test = test[order]
    return x,y,test

# Function to give best model score and parameters
def best_model(model):
    print(model.best_score_)    
    print(model.best_params_)
    print(model.best_estimator_)
    best = model.best_estimator_
    # print(best)
    return best
def get_auc_scores(y_actual, method,method2):
    auc_score = roc_auc_score(y_actual, method); 
    fpr_df, tpr_df, _ = roc_curve(y_actual, method2); 
    return (auc_score, fpr_df, tpr_df)

#save result to csv
def saveresult(model,data,pred):
    df = pd.DataFrame(pred)
    path = 'C:/Users/yuanhsu/Desktop/111-1/資料科學導論/hw4/csv'
    testing= pd.read_csv(path+'/test.csv')
    res = pd.concat([testing['RowNumber'],df],axis=1)
    res = res.rename(columns={0: 'Exited'})
    res.to_csv(data+'_'+model+'.csv')
    print('done with'+data+'_'+model)