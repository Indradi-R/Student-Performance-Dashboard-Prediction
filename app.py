import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
from joblib import load

st.set_page_config(layout="wide")

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
course_selected = st.selectbox('Course', ['None', *course_list])

if course_selected == 'None':
    st.error("Please select a valid course.")
else:
    reverse_mapping = {v: k for k, v in category_mapping.items()}
    course_selected = reverse_mapping[course_selected]
    
    time_selected = 0 if course_selected in [9991, 8014] else 1
    
    admgrade_selected = st.number_input("Admission grade", value=0.0, step=0.1, min_value=0.0, max_value=200.0)
    gender_selected = st.selectbox('Gender', ['Male', 'Female'])
    gender_selected = 1 if gender_selected == "Male" else 0
    age_selected = st.number_input("Age at enrollment", step=1, min_value=17, max_value=70)
    
    special_selected = 1 if st.radio('Special education needs?', ['Yes', 'No']) == "Yes" else 0
    debtor_selected = 1 if st.radio('Debtor?', ['Yes', 'No']) == "Yes" else 0
    tuition_selected = 1 if st.radio('Tuition up to date?', ['Yes', 'No']) == "Yes" else 0
    scholarship_selected = 1 if st.radio('Scholarship holder?', ['Yes', 'No']) == "Yes" else 0
    
    grade1_selected = st.number_input("First semester grade", value=0.0, step=0.1, min_value=0.0, max_value=20.0)
    grade2_selected = st.number_input("Second semester grade", value=0.0, step=0.1, min_value=0.0, max_value=20.0)
    
    if st.button("Predict"):
        model = load('model.joblib')
        X_new = pd.DataFrame({
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
        })
        predictions = model.predict(X_new)
        st.subheader("Prediction Result")
        st.write("Student is likely to dropout." if predictions == 0 else "Student is NOT likely to dropout.")
