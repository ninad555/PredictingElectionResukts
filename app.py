import pandas as pd  #For data manipulation
import numpy as np   #For performing the numerical operations on data
import tensorflow as tf  #For building models
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import streamlit as st

#to create the heading
st.header("unamed-XXXXXXXXXx")

def data_preprocessing(path):
    data = pd.read_excel(path, sheet_name="Election_Dataset_Two Classes")
    data['vote'] = data['vote'].map({
        'Labour': 0,
        'Conservative': 1
    })
    data['gender'] = data['gender'].map({
        'female': 0,
        'male': 1
    })
    data["age"] = (data["age"] - data["age"].mean()) / data["age"].std()

    return data

def model_predict(load_data):
    x = load_data.drop(columns=['Unnamed: 0','vote'])
    y = load_data['vote']

    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)
    LG=LogisticRegression(max_iter=2500, n_jobs=-2, penalty='l2', solver='sag',
               tol=0.001)
    LG_model=LG.fit(x_train,y_train)
    y_pred01=LG_model.predict(x_test)
    print(classification_report(y_pred01,y_test))

    return LG_model

age = st.text_input("Whats your age?")
gender = st.selectbox("Whats your Gender?",("Male" , "Female"))
economic_status_nation = st.slider('Rate the economic condition of your nation?',1, 5)
economic_status_household = st.slider('Rate the economic condition of your household?',1, 5)
labour_leader = st.slider('How strongly do you support the work of Labour leaders ?', 1, 5)
conservative_leader = st.slider('How strongly do you support the work of conservative leaders ?', 1, 5)
european_integration = st.slider('To what extend are you in favour of European Union?', 1, 11)
political_knowledege = st.slider('Your knowledge about political parties position?', 0 ,3)


if st.button("Submit"):
    if gender == "Male":
        gender = 1
    else:
        gender = 0
    input_array = [age, economic_status_nation, economic_status_household, labour_leader, conservative_leader,
                   european_integration, political_knowledege,
                   gender]
    print(input_array)
    path = "C:/Users/admin/PycharmProjects/DHL_WebApp/Election_Data.xlsx"
    load_data = data_preprocessing(path)
    print(load_data.head())
    get_model = model_predict(load_data)
    predicted = get_model.predict([input_array])[0]
    if predicted == 0:
        st.write("Predicted party is Labour Party")
    else:
        st.write("Predicted party is Conservative Party")


