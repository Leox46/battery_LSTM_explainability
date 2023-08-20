import streamlit as st
import pandas as pd
import pages.util.util as util
import pages.nasa.nasa as nasa

st.markdown(
"""
# NASA Battery Dataset

To train the implemented LSTM neural network, the data contained within the [NASA Li-ion Battery Aging Dataset](https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository) were used. This dataset reports the data of 4 batteries, labeled as B0005, B0006, B0007, B0018, that were run through 3 different operational profiles (charge, discharge and impedance) at room temperature.

To train the LSTM network, data measured during battery charging cycles were exploited, such as voltage, current and temperature measured; the capacity measured during the previous discharging cycle was also used.

On this page, it is possible to interact with the data contained in the dataset described above, displaying for each of the four batteries the voltage, current and temperature measured during charging cycles, and the capacity measured during discharging cycles.
"""
)

@st.cache_data(show_spinner="Loading battery data...")
def load_dataset_field(battery, field):
    dataset = pd.read_excel(battery+'/data/'+field+'.xlsx', header=0)
    return dataset

col1, col2 = st.columns(2)
with col1:
    battery = st.selectbox(
        'Battery',
        ('B0005', 'B0006', 'B0007', 'B0018'))

#util.write_data(battery, 'voltage_measured')
#util.write_data(battery, 'current_measured')
#util.write_data(battery, 'temperature_measured')
#util.write_capacity_data(battery)

# Initialize cache
load_dataset_field(battery, 'voltage_measured')
load_dataset_field(battery, 'current_measured')
load_dataset_field(battery, 'temperature_measured')
load_dataset_field(battery, 'capacity')

with col2:
    measure_options = {'voltage_measured': 'Voltage', 'current_measured': 'Current', 'temperature_measured': 'Temperature', 'capacity': 'Capacity'}
    def format_func(option):
        return measure_options[option]
    field = st.selectbox(
        'Field',
        measure_options, format_func=format_func)


dataset = load_dataset_field(battery, field)

col1, col2 = st.columns(2)
if field == 'capacity':
    with col1:
        cycle_from = st.number_input('Cycle from', step=1, min_value=1, max_value=dataset['cycle'].iat[-1])
    with col2:
        cycle_to = st.number_input('Cycle to', step=1, min_value=1, max_value=dataset['cycle'].iat[-1], value=dataset['cycle'].iat[-1])

    if cycle_from > cycle_to:
        st.error("'Cycle from' must be less than 'Cycle to'", icon="🚨")
        quit()

else:
    with col1:
        time_from = st.number_input('Time from (minutes)', step=1, min_value=0)
        time_from = time_from * 60
    with col2:
        if field == 'voltage_measured':
            value = 100
        elif field == 'current_measured':
            value = 175
        elif field == 'temperature_measured':
            value = 150
        time_to = st.number_input('Time to (minutes)', step=1, min_value=0, value=value)
        time_to = time_to * 60

    if time_from > time_to:
        st.error("'Time from' must be less than 'Time to'", icon="🚨")
        quit()

    if battery in ['B0005', 'B0006', 'B0007']:
        values = [2, 21, 41, 61, 81, 102, 122, 142]
    else:
        values = [2, 21, 41, 61, 81, 101]
    cycles_to_show = st.multiselect('Cycles', dataset['cycle'].unique(), default=values)


if field == 'capacity':
    fig = nasa.plot_capacity_data(battery, dataset, cycle_from, cycle_to)
    st.pyplot(fig)
else:
    fig = nasa.plot_data(battery, field, measure_options[field], dataset, time_from, time_to, cycles_to_show)
    st.pyplot(fig)











