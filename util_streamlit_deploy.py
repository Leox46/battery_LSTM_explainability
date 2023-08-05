import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tf_keras_vis.saliency import Saliency
import xlsxwriter

def generate_saliency_map(battery, model, cycles, features, feature_names):
    features = np.reshape(features, (features.shape[0], features.shape[1], 1))

    saliency = Saliency(model,
        clone=True)

    saliency_map = saliency(
        saliency_score_function,
        features
    )

    workbook = xlsxwriter.Workbook(battery+'/saliency.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, 'cycle')
    for i in range(len(feature_names)):
        worksheet.write(0, i+1, feature_names[i])

    for i in range(len(saliency_map)):
        worksheet.write(i+1, 0, cycles[i])
        feature_relevances = saliency_map[i]
        for j in range(len(feature_relevances)):
            worksheet.write(i+1, j+1, feature_relevances[j])

    workbook.close()

def plot_saliency_map_streamlit(battery, matrix, excluded_features, first_cycle, last_cycle):

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


    # Excluded features
    excluded_features.append('cycle')
    saliency_map = matrix.drop(columns=excluded_features)

    feature_names = []
    for i in matrix.columns:
        if not(i in excluded_features):
            feature_names.append(i)

    cycles = matrix['cycle']

    tmp_cycles = []
    cycle_label_interval = 5
    for i in range(len(cycles)):
        cycle = cycles[i]
        if ((i % cycle_label_interval) == 0):
            tmp_cycles.append(cycle)
        else:
            tmp_cycles.append("")
    cycles = tmp_cycles

    fig = plt.figure()
    ax = fig.add_subplot()
    c = ax.imshow(saliency_map, cmap='jet', interpolation='nearest', aspect='auto')
    plt.colorbar(c, label="Feature Relevance")
    plt.xticks(
        ticks=range(len(feature_names)),
        labels=feature_names,
        rotation=45,
        fontsize=6,
        ha="right",
        rotation_mode="anchor"
    )
    plt.xlabel('Features')
    plt.yticks(
        ticks=range(len(cycles)),
        labels=cycles,
        fontsize=6,
        #rotation=45,
        #ha="right",
        #rotation_mode="anchor"
    )
    plt.ylabel('Cycles')
    plt.title(battery)

    '''
    c = plt.imshow(matrix, cmap='jet', interpolation='nearest', aspect='auto')
    plt.colorbar(c, label="Feature Relevance")
    plt.xticks(
        ticks=range(len(feature_names)),
        labels=feature_names,
        rotation=45,
        ha="right",
        rotation_mode="anchor"
    )
    plt.xlabel('Features')
    plt.yticks(
        ticks=range(len(cycles)),
        labels=cycles,
        #fontsize=6
        #rotation=45,
        #ha="right",
        #rotation_mode="anchor"
    )
    plt.ylabel('Cycles')
    plt.title('')
    '''

    return fig


















