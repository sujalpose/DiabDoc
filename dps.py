import os
import pickle
# st.beta_set_page_config(page_title='Diabetes')
# DB Management
import sqlite3
import time
from streamlit_lottie import st_lottie
import requests
# Viz Pkgs
import matplotlib
import pyqrcode
import qrcode
import streamlit as st
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

matplotlib.use('Agg')
import seaborn as sns

# File Processing Pkgs
import pandas as pd
import docx2txt
from PIL import Image
from PyPDF2 import PdfFileReader
import pdfplumber

timestr = time.strftime("%Y%m%d-%H%M%S")
#qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=2,border=3)

def load_image(img):
    im = Image.open(img)
    return im


PAGE_CONFIG = {"page_title":"DiabDoc","page_icon": "glucosemeter.png","layout":"centered"}
st.set_page_config(**PAGE_CONFIG)
conn = sqlite3.connect('data.db')
c = conn.cursor()


# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def create_diabetesdatap():
    c.execute(
        'CREATE TABLE IF NOT EXISTS diabetesdatap(username TEXT,Pregnancies INTEGER,Glucose INTEGER,Blood_Pressure INTEGER,Skin_Thickness INTEGER,Insulin INTEGER,BMI FLOAT,DPF FLOAT,Age INTEGER,Datetime TEXT)')

def create_diabetestables():
    c.execute(
        'CREATE TABLE IF NOT EXISTS diabetestables(username TEXT, Age INTEGER, Gender FLOAT, Polyuria FLOAT, Polydipsia FLOAT,SuddenWeightLoss FLOAT,Weakness FLOAT,Polyphagia FLOAT,GenitalThrush FLOAT,VisualBlurring FLOAT,Itching FLOAT,Irritability FLOAT,DelayedHealing FLOAT,PartialParesis FLOAT, MuscleStiffness FLOAT,Alopecia FLOAT,Obesity FLOAT,Datetime TEXT)')

def create_predictiontablep():
    c.execute(
        'CREATE TABLE IF NOT EXISTS predictiontablep(username TEXT,prediction INTEGER)')
#,FOREIGN KEY(prediction) REFERENCES userstable(userid)

def create_predictiontables():
    c.execute(
        'CREATE TABLE IF NOT EXISTS predictiontables(username TEXT,prediction INTEGER)')
#,FOREIGN KEY(prediction) REFERENCES userstable(userid)

def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()


def add_diabetesdatap(username, Pregnancies, Glucose, Blood_Pressure, Skin_Thickness, Insulin, BMI, DPF, Age):
    c.execute(
        'INSERT INTO diabetesdatap(username,Pregnancies,Glucose,Blood_Pressure,Skin_Thickness,Insulin,BMI,DPF,Age,Datetime) VALUES (?,?,?,?,?,?,?,?,?,datetime())',
        (username, Pregnancies, Glucose, Blood_Pressure, Skin_Thickness, Insulin, BMI, DPF, Age))
    conn.commit()

def add_diabetesdatas(username, Age, Gender, Polyuria, Polydipsia,SuddenWeightLoss,Weakness,Polyphagia,GenitalThrush,VisualBlurring,Itching,Irritability,DelayedHealing,PartialParesis, MuscleStiffness,Alopecia,Obesity):
    c.execute(
        'INSERT INTO diabetestables(username, Age, Gender, Polyuria, Polydipsia,SuddenWeightLoss,Weakness,Polyphagia,GenitalThrush,VisualBlurring,Itching,Irritability,DelayedHealing,PartialParesis, MuscleStiffness,Alopecia,Obesity,Datetime) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime())',
        (username, Age, Gender, Polyuria, Polydipsia,SuddenWeightLoss, Weakness, Polyphagia, GenitalThrush,VisualBlurring, Itching, Irritability, DelayedHealing,PartialParesis, MuscleStiffness, Alopecia, Obesity))
    conn.commit()

def add_predictiondatap(username,prediction):
        c.execute(
            'INSERT INTO predictiontablep(username,prediction) VALUES (?,?)',(username,prediction))
        conn.commit()

def add_predictiondatas(username, prediction):
        c.execute(
            'INSERT INTO predictiontables(username,prediction) VALUES (?,?)', (username, prediction))
        conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def view_all_data():
    c.execute('SELECT * FROM diabetesdatap')
    diabetesdata = c.fetchall()
    return diabetesdata

def view_all_data2():
    c.execute('SELECT * FROM diabetestables')
    diabetesdata2 = c.fetchall()
    return diabetesdata2

def view_one_data2(username):
    c.execute('SELECT * FROM diabetestables where username=?',(username))
    diabetesdata2 = c.fetchall()
    return diabetesdata2

def view_prediction_data():
    c.execute('SELECT * FROM predictiontablep')
    predictiondata = c.fetchall()
    return predictiondata

def view_prediction_datas():
    c.execute('SELECT * FROM predictiontables')
    predictiondatas = c.fetchall()
    return predictiondatas

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

pickle_in = open("classifier.pkl", "rb")
classifier = pickle.load(pickle_in)

gender_dict = {"Male":0,"Female":1}
feature_dict = {"No":0,"Yes":1}

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



# create a title and sub title
# st.title("Diabetes Prediction System")
# st.subheader("""
# Diabetes Detection
# Detect if someone has diabetes using machine learning and python !
# """)

# Get the data
df = pd.read_csv('C:/Users/SUJAL/PycharmProjects/pythonProject2/diabetes.csv')
df2 = pd.read_csv('C:/Users/SUJAL/PycharmProjects/pythonProject2/diabetes_data_upload.csv')

# Split the data into indepenent X and dependent Y variables
X = df.iloc[:, 0:8].values
Y = df.iloc[:, -1].values

# Split the data set into 75% training and 25% testing
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state=0)


st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
  <a class="navbar-brand" href="https://youtube.com/dataprofessor" target="_blank">DiabDoc</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="C:/Users/SUJAL/PycharmProjects/pythonProject2/app1.py">LogIn</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/PycharmProjects/pythonProject2/app1.py" target="_blank">Twitter</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)



def main():
    #st.title("Welcome to DiabDoc")
    html_temp = """
        <div style="background-color:tomato;padding:10px">
        <h2 style="color:white;text-align:center;">Welcome to DiabDoc</h2>
        </div>
        """
    st.markdown(html_temp, unsafe_allow_html=True)
    #st.sidebar.header("DiabDoc")
    # Open and display an image

    #st.sidebar.write(
    #"“Diabetes sounds like you’re going to die when you hear it. I was immediately frightened. But once I got a better idea of what it was and that is was something I could manage myself, I was comforted.”")
    #st.sidebar.write("Nick Jonas")



    menu = ["Information about Diabetes","Login","SignUp"]

    choice = st.selectbox("Navigate",menu)

    if choice == "Information about Diabetes":
        st.header("What is Diabetes")
        st.write("""Diabetes is a disease that occurs when your blood glucose, also called blood sugar, is too high. Blood glucose is your main source of energy and comes from the food you eat. Insulin, a hormone made by the pancreas, helps glucose from food get into your cells to be used for energy. Sometimes your body doesn’t make enough—or any—insulin or doesn’t use insulin well. Glucose then stays in your blood and doesn’t reach your cells.Over time, having too much glucose in your blood can cause health problems. Although diabetes has no cure, you can take steps to manage your diabetes and stay healthy.
        Sometimes people call diabetes “a touch of sugar” or “borderline diabetes.” These terms suggest that someone doesn’t really have diabetes or has a less serious case, but every case of diabetes is serious.""")
        st.video('diabdoc.mp4', start_time=0)
        st.header("Diabetes Types")
        st.write("""Diabetes mellitus, commonly known as diabetes, is a metabolic disease that causes high blood sugar. The hormone insulin moves sugar from the blood into your cells to be stored or used for energy. With diabetes, your body either doesn’t make enough insulin or can’t effectively use the insulin it does make. Untreated high blood sugar from diabetes can damage your nerves, eyes, kidneys, and other organs.""")
        st.write("""There are a few different types of diabetes:

        Type 1 diabetes is an autoimmune disease. The immune system attacks and destroys cells in the pancreas, where insulin is made. It’s unclear what causes this attack. About 10 percent of people with diabetes have this type.
        
        Type 2 diabetes occurs when your body becomes resistant to insulin, and sugar builds up in your blood.
        Prediabetes occurs when your blood sugar is higher than normal, but it’s not high enough for a diagnosis of type 2 diabetes.
        
        Gestational diabetes is high blood sugar during pregnancy. Insulin-blocking hormones produced by the placenta cause this type of diabetes.
        A rare condition called diabetes insipidus is not related to diabetes mellitus, although it has a similar name. It’s a different condition in which your kidneys remove too much fluid from your body.""")

        st.write("""Each type of diabetes has unique symptoms, causes, and treatments""")
        st.header("Symptoms of diabetes")
        st.write("""General symptoms
        The general symptoms of diabetes include:

        increased hunger
        increased thirst
        weight loss
        frequent urination
        blurry vision
        extreme fatigue
        sores that don’t heal""")
        st.header("Symptoms in men")
        st.write("""In addition to the general symptoms of diabetes, men with diabetes may have a decreased sex drive, erectile dysfunction (ED), and poor muscle strength.""")

        st.header("Symptoms in women")
        st.write("""Women with diabetes can also have symptoms such as urinary tract infections, yeast infections, and dry, itchy skin.""")

        st.header("Type 1 diabetes")
        st.write("""Symptoms of type 1 diabetes can include:

                    extreme hunger
                    increased thirst
                    unintentional weight loss
                    frequent urination
                    blurry vision
                    tiredness
                    It may also result in mood changes.""")

        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_bkq07nvf.json"
        lottie_json = load_lottieurl(lottie_url)
        st_lottie(lottie_json)

    elif choice == "Login":
        st.sidebar.header("Enter your username and password")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')

        if st.sidebar.checkbox("Login"):

            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))



            if result:
                st.balloons()

                st.sidebar.success("Logged In as {}".format(username))
                st.title("Welcome {}".format(username))
                task = st.selectbox("Task",["Select Task","Exploration","Prediction","Profiles","History"])
                if task == "Select Task":

                    st.subheader("Please select a task to move forward")

                elif task == "Exploration":
                    menu = ["PIMA Diabetes Dataset","Early Diabetes Risk Prediction Dataset"]
                    choice = st.selectbox("Menu", menu)
                    st.title("Data Exploration")
                    if choice == "PIMA Diabetes Dataset":
                        df = pd.read_csv('C:/Users/SUJAL/PycharmProjects/pythonProject2/diabetes.csv')
                        # Set a subheader
                        st.subheader('Data Information :')
                        # Show the data as a table

                        #st.dataframe(df)

                        # Show Dataset

                        if st.checkbox("Show Dataset"):
                            def color_df(val):
                                if val == 0:
                                    color = 'green'
                                else:
                                    color = 'red'

                                return f'background-color: {color}'

                            st.dataframe(df.style.applymap(color_df, subset=['Outcome']))
                            rowview = st.slider("Number of Rows to View",0,770)
                            st.dataframe(df.head(rowview))

                        # Show Columns
                        if st.button("Column Names"):
                            st.write(df.columns)

                        # Show Shape
                        if st.checkbox("Shape of Dataset"):
                            data_dim = st.radio("Show Dimension By ", ("Rows", "Columns"))
                            if data_dim == 'Rows':
                                st.text("Number of Rows")
                                st.write(df.shape[0])
                            elif data_dim == 'Columns':
                                st.text("Number of Columns")
                                st.write(df.shape[1])
                            else:
                                st.write(df.shape)
                            # Select Columns
                            if st.checkbox("Select Columns To Show"):
                                all_columns = df.columns.tolist()
                                selected_columns = st.multiselect("Select", all_columns)
                                new_df = df[selected_columns]
                                st.dataframe(new_df)

                            # Show Values
                            if st.button("Value Counts"):
                                st.text("Value Counts By Target/Class")
                                st.write(df.iloc[:, -1].value_counts())

                            # Show Datatypes
                            if st.button("Data Types"):
                                st.write(df.dtypes)

                            # Show Summary
                            if st.checkbox("Summary"):
                                st.write(df.describe().T)

                            ## Plot and Visualization

                            st.subheader("Data Visualization")
                            # Correlation
                            # Seaborn Plot
                            st.set_option('deprecation.showPyplotGlobalUse', False)
                            if st.checkbox("Correlation Plot[Seaborn]"):
                                st.write(sns.heatmap(df.corr(), annot=True))

                                st.pyplot()

                            # Pie Chart
                            if st.checkbox("Pie Plot"):
                                all_columns_names = df.columns.tolist()
                                if st.button("Generate Pie Plot"):
                                    st.success("Generating A Pie Plot")
                                    st.write(df.iloc[:, -1].value_counts().plot.pie(autopct="%1.1f%%"))
                                    st.pyplot()

                            # Count Plot
                            if st.checkbox("Plot of Value Counts"):
                                st.text("Value Counts By Target")
                                all_columns_names = df.columns.tolist()
                                primary_col = st.selectbox("Primary Columm to GroupBy", all_columns_names)
                                selected_columns_names = st.multiselect("Select Columns", all_columns_names)
                                if st.button("Plot"):
                                    st.text("Generate Plot")
                                    if selected_columns_names:
                                        vc_plot = df.groupby(primary_col)[selected_columns_names].count()
                                    else:
                                        vc_plot = df.iloc[:, -1].value_counts()
                                    st.write(vc_plot.plot(kind="bar"))
                                    st.pyplot()

                            # Customizable Plot

                            st.subheader("Customizable Plot")
                            all_columns_names = df.columns.tolist()
                            type_of_plot = st.selectbox("Select Type of Plot",
                                                    ["area", "bar", "line", "hist", "box", "kde"])
                            selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names)

                            if st.button("Generate Plot"):
                                st.success("Generating Customizable Plot of {} for {}".format(type_of_plot,
                                                                                          selected_columns_names))

                                # Plot By Streamlit
                                if type_of_plot == 'area':
                                    cust_data = df[selected_columns_names]
                                    st.area_chart(cust_data)

                                elif type_of_plot == 'bar':
                                    cust_data = df[selected_columns_names]
                                    st.bar_chart(cust_data)

                                elif type_of_plot == 'line':
                                    cust_data = df[selected_columns_names]
                                    st.line_chart(cust_data)

                                # Custom Plot
                                elif type_of_plot:
                                    cust_plot = df[selected_columns_names].plot(kind=type_of_plot)
                                    st.write(cust_plot)
                                    st.pyplot()

                    elif choice == "Early Diabetes Risk Prediction Dataset":
                        # Set a subheader
                        st.subheader('Data Information :')
                        # Show the data as a table
                        st.dataframe(df2)

                        # Show Dataset

                        if st.checkbox("Show Dataset"):
                            rowview = st.slider("Number of Rows to View",0,770)
                            st.dataframe(df2.head(rowview))

                        # Show Columns
                        if st.button("Column Names"):
                            st.write(df2.columns)

                        # Show Shape
                        if st.checkbox("Shape of Dataset"):
                            data_dim = st.radio("Show Dimension By ", ("Rows", "Columns"))
                            if data_dim == 'Rows':
                                st.text("Number of Rows")
                                st.write(df2.shape[0])
                            elif data_dim == 'Columns':
                                st.text("Number of Columns")
                                st.write(df2.shape[1])
                            else:
                                st.write(df2.shape)
                            # Select Columns
                            if st.checkbox("Select Columns To Show"):
                                all_columns = df2.columns.tolist()
                                selected_columns = st.multiselect("Select", all_columns)
                                new_df = df2[selected_columns]
                                st.dataframe(new_df)

                            # Show Values
                            if st.button("Value Counts"):
                                st.text("Value Counts By Target/Class")
                                st.write(df2.iloc[:, -1].value_counts())

                            # Show Datatypes
                            if st.button("Data Types"):
                                st.write(df2.dtypes)

                            # Show Summary
                            if st.checkbox("Summary"):
                                st.write(df2.describe().T)

                            ## Plot and Visualization

                            st.subheader("Data Visualization")
                            # Correlation
                            # Seaborn Plot
                            st.set_option('deprecation.showPyplotGlobalUse', False)
                            if st.checkbox("Correlation Plot[Seaborn]"):
                                st.write(sns.heatmap(df2.corr(), annot=True))

                                st.pyplot()

                            # Pie Chart
                            if st.checkbox("Pie Plot"):
                                all_columns_names = df2.columns.tolist()
                                if st.button("Generate Pie Plot"):
                                    st.success("Generating A Pie Plot")
                                    st.write(df2.iloc[:, -1].value_counts().plot.pie(autopct="%1.1f%%"))
                                    st.pyplot()

                            # Count Plot
                            if st.checkbox("Plot of Value Counts"):
                                st.text("Value Counts By Target")
                                all_columns_names = df2.columns.tolist()
                                primary_col = st.selectbox("Primary Columm to GroupBy", all_columns_names)
                                selected_columns_names = st.multiselect("Select Columns", all_columns_names)
                                if st.button("Plot"):
                                    st.text("Generate Plot")
                                    if selected_columns_names:
                                        vc_plot = df2.groupby(primary_col)[selected_columns_names].count()
                                    else:
                                        vc_plot = df2.iloc[:, -1].value_counts()
                                    st.write(vc_plot.plot(kind="bar"))
                                    st.pyplot()

                            # Customizable Plot

                            st.subheader("Customizable Plot")
                            all_columns_names = df2.columns.tolist()
                            type_of_plot = st.selectbox("Select Type of Plot",
                                                    ["area", "bar", "line", "hist", "box", "kde"])
                            selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names)

                            if st.button("Generate Plot"):
                                st.success("Generating Customizable Plot of {} for {}".format(type_of_plot,
                                                                                          selected_columns_names))

                                # Plot By Streamlit
                                if type_of_plot == 'area':
                                    cust_data = df2[selected_columns_names]
                                    st.area_chart(cust_data)

                                elif type_of_plot == 'bar':
                                    cust_data = df2[selected_columns_names]
                                    st.bar_chart(cust_data)

                                elif type_of_plot == 'line':
                                    cust_data = df2[selected_columns_names]
                                    st.line_chart(cust_data)

                                # Custom Plot
                                elif type_of_plot:
                                    cust_plot = df2[selected_columns_names].plot(kind=type_of_plot)
                                    st.write(cust_plot)
                                    st.pyplot()




                elif task == "Prediction":
                    st.title("Diabetes Prediction")

                    menu = ["Prediction by ...","By File","By Symptoms", "By Parameters"]
                    predchoice = st.selectbox("Choice", menu)
                    # Get the feature input from the user
                    if predchoice == "By File":


                        def read_pdf(file):
                            pdfReader = PdfFileReader(file)
                            count = pdfReader.numPages
                            all_page_text = ""
                            for i in range(count):
                                page = pdfReader.getPage(i)
                                all_page_text += page.extractText()

                            return all_page_text

                        def read_pdf_with_pdfplumber(file):
                            with pdfplumber.open(file) as pdf:
                                page = pdf.pages[0]
                                return page.extract_text()

                        # import fitz  # this is pymupdf

                        # def read_pdf_with_fitz(file):
                        # 	with fitz.open(file) as doc:
                        # 		text = ""
                        # 		for page in doc:
                        # 			text += page.getText()
                        # 		return text

                        # Fxn
                        @st.cache
                        def load_image2(image_file):
                            img = Image.open(image_file)
                            return img

                        menu = ["Image", "Dataset", "DocumentFiles"]
                        choice = st.selectbox("Type", menu)


                        if choice == "Image":
                            st.subheader("Home")
                            image_file = st.file_uploader("Upload Image", type=['png', 'jpeg', 'jpg'])
                            if image_file is not None:
                                    # To See Details
                                    # st.write(type(image_file))
                                    # st.write(dir(image_file))
                                file_details = {"Filename": image_file.name, "FileType": image_file.type,
                                                    "FileSize": image_file.size}
                                st.write(file_details)

                                img = load_image2(image_file)
                                st.image(img)


                        if choice == "Dataset":
                            st.subheader("Dataset")
                            data_file = st.file_uploader("Upload CSV", type=['csv'])
                            if st.button("Process"):
                                if data_file is not None:
                                    file_details = {"Filename": data_file.name, "FileType": data_file.type,
                                                        "FileSize": data_file.size}
                                    st.write(file_details)

                                    df = pd.read_csv(data_file)
                                    st.dataframe(df)

                        elif choice == "DocumentFiles":
                            st.subheader("DocumentFiles")
                            docx_file = st.file_uploader("Upload File", type=['txt', 'docx', 'pdf'])
                            if st.button("Process"):
                                if docx_file is not None:
                                    file_details = {"Filename": docx_file.name, "FileType": docx_file.type,
                                                        "FileSize": docx_file.size}
                                    st.write(file_details)
                                        # Check File Type
                                    if docx_file.type == "text/plain":
                                            # raw_text = docx_file.read() # read as bytes
                                            # st.write(raw_text)
                                            # st.text(raw_text) # fails
                                        st.text(str(docx_file.read(), "utf-8"))  # empty
                                        raw_text = str(docx_file.read(),
                                                           "utf-8")  # works with st.text and st.write,used for futher processing
                                            # st.text(raw_text) # Works
                                        st.write(raw_text)  # works
                                    elif docx_file.type == "application/pdf":
                                            # raw_text = read_pdf(docx_file)
                                            # st.write(raw_text)
                                        try:
                                            with pdfplumber.open(docx_file) as pdf:
                                                page = pdf.pages[0]
                                                st.write(page.extract_text())
                                        except:
                                            st.write("None")


                                    elif docx_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                                            # Use the right file processor ( Docx,Docx2Text,etc)
                                        raw_text = docx2txt.process(
                                                docx_file)  # Parse in the uploadFile Class directory
                                        st.write(raw_text)




                    elif predchoice == "By Parameters":
                        def get_user_input():
                            st.subheader('Input Parameters :')
                            pregnancies = st.slider("Pregnancies",0,15)
                            glucose = st.slider("Glucose",0,200)
                            blood_pressure = st.slider("Blood Pressure",0,100)
                            skin_thickness = st.slider("Skin Thickness",0,50)
                            insulin = st.slider("Insulin",0,300)
                            BMI = st.slider("BMI",0.0,70.0)
                            DPF = st.slider("DPF",0.0,2.9)
                            age = st.slider("Age",1,110)
                            if st.button("Save"):
                                create_diabetesdatap()
                                add_diabetesdatap(username, pregnancies, glucose, blood_pressure, skin_thickness, insulin,
                                             BMI,
                                             DPF, age)

                            # store a dictionary into a variable
                            user_data = {'pregnancies': pregnancies,
                                    'glucose': glucose,
                                    'blood_pressure': blood_pressure,
                                    'skin_thickness': skin_thickness,
                                    'insulin': insulin,
                                    'BMI': BMI,
                                    'DPF': DPF,
                                    'age': age,
                                    }


                            # TRANSLATE the data into a dataframe
                            features = pd.DataFrame(user_data, index=[0])
                            return features


                        # store the user input into a variable
                        user_input = get_user_input()

                        # set a subheader and display the users input
                        st.subheader('User Input: ')
                        st.write(user_input)

                        # create and train the model
                        from sklearn.ensemble import RandomForestClassifier
                        RandomForestClassifier = RandomForestClassifier()
                        RandomForestClassifier.fit(X_train, Y_train)

                        # store the models prediction in a variable
                        finalprediction = RandomForestClassifier.predict(user_input)

                        st.spinner()

                        if st.button("Predict"):

                            st.subheader('Result : ')
                            if finalprediction == 1:
                                with st.spinner(text='Loading Result...'):
                                    # time.sleep(5)
                                    # st.info('Your result is here...')
                                    st.error("Person is Diabetic!")

                                    # show the model metrics
                                    #st.subheader('Model Test Accuracy Score :')
                                    st.write(
                                        str(accuracy_score(Y_test, RandomForestClassifier.predict(X_test)) * 100) + '%' + '  Probability that patient has diabetes')
                                    # set a subheader and display the classification
                                    #st.subheader('Classification : ')
                                    #st.write(prediction)

                            else:
                                with st.spinner(text='Loading Result...'):
                                    # .sleep(5)
                                    # st.info('Your result is here...')
                                    st.success("Not a Diabetic Person")
                            create_predictiontablep()
                            add_predictiondatap(username, finalprediction)



                        if st.button("Generate Report"):

                            for index, values in user_input.iterrows():
                                #username = values["username"]
                                pregnancies = values["pregnancies"]
                                glucose = values["glucose"]
                                blood_pressure = values["blood_pressure"]
                                skin_thickness = values["skin_thickness"]
                                insulin = values["insulin"]
                                BMI = values["BMI"]
                                DPF = values["DPF"]
                                age = values["age"]
                                #prediction = values["prediction"]
                                data = f'''
                                Name : {username}
                                Pregnancies : {pregnancies}
                                Glucose : {glucose}
                                Blood Pressure : {blood_pressure}
                                Skin Thickness : {skin_thickness}
                                Insulin : {insulin}
                                BMI : {BMI}
                                DPF : {DPF}
                                Age : {age}
                                
                                '''
                                image = pyqrcode.create(data)
                                image.svg(f"{username}.svg", scale="5")

                                qr.add_data(data)
                                qr.make(fit=True)
                                img = qr.make_image(fill_color='black', back_color='white')

                            img_filename = 'generate_image_{}.png'.format(timestr)
                            path_for_images = os.path.join('image_folder', img_filename)
                            img.save(path_for_images)

                            final_img = load_image(path_for_images)
                            st.image(final_img)

                    elif predchoice == "By Symptoms":
                            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>',
                                 unsafe_allow_html=True)
                            def get_user_input():
                                col1, col2 = st.columns(2)
                                Age = col1.text_input("Age", "")
                                # Gender = st.text_input("Gender", "Male/Female")
                                Gender = col1.radio("Sex", tuple(gender_dict.keys()))
                                Polyuria = col1.radio("Polyuria (Frequent Urination)", tuple(feature_dict.keys()))
                                Polydipsia = col1.radio("Polydipsia (Extreme Thirstiness)", tuple(feature_dict.keys()))
                                SuddenWeightLoss = col1.radio("Sudden Weight Loss", tuple(feature_dict.keys()))
                                Weakness = col1.radio("Weakness", tuple(feature_dict.keys()))
                                Polyphagia = col1.radio("Polyphagia (Excessive Hunger)", tuple(feature_dict.keys()))
                                GenitalThrush = col1.radio("Genital Thrush", tuple(feature_dict.keys()))
                                VisualBlurring = col2.radio("Visual Blurring", tuple(feature_dict.keys()))
                                Itching = col2.radio("Itching", tuple(feature_dict.keys()))
                                Irritability = col2.radio("Irritability", tuple(feature_dict.keys()))
                                DelayedHealing = col2.radio("Delayed Healing", tuple(feature_dict.keys()))
                                PartialParesis = col2.radio("Partial Paresis", tuple(feature_dict.keys()))
                                MuscleStiffness = col2.radio("Muscle Stiffness", tuple(feature_dict.keys()))
                                Alopecia = col2.radio("Alopecia (Loss of Hair)", tuple(feature_dict.keys()))
                                Obesity = col2.radio("Obesity", tuple(feature_dict.keys()))


                                if st.button("Save"):
                                    create_diabetestables()
                                    add_diabetesdatas(username, Age, Gender, Polyuria, Polydipsia,SuddenWeightLoss,Weakness,Polyphagia,GenitalThrush,VisualBlurring,Itching,Irritability,DelayedHealing,PartialParesis, MuscleStiffness,Alopecia,Obesity)

                                # store a dictionary into a variable
                                user_data = {'Age': Age,
                                             'Gender': get_value(Gender, gender_dict),
                                             'Polyuria': get_fvalue(Polyuria),
                                             'Polydipsia': get_fvalue(Polydipsia),
                                             'Sudden Weight Loss': get_fvalue(SuddenWeightLoss),
                                             'Weakness': get_fvalue(Weakness),
                                             'Polyphagia': get_fvalue(Polyphagia),
                                             'Genital Thrush': get_fvalue(GenitalThrush),
                                             'Visual Blurring': get_fvalue(VisualBlurring),
                                             'Itching': get_fvalue(Itching),
                                             'Irritability': get_fvalue(Irritability),
                                             'Delayed Healing': get_fvalue(DelayedHealing),
                                             'Partial Paresis': get_fvalue(PartialParesis),
                                             'Muscle Stiffness': get_fvalue(MuscleStiffness),
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

                            prediction = ""
                            if st.button("Predict"):
                                # result = predict_note_authentication(Age, Gender, Polyuria, Polydipsia,suddenweightloss,weakness,Polyphagia,Genitalthrush,visualblurring,Itching,Irritability,delayedhealing,partialparesis,musclestiffness,Alopecia,Obesity)

                                prediction = classifier.predict(user_input)
                                create_predictiontables()
                                add_predictiondatas(username, prediction)
                                if prediction == [1]:
                                    with st.spinner(text='Loading Result...'):

                                        st.error("Person is Diabetic!")

                                else:
                                    with st.spinner(text='Loading Result...'):
                                        # .sleep(5)
                                        # st.info('Your result is here...')
                                        st.success("Not a Diabetic Person")
                            st.success('The output is {}'.format(prediction))


                            if st.button("Generate Report"):

                                for index, values in user_input.iterrows():
                                    # username = values["username"]
                                    Age = values["Age"]
                                    Gender = values["Gender"]
                                    Polyuria = values["Polyuria"]
                                    Polydipsia = values["Polydipsia"]
                                    SuddenWeightLoss = values["Sudden Weight Loss"]
                                    Weakness = values["Weakness"]
                                    Polyphagia = values["Polyphagia"]
                                    GenitalThrush = values["Genital Thrush"]
                                    VisualBlurring = values["Visual Blurring"]
                                    Itching = values["Itching"]
                                    Irritability = values["Irritability"]
                                    DelayedHealing = values["Delayed Healing"]
                                    PartialParesis = values["Partial Paresis"]
                                    MuscleStiffness = values["Muscle Stiffness"]
                                    Alopecia = values["Alopecia"]
                                    Obesity = values["Obesity"]

                                    #prediction = values["prediction"]
                                    data = f'''
                                    Name : {username}
                                    Age : {Age}
                                    Gender : {Gender}
                                    Polyuria : {Polyuria}
                                    Polydipsia : {Polydipsia}
                                    SuddenWeightLoss : {SuddenWeightLoss}
                                    Weakness : {Weakness}
                                    Polyphagia : {Polyphagia}
                                    GenitalThrush : {GenitalThrush}
                        	        VisualBlurring : {VisualBlurring}
                        	        Itching : {Itching}
                        	        Irritability : {Irritability}
                        	        DelayedHealing : {DelayedHealing}
                        	        PartialParesis : {PartialParesis}
                        	        MuscleStiffness : {MuscleStiffness}
                        	        Alopecia : {Alopecia}
                        	        Obesity : {Obesity}
                                    
                                    '''
                                    image2 = pyqrcode.create(data)
                                    image2.svg(f"{username}.svg", scale="5")

                                    qr.add_data(data)
                                    qr.make(fit=True)
                                    img = qr.make_image(fill_color='black', back_color='white')

                                img_filename = 'generate_image_{}.png'.format(timestr)
                                path_for_images = os.path.join('image_folder', img_filename)
                                img.save(path_for_images)

                                final_img = load_image(path_for_images)
                                st.image(final_img)

                elif task == "Profiles":
                    st.subheader("User Profiles")

                    if username=="Admin":
                        user_result = view_all_users()
                        clean_db = pd.DataFrame(user_result,columns=["Id","Username","Password"])
                        st.dataframe(clean_db)
                    else:
                        st.error("You don't have rights to view this section")


                elif task == "History":

                    if username=="admin":
                        st.subheader("Prediction by Parameters")
                        diabetes_data = view_all_data()
                        clean_db = pd.DataFrame(diabetes_data,
                                                columns=["username", "Pregnancies", "Glucose", "Blood Pressure",
                                                         "Skin Thickness", "Insulin", "BMI", "DPF", "Age",
                                                         "Date"])
                        st.dataframe(clean_db)

                        #def color_df(val):
                         #   if val == 1:
                         #       color = 'red'
                         #   else:
                          #      color = 'green'
                          #  return f'background-color:{color}'
                        prediction_data = view_prediction_data()
                        clean_db3 = pd.DataFrame(prediction_data,
                                                columns=["username","prediction"])
                        st.dataframe(clean_db3)
#.style.applymap(color_df, subset=['prediction'])
                        st.subheader("Prediction by Symptoms")
                        diabetes_data2 = view_all_data2()

                        clean_db2 = pd.DataFrame(diabetes_data2,
                                                 columns=["username", "Age", "Gender", "Polyuria", "Polydipsia",
                                                          "Sudden Weight Loss", "Weakness", "Polyphagia",
                                                          "Genital Thrush", "VisualBlurring", "Itching", "Irritability",
                                                          "Delayed Healing", "Partial Paresis", "Muscle Stiffness",
                                                          "Alopecia", "Obesity", "Date"])
                        st.dataframe(clean_db2)

                        prediction_data = view_prediction_datas()
                        clean_db4 = pd.DataFrame(prediction_data,
                                                 columns=["username", "prediction"])
                        st.dataframe(clean_db4)
                    else:
                        st.subheader("Prediction by Parameters")
                        diabetes_data = c.execute('SELECT * FROM diabetesdatap where username=?', (username,))
                        clean_db = pd.DataFrame(diabetes_data,
                                                columns=["username", "Pregnancies", "Glucose", "Blood Pressure",
                                                         "Skin Thickness", "Insulin", "BMI", "DPF", "Age",
                                                         "Date"])
                        st.dataframe(clean_db)



                        st.subheader("Prediction by Symptoms")

                        diabetes_data2 = c.execute('SELECT * FROM diabetestables where username=?', (username,))
                        clean_db2 = pd.DataFrame(diabetes_data2,
                                                 columns=["username", "Age", "Gender", "Polyuria", "Polydipsia",
                                                          "Sudden Weight Loss", "Weakness", "Polyphagia",
                                                          "Genital Thrush", "VisualBlurring", "Itching", "Irritability",
                                                          "Delayed Healing", "Partial Paresis", "Muscle Stiffness",
                                                          "Alopecia", "Obesity", "Date"])
                        st.dataframe(clean_db2)


            else:
                st.warning("Incorrect Username/Password")


        lottie_url2 = "https://assets2.lottiefiles.com/packages/lf20_ioxlu1zt.json"
        lottie_json2 = load_lottieurl(lottie_url2)
        st_lottie(lottie_json2)

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')
        if new_password == confirm_password:
            st.success("Password Confirmed")
        else:
            st.warning("Passwords not the same")

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Login to Get Started")


    image = Image.open('diabetes_fruit.jpeg')
    st.sidebar.image(image, caption='An applcation to know you better', use_column_width=True)
if __name__ == '__main__':
    main()