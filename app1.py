
import numpy as np
import pickle
import pandas as pd
# from flasgger import Swagger
import streamlit as st

from PIL import Image

# app=Flask(__name__)
# Swagger(app)

pickle_in = open("classifier.pkl", "rb")
classifier = pickle.load(pickle_in)

gender_dict = {"Male":1,"Female":2}
feature_dict = {"No":1,"Yes":2}

def get_value(val,my_dict):
	for key,value in my_dict.items():
		if val == key:
			return value

def get_key(val,my_dict):
	for key,value in my_dict.items():
		if val == key:
			return key

def get_fvalue(val):
	feature_dict = {"No":0,"Yes":1}
	for key,value in feature_dict.items():
		if val == key:
			return value


# @app.route('/')
def welcome():
    return "Welcome All"


# @app.route('/predict',methods=["Get"])
#def predict_note_authentication(Age, Gender, Polyuria, Polydipsia,suddenweightloss,weakness,Polyphagia,Genitalthrush,visualblurring,Itching,Irritability,delayedhealing,partialparesis,musclestiffness,Alopecia,Obesity):

 #   prediction = classifier.predict([[Age, Gender, Polyuria, Polydipsia,suddenweightloss,weakness,Polyphagia,Genitalthrush,visualblurring,Itching,Irritability,delayedhealing,partialparesis,musclestiffness,Alopecia,Obesity]])
  #  print(prediction)
   # return prediction


def main():
    st.title("Early Stage Diabetes Risk Prediction")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Diabetes Prediction ML App </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    def get_user_input():
        col1, col2 = st.beta_columns(2)
        Age = col1.text_input("Age", "")
        #Gender = st.text_input("Gender", "Male/Female")
        Gender = col1.radio("Sex",tuple(gender_dict.keys()))
        Polyuria = col1.radio("Polyuria", tuple(feature_dict.keys()))
        Polydipsia = col1.radio("Polydipsia", tuple(feature_dict.keys()))
        suddenweightloss = col1.radio("Sudden Weight Loss", tuple(feature_dict.keys()))
        weakness = col1.radio("Weakness", tuple(feature_dict.keys()))
        Polyphagia = col1.radio("Polyphagia", tuple(feature_dict.keys()))
        Genitalthrush = col1.radio("Genital Thrush", tuple(feature_dict.keys()))
        visualblurring = col2.radio("Visual Blurring", tuple(feature_dict.keys()))
        Itching = col2.radio("Itching", tuple(feature_dict.keys()))
        Irritability = col2.radio("Irritability", tuple(feature_dict.keys()))
        delayedhealing = col2.radio("Delayed Healing", tuple(feature_dict.keys()))
        partialparesis = col2.radio("Partial Paresis", tuple(feature_dict.keys()))
        musclestiffness = col2.radio("Muscle Stiffness", tuple(feature_dict.keys()))
        Alopecia = col2.radio("Alopecia", tuple(feature_dict.keys()))
        Obesity = col2.radio("Obesity", tuple(feature_dict.keys()))

        # store a dictionary into a variable
        user_data = {'Age': Age,
                     'Gender': get_value(Gender,gender_dict),
                     'Polyuria': get_fvalue(Polyuria),
                     'Polydipsia': get_fvalue(Polydipsia),
                     'Sudden Weight Loss': get_fvalue(suddenweightloss),
                     'Weakness': get_fvalue(weakness),
                     'Polyphagia': get_fvalue(Polyphagia),
                     'Genital Thrush': get_fvalue(Genitalthrush),
                     'Visual Blurring': get_fvalue(visualblurring),
                     'Itching': get_fvalue(Itching),
                     'Irritability': get_fvalue(Irritability),
                     'Delayed Healing': get_fvalue(delayedhealing),
                     'Partial Paresis': get_fvalue(partialparesis),
                     'Muscle Stiffness': get_fvalue(musclestiffness),
                     'Alopecia': get_fvalue(Alopecia),
                     'Obesity': get_fvalue(Obesity),

                     }

        # TRANSLATE the data into a dataframe
        features = pd.DataFrame(user_data, index=[0])
        return features

        # store the user input into a variable

    user_input = get_user_input()

    # set a subheader and display the users input
    st.subheader('User Input: ')
    st.write(user_input)

    result = ""
    if st.button("Predict"):
        #result = predict_note_authentication(Age, Gender, Polyuria, Polydipsia,suddenweightloss,weakness,Polyphagia,Genitalthrush,visualblurring,Itching,Irritability,delayedhealing,partialparesis,musclestiffness,Alopecia,Obesity)
        result = classifier.predict(user_input)

        if result == [1]:
            with st.spinner(text='Loading Result...'):

                st.error("Person is Diabetic!")

        else:
            with st.spinner(text='Loading Result...'):
                # .sleep(5)
                # st.info('Your result is here...')
                st.success("Not a Diabetic Person")
    st.success('The output is {}'.format(result))
    if st.button("About"):
        st.text("Lets LEarn")
        st.text("Built with Streamlit")


if __name__ == '__main__':
    main()


