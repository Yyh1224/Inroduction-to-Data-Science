import numpy as np

def preprocess(df):
    #continuous, category var
    category = ['HasCrCard', 'IsActiveMember','Geography', 'Gender']
    continuous = df.columns.to_list()
    exited = ['Exited']
    nouse = ['RowNumber','CustomerId','Surname']
    if 'Exited' in df.columns:
        [continuous.remove(i) for i in (category+nouse+exited)]
        df = df[exited + continuous + category]
    else:
        [continuous.remove(i) for i in (category+nouse)]
        df = df[continuous + category]
    #one-hot variables for negative relation
    df.loc[df.HasCrCard == 0, 'HasCrCard'] = -1
    df.loc[df.IsActiveMember == 0, 'IsActiveMember'] = -1
    #one-hot encoding categorical variables
    lst = ['Geography', 'Gender']
    remove = list()
    for i in lst:
        if (df[i].dtype == np.str or df[i].dtype == np.object):
            for j in df[i].unique():
                df[i+'_'+j] = np.where(df[i] == j,1,-1)
            remove.append(i)
    df = df.drop(remove, axis=1)
    # minMax scaling the continuous variables
    minVec = df[continuous].min().copy()
    maxVec = df[continuous].max().copy()
    df[continuous] = (df[continuous]-minVec)/(maxVec-minVec)
    return df

