import matplotlib.pyplot as plt

def plot_data(battery, field, field_label, dataset, time_from, time_to, cycles_to_show):
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
    ax.set_ylabel(field_label)

    ax.set_title(battery)

    return fig

def plot_capacity_data(battery, dataset, cycle_from, cycle_to):
    fig, ax = plt.subplots()

    x_values = []
    y_values = []
    current_cycle = dataset['cycle'][0]
    for i in range(len(dataset['cycle'])):
        cycle = dataset['cycle'][i]
        capacity = dataset['capacity'][i]
        if (cycle >= cycle_from) and (cycle <= cycle_to):
            x_values.append(capacity)
            y_values.append(cycle)

    ax.plot(y_values,x_values, label='Capacity')
    ax.grid()

    ax.legend(fontsize="9.5")
    ax.set_xlabel('Cycles')
    ax.set_ylabel('Capacity (Ah)')

    ax.set_title(battery)

    return fig