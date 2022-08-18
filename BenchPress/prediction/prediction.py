import joblib
import pandas as pd

class dfTransformer():
  def __init__(self,func):
    self.func=func
  
  def transform(self,df):
    return self.func(df)

  def fit(self, X, y=None):
    return self
    
def to_float(x):
    try:
        return abs(float(x))
    except:        
        return abs(float(x.replace('.','',1)))

def data_transformer(df):
    df.BestSquatKg = df.BestSquatKg.apply(to_float)
    df.Sex = df.Sex.map({'M':1, 'F':0})
    return df

def BP_predict(model, values):
    exemplo = pd.DataFrame(values,
    index=['Sex', 'Equipment', 'Age', 'BodyweightKg', 'BestSquatKg','BestDeadliftKg']).T
    return list(model.predict(exemplo))


