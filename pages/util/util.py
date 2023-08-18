import sys, getopt
import datetime
import numpy as np
import pandas as pd
import math
from scipy.io import loadmat
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn import metrics
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import LSTM
from tensorflow.keras.optimizers import Adam

import xlsxwriter

#tf.compat.v1.disable_v2_behavior()

def load_all_data(battery):
    sampling_size = 10
    mat = loadmat(battery + '.mat')
    counter = 0
    dataset = []
    capacity_data = []

    can_registry_charge = True
    can_registry_discharge = False
    for i in range(len(mat[battery][0, 0]['cycle'][0])):
        row = mat[battery][0, 0]['cycle'][0, i]

        date_time = datetime.datetime(int(row['time'][0][0]),
               int(row['time'][0][1]),
               int(row['time'][0][2]),
               int(row['time'][0][3]),
               int(row['time'][0][4])) + datetime.timedelta(seconds=int(row['time'][0][5]))

        #print((counter+1), date_time, row['type'][0])
        #if(row['type'][0] == 'discharge'): print("\n")

        if row['type'][0] == 'charge':
            if not can_registry_charge:
                print("Deleted charge cycle", counter, "on battery", battery, "because", (counter+1), "cycle is also charge")
                del dataset[-sampling_size:]

            can_registry_charge = False
            can_registry_discharge = True
            data = row['data']

            count_cycle_measurements = len(data[0][0]['Voltage_measured'][0])
            sampling_interval = math.floor(count_cycle_measurements / (sampling_size))
            if(sampling_interval > 0):
                for j in range(count_cycle_measurements):
                    time = data[0][0]['Time'][0][j]
                    voltage_measured = data[0][0]['Voltage_measured'][0][j]
                    current_measured = data[0][0]['Current_measured'][0][j]
                    temperature_measured = data[0][0]['Temperature_measured'][0][j]

                    dataset.append([counter + 1, time, voltage_measured, current_measured, temperature_measured])
            else:
                print("Skipped charge cycle", (counter+1), "on battery", battery, "because there are <", sampling_size, "records")

        if row['type'][0] == 'discharge':
            if can_registry_discharge:
                data = row['data']
                capacity = data[0][0]['Capacity'][0][0]

                capacity_data.append([counter + 1, capacity])
                #counter = counter + 1
                can_registry_charge = True
                can_registry_discharge = False
            else:
                print("Skipped discharge cycle", (counter+1), "on battery", battery, "because precedent cycle was discharge")

            counter = counter + 1

    print("\n")

    dataset = pd.DataFrame(data=dataset,
        columns=['cycle', 'time', 'voltage_measured',
            'current_measured', 'temperature_measured'])

    capacity_data = pd.DataFrame(data=capacity_data,
        columns=['cycle', 'capacity'])

    return [dataset, capacity_data]

def write_data(battery, measure, interval = 1, exclude_cycles = [], include_cycles = []):
    dataset, capacity = load_all_data(battery)

    cycles = []
    times = []
    measures = []
    current_cycle = dataset['cycle'][0]
    count = 0
    for i in range(len(dataset['cycle'])):
        cycle = dataset['cycle'][i]
        if(dataset['cycle'][i] != current_cycle):
            current_cycle = cycle
            count = count + 1
        if (not (cycle in exclude_cycles)) and ( (count % interval == 0) or (cycle in include_cycles) ):
            cycles.append(current_cycle)
            times.append(dataset['time'][i])
            measures.append(dataset[measure][i])

    workbook = xlsxwriter.Workbook(battery+'/data/'+measure+'.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'cycle')
    worksheet.write(0, 1, 'time')
    worksheet.write(0, 2, measure)
    for i in range(len(cycles)):
        if (not math.isnan(measures[i])) and (cycles[i] > 0):
            worksheet.write(i+1, 0, cycles[i])
            worksheet.write(i+1, 1, times[i])
            worksheet.write(i+1, 2, measures[i])

    workbook.close()

def write_capacity_data(battery, interval = 1, exclude_cycles = [], include_cycles = []):
    dataset, capacity_data = load_all_data(battery)

    cycles = []
    capacities = []
    current_cycle = capacity_data['cycle'][0]
    for i in range(len(capacity_data['cycle'])):
        cycle = capacity_data['cycle'][i]
        if (not (cycle in exclude_cycles)) and ( (i % interval == 0) or (cycle in include_cycles) ):
            cycles.append(cycle)
            capacities.append(capacity_data['capacity'][i])

    workbook = xlsxwriter.Workbook(battery+'/data/capacity.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'cycle')
    worksheet.write(0, 1, 'capacity')
    for i in range(len(cycles)):
        worksheet.write(i+1, 0, cycles[i])
        worksheet.write(i+1, 1, capacities[i])

    workbook.close()

def load_model(path):
    print('*************************')
    print('***** Model Loaded: *****')
    print('*************************')
    if (not path.endswith('/model')) and (not path.endswith('/model/')):
        path = path+'/model'
    model = tf.keras.models.load_model(path)
    model.summary()
    return model

def test_model(model, features, target):


    print('*************************')
    print('***** Testing Model: *****')
    print('*************************')
    #features = np.reshape(features, (features.shape[0], features.shape[1], 1))
    pred = model.predict(features)


    print('***** Predictions (', len(pred),' rows): *****')
    print(pd.DataFrame(data=pred).head())
    print('\n')

    return pred

    '''features = pd.DataFrame(data=features)
    new_soh = []
    new_soh['SoH'] =  soh
    new_soh['NewSoH'] = soh_pred
    new_soh = new_soh.groupby(['cycle']).mean().reset_index()
    print(new_soh.head(10))
    rms = np.sqrt(mean_squared_error(new_soh['SoH'], new_soh['NewSoH']))
    print('Root Mean Square Error: ', rms)'''























