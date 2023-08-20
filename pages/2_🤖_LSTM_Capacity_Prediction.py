import streamlit as st
import pages.util.util as util
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

st.markdown(
"""
# LSTM Capacity Prediction

On this page it is possible to observe the results of the Explainability techniques applied to the LSTM model implemented for estimating the capacity of a lithium battery.
"""
)

battery = st.selectbox(
    'Battery',
    ('B0005', 'B0006', 'B0007', 'B0018'))

testing_dataset = pd.read_excel(battery+'/'+battery+'_norm_window.xlsx', header=0)
testing_target = testing_dataset['capacity_predicted']
cycles = testing_dataset['cycle']

col1, col2 = st.columns(2)
with col1:
    cycle_from = st.selectbox('Cycle from', testing_dataset['cycle'])
with col2:
    cycle_to = st.selectbox('Cycle to', testing_dataset['cycle'], index=(len(testing_dataset['cycle'])-1))


model = util.load_model(battery+'/models/lstm/model')

testing_features = testing_dataset.drop(columns='capacity_predicted')
testing_features = testing_features.drop(columns='cycle')

testing_features = testing_features.to_numpy()
testing_target = testing_target.to_numpy()
test_predictions = util.test_model(model, testing_features, testing_target)

test_results = pd.DataFrame(data=[])
test_results['capacity'] = testing_target
test_results['capacity_predicted'] = test_predictions

mse = mean_squared_error(test_results['capacity'], test_results['capacity_predicted'])
rmse = np.sqrt(mse)
mape = mean_absolute_percentage_error(test_results['capacity'], test_results['capacity_predicted'])
mae = mean_absolute_error(test_results['capacity'], test_results['capacity_predicted'])

metrics_dataframe = pd.DataFrame([[mse, rmse, mape, mae]], columns=['MSE', 'RMSE', 'MAPE', 'MAE'])
st.dataframe(metrics_dataframe,
    hide_index=True,
    column_config={
        "MSE": st.column_config.NumberColumn(format="%.8f"),
        "RMSE": st.column_config.NumberColumn(format="%.8f"),
        "MAPE": st.column_config.NumberColumn(format="%.8f"),
        "MAE": st.column_config.NumberColumn(format="%.8f"),
    },
)

fig, ax = plt.subplots()

x_values_capacity = []
x_values_capacity_predicted = []
y_values = []
current_cycle = testing_dataset['cycle'][0]
for i in range(len(testing_dataset['cycle'])):
    cycle = testing_dataset['cycle'][i]
    capacity = test_results['capacity'][i]
    capacity_predicted = test_results['capacity_predicted'][i]
    if (cycle >= cycle_from) and (cycle <= cycle_to):
        x_values_capacity.append(capacity)
        x_values_capacity_predicted.append(capacity_predicted)
        y_values.append(cycle)

ax.plot(y_values,x_values_capacity, label='Capacity')
ax.plot(y_values,x_values_capacity_predicted, label='Capacity Predicted')
ax.grid()

ax.legend(fontsize="9.5")
ax.set_xlabel('Cycles')
ax.set_ylabel('Capacity (Ah)')

ax.set_title(battery)

st.pyplot(fig)








