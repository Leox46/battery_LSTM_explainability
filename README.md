# About

This [web application](https://battery-lstm-explainability.streamlit.app/) is the tool presented in the paper entitled "Enhancing Battery Capacity Estimation with an Efficient LSTM Model and Explainability Features".
The main goals of the presented work are:
- Propose a novel efficient LSTM model, which is able to perform like the state-of-the-art models, but with a simpler architecture that can enhance its efficiency, training time, and ease the adoption of explainability techniques.
- Then, apply explainability techniques to the network obtained previously, in order to provide a tool that can help evaluate the trust that can be placed in this model.

The web application is structured as follows:
- **NASA Battery Dataset**: on this page it is possible to interact with the data contained in the [NASA Li-ion Battery Aging Dataset](https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository), used to train the implemented LSTM neural network. This dataset reports the data of 4 batteries, labeled as B0005, B0006, B0007, B0018, that were run through 3 different operational profiles (charge, discharge and impedance) at room temperature.
- **LSTM Capacity Prediction**: on this page it is possible to interact with the implemented LSTM model, evaluating the accuracy of the predictions processed by the neural network.
- **Explainability**: on this page it is possible to observe the results of the Explainability techniques applied to the LSTM model implemented for estimating the capacity of a lithium battery.
