from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

#先讀取combine資料看要怎麼放進model  dataFrame?list?Series?
data=pd.read_csv("combine.csv")
inputs=data.drop('label',axis='columns') #inputs放需要訓練的欄位
target=data['label'] #target放label
# print(target.head())

#拆分訓練集與測試集
# X=inputs
# y=target
# X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
# model=DecisionTreeClassifier().fit(X_train,y_train)
# 用建立好的模型來預測資料
# model.predict(X_test)
# 檢驗模型的正確率
# model.score(X_test,y_test)

#沒拆
X=inputs
y=target
model=DecisionTreeClassifier().fit(X,y)

#匯出模型
from joblib import dump

dump(model,'decision_tree_model')
