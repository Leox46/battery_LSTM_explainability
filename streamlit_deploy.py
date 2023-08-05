import streamlit as st
import util_streamlit_deploy
import pandas as pd
import shap

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

    features = dataset.drop(columns='capacity_predicted')

    # Cycles to display
    first_row = 0
    last_row = 0
    for i in range(len(matrix['cycle'])):
        cycle = matrix['cycle'][i]
        if i < first_cycle:
            first_row = i
        if i <= last_cycle:
            last_row = i
    matrix = matrix.iloc[first_row:(last_row+1)]
    matrix.reset_index(drop=True, inplace=True)
    features = features.iloc[first_row:(last_row+1)]
    features.reset_index(drop=True, inplace=True)

    # Revert columns order
    matrix = matrix[matrix.columns[::-1]]
    features = features[features.columns[::-1]]

    # Excluded features
    excluded_features.append('cycle')
    features = features.drop(columns=excluded_features)
    matrix = matrix.drop(columns=excluded_features)

    matrix = matrix.to_numpy()

    shap.summary_plot(
        matrix,
        features,
        #shap_values[0][:1],
        #testing_features.iloc[:1],
        max_display=max_display_features,
        sort= not sort_features
    )
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()


