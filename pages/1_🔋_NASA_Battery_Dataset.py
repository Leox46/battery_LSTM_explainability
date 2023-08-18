import streamlit as st
import pandas as pd
import pages.util.util as util
import matplotlib.pyplot as plt

st.markdown(
"""
Per addestrare la rete neurale LSTM implementata, sono stati utilizzati i dati contenuti all’interno del NASA Li-ion Battery Aging Dataset [link / riferimenti], utilizzato per addestrare la rete neurale LSTM implementata. In questo dataset, sono riportati i dati dei cicli di carica - scarica effettuati direttamente dal NASA Prognostics Center of Excellence Data Set Repository su 4 batterie (B0005, B0006, B0007, B0018) that were run through 3 different operational profiles (charge, discharge and impedance) at room temperature.

Per addestrare la rete LSTM, verranno sfruttati i dati misurati durante i cicli di carica delle batterie, quali tensione, intensità di corrente e temperatura della batteria misurati durante i cicli di carica.
Per comprendere come cambiano i parametri interni della batteria durante il suo invecchiamento, verrà considerata anche la capacità misurata durante il ciclo di scarica precedente.

Tramite il grafico seguente, è possibile visualizzare per ognuna delle quattro batterie la tensione, l’intensità di corrente e la temperatura misurate durante i cicli di carica, e la capacità misurata durante i cicli di scarica.
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
    a = 1
else:
    fig, ax = plt.subplots()

    x_values = []
    y_values = []
    current_cycle = dataset['cycle'][0]
    for i in range(len(dataset['cycle'])):
        cycle = dataset['cycle'][i]
        time = dataset['time'][i]
        measure = dataset[field][i]
        if (cycle != current_cycle or i == len(dataset['cycle'])-1) and len(x_values):
            if current_cycle in cycles_to_show:
                ax.plot(y_values,x_values, label='Cycle ' + str(current_cycle))
            x_values = []
            y_values = []
            current_cycle = cycle
        else:
            if (time >= time_from) and (time <= time_to):
                x_values.append(measure)
                y_values.append(time / 60)

    ax.legend(fontsize="9.5")
    ax.set_xlabel('Time (minutes)')
    ax.set_ylabel(measure_options[field])

    ax.set_title(battery)

    st.pyplot(fig)











