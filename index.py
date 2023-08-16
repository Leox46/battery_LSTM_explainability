import streamlit as st
import util_streamlit_deploy
import pandas as pd

import xlsxwriter

col1, col2 = st.columns(2)
with col1:
    battery = st.selectbox(
        'Battery',
        ('B0005', 'B0006', 'B0007', 'B0018'))
    #st.write('You selected:', battery)

dataset = pd.read_excel(battery+'/'+battery+'_norm_window.xlsx', header=0)

with col2:
    options = {'saliency': 'Saliency Map', 'shap': 'SHAP'}
    def format_func(option):
        return options[option]
    technique = st.selectbox(
        'Explainability Technique',
        options, format_func=format_func)
    #st.write('You selected:', technique)

col3, col4 = st.columns(2)
with col3:

    excluded_features = st.multiselect(
        'Excluded features',
        [
            'cap',
            'volt_1', 'cur_1', 'temp_1',
            'volt_2', 'cur_2', 'temp_2',
            'volt_3', 'cur_3', 'temp_3',
            'volt_4', 'cur_4', 'temp_4',
            'volt_5', 'cur_5', 'temp_5',
            'volt_6', 'cur_6', 'temp_6',
            'volt_7', 'cur_7', 'temp_7',
            'volt_8', 'cur_8', 'temp_8',
            'volt_9', 'cur_9', 'temp_9',
            'volt_10', 'cur_10', 'temp_10',
        ]
    )

    if technique == 'shap':
        col5, col6 = st.columns(2)
        with col5:
            max_display_features = st.selectbox('# Features to show', range(1, 32), 14)
        with col6:
            sort_features = st.checkbox('Sort Features')

with col4:
    first_cycle = st.selectbox('First cycle', dataset['cycle'])
    last_cycle = st.selectbox('Last cycle', dataset['cycle'], index=(len(dataset['cycle'])-1))

matrix = pd.read_excel(battery+'/'+technique+'.xlsx', header=0)
if(technique == 'saliency'):
    c = util_streamlit_deploy.plot_saliency_map_streamlit(battery, matrix, excluded_features, first_cycle, last_cycle)
    st.pyplot(c)
elif(technique == 'shap'):
    util_streamlit_deploy.plot_shap_streamlit(dataset, matrix, excluded_features, first_cycle, last_cycle, max_display_features, sort_features)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()


