import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tf_keras_vis.saliency import Saliency
import shap
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
        if cycle <= first_cycle:
            first_row = i
        if cycle <= last_cycle:
            last_row = i

    matrix = matrix.iloc[first_row:(last_row+1)]
    matrix = matrix.iloc[::-1] # reverse rows, to show first cycles near to (0,0)
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

    fig, ax = plt.subplots()
    c = ax.imshow(saliency_map, cmap='jet', interpolation='nearest', aspect='auto')
    plt.colorbar(c, ax=ax, label="Feature Relevance")
    ax.set_xticks(
        ticks=range(len(feature_names)),
        labels=feature_names,
        rotation=45,
        fontsize=6,
        ha="right",
        rotation_mode="anchor"
    )
    ax.set_xlabel('Features')
    ax.set_yticks(
        ticks=range(len(cycles)),
        labels=cycles,
        fontsize=6,
        #rotation=45,
        #ha="right",
        #rotation_mode="anchor"
    )
    ax.set_ylabel('Cycles')
    ax.set_title(battery)

    return fig


def plot_shap_streamlit(dataset, matrix, excluded_features, first_cycle, last_cycle, max_display_features, sort_features):
    features = dataset.drop(columns='capacity_predicted')

    # Cycles to display
    first_row = 0
    last_row = 0
    for i in range(len(matrix['cycle'])):
        cycle = matrix['cycle'][i]
        if i <= first_cycle:
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
















