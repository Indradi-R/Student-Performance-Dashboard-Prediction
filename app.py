import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
from joblib import load
import plotly.graph_objects as go

st.set_page_config(layout="wide")

data = pd.read_csv("newEduDataset.csv", delimiter=",")

category_mapping = {
    33: 'Biofuel Production Technologies',
    171: 'Animation and Multimedia Design',
    8014: 'Social Service (evening attendance)',
    9003: 'Agronomy',
    9070: 'Communication Design',
    9085: 'Veterinary Nursing',
    9119: 'Informatics Engineering',
    9130: 'Equinculture',
    9147: 'Management',
    9238: 'Social Service',
    9254: 'Tourism',
    9500: 'Nursing',
    9556: 'Oral Hygiene',
    9670: 'Advertising and Marketing Management',
    9773: 'Journalism and Communication',
    9853: 'Basic Education',
    9991: 'Management (evening attendance)'
}
data['Course_Label'] = data['Course'].replace(category_mapping)

st.subheader("Prediction")
course_list = sorted(list(data.Course_Label.unique()))
course_list = list(data.Course_Label.unique())[::-1]
course_list.sort()

if 'pred_selected' not in st.session_state:
    st.session_state.pred_selected = None

if st.session_state.pred_selected is None:
    course_selected = st.selectbox('Course', ['None', *course_list])
else:
    course_selected = st.selectbox('Course', course_list)

if course_selected == 'None':
    st.error("Please select a valid course.")
else:
    st.session_state.course_selected = course_selected

reverse_mapping = {v: k for k, v in category_mapping.items()}

if course_selected != 'None':
    course_selected = reverse_mapping[course_selected]

if course_selected in [9991, 8014]:
    time_selected=0
else:
    time_selected=1

admgrade_selected = st.number_input("Admission grade", value=0.0, step=0.1, min_value=0.0, max_value=200.0)
admgrade_selected = round(admgrade_selected,1)

colGender, colAge = st.columns(2)

with colGender:
    gender_list = ['Male', 'Female']
    gender_selected = st.selectbox('Gender', (gender_list))

    if gender_selected=="Female":
        gender_selected=0
    elif gender_selected=="Male":
        gender_selected=1

with colAge:
    age_selected = st.number_input("Age at enrollment", step=1, min_value=17, max_value=70)

bool1, bool2 = st.columns(2)

with bool1:
    special_list = ['Yes', 'No']
    special_selected = st.radio('Special education needs?', (special_list))

    if (special_selected=="No"):
        special_selected=0
    elif(special_selected=="Yes"):
        special_selected=1
    
with bool2:
    debtor_list = ['Yes', 'No']
    debtor_selected = st.radio('Debtor?', (debtor_list))

    if (debtor_selected=="No"):
        debtor_selected=0
    elif(debtor_selected=="Yes"):
        debtor_selected=1

bool3, bool4 = st.columns(2)
with bool3:
    tuition_list = ['Yes', 'No']
    tuition_selected = st.radio('Tuition up to date?', (tuition_list))

    if (tuition_selected=="No"):
        tuition_selected=0
    elif(tuition_selected=="Yes"):
        tuition_selected=1

with bool4:
    scholarship_list = ['Yes', 'No']
    scholarship_selected = st.radio('Scholarship holder?', (scholarship_list))

    if (scholarship_selected=="No"):
        scholarship_selected=0
    elif(scholarship_selected=="Yes"):
        scholarship_selected=1

grade1, grade2 = st.columns(2)

with grade1:   
    grade1_selected = st.number_input("First semester grade", value=0.0, step=0.1, min_value=0.0, max_value=20.0)
    grade1_selected = round(grade1_selected,2)

with grade2:
    grade2_selected = st.number_input("Second semester grade", value=0.0, step=0.1, min_value=0.0, max_value=20.0)
    grade2_selected = round(grade2_selected,2)

st.markdown('<style>div.stButton > button {margin: 0 auto; display: block; background: white; color: black;}</style>', unsafe_allow_html=True)
button_predict = st.button("Predict", key='custom_button')
if button_predict:
    if course_selected=="None":
        st.write("Please select a valid course.")
    else:
        model = load('model.joblib')
        user_data = {
            'Course': [course_selected], 
            'Daytime_evening_attendance': [time_selected], 
            'Admission_grade': [admgrade_selected], 
            'Educational_special_needs': [special_selected], 
            'Debtor': [debtor_selected], 
            'Tuition_fees_up_to_date': [tuition_selected], 
            'Gender': [gender_selected], 
            'Scholarship_holder': [scholarship_selected], 
            'Age_at_enrollment': [age_selected], 
            'Curricular_units_1st_sem_grade': [grade1_selected],
            'Curricular_units_2nd_sem_grade': [grade2_selected]
        }

        X_new = pd.DataFrame(user_data)
        predictions = model.predict(X_new)
        st.subheader("Prediction Result")
        if predictions == 0:
            st.write("Student is likely to dropout.")
        elif predictions == 1:
            st.write("Student is NOT likely to dropout.")
