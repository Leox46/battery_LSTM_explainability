import streamlit as st

st.markdown(
"""
Questa applicazione web è il risultato del lavoro di tesi svolto da Leonardo Dal Ronco: “Explainability applicata a reti neurali LSTM per la stima della capacità di batterie al litio” [link].
I due obbiettivi di questo lavoro di tesi sono stati:
- Implementare una rete neurale LSTM più semplice rispetto a quelle descritte in letteratura [riferimenti], ma in grado di ottenere gli stessi risultati in termini di accuratezza. Una rete più semplice migliorarne la successiva spiegabilità della stessa.
- Applicare le principali tecniche di Explainability alla rete ottenuta in precedenza, in modo da fornire uno strumento in grado di aiutare a valutare la fiducia che è possibile riporre in tale modello.

L’applicazione web è strutturata come segue:
- NASA Dataset: in questa pagina è possibile interagire con i dati contenuti all’interno del NASA Li-ion Battery Aging Dataset [link / riferimenti], utilizzato per addestrare la rete neurale LSTM implementata. In questo dataset, sono riportati i dati dei cicli di carica - scarica effettuati dal NASA Li-ion Battery Aging Dataset [link / riferimenti] su 4 batterie, etichettate come B0005, B0006, B0007, B0018.
- LSTM Model: in questa pagina è possibile interagire con il modello LSTM implementato, valutando l’accuratezza delle previsioni elaborate dalla rete neurale.
- Explainability: in questa pagina è possibile osservare i risultati delle tecniche di Explainability applicate al modello LSTM implementato per la stima della capacità di una batteria al litio.
"""
)