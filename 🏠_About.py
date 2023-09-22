import streamlit as st

st.markdown(
"""
# About

This web application is the result of the thesis work carried out by engineer Leonardo Dal Ronco: "Explainable Artificial Intelligence applied to LSTM Neural Networks for lithium-ion batteries capacity estimation".
The two goals of this thesis work were:
- Implement an LSTM neural network with the same structure as the network described by [Ansari, S. (2021)](https://www.mdpi.com/2071-1050/13/23/13333), simpler than the ones described by [Choi, Y. (2019)](https://ieeexplore.ieee.org/abstract/document/8731962/) and [Park, K. (2020)](https://ieeexplore.ieee.org/abstract/document/8967059), but able to obtain the same results in terms of accuracy. A simpler network improves the subsequent explainability of the network.
- Apply explainability techniques to the network obtained previously, in order to provide a tool that can help evaluate the trust that can be placed in this model.

The web application is structured as follows:
- **NASA Battery Dataset**: on this page it is possible to interact with the data contained in the [NASA Li-ion Battery Aging Dataset](https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository), used to train the implemented LSTM neural network. This dataset reports the data of 4 batteries, labeled as B0005, B0006, B0007, B0018, that were run through 3 different operational profiles (charge, discharge and impedance) at room temperature.
- **LSTM Capacity Prediction**: on this page it is possible to interact with the implemented LSTM model, evaluating the accuracy of the predictions processed by the neural network.
- **Explainability**: on this page it is possible to observe the results of the Explainability techniques applied to the LSTM model implemented for estimating the capacity of a lithium battery.
"""
)