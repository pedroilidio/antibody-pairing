# Holy-BioMole
We are students in Biomolecular Sciences from the University of São Paulo, Brazil, and we think proteins are cool (but shouldn't be too cool, it would ruin their nice curves) 🙌


### Project Description
We are working on the `antibody-pairing` challenge.

Our current best predictor (version 0.0.6) applies one-hot encoding to the pair of possible interacting heavy and light chain sequences provided in the input and classifies the possibility of interaction using a LightGBM classifier.

We are currently working to improve the prediction by considering biochemical features extracted from the data, such as amino acid content and auto-cross correlation of the chemical properties of the amino acids.

To predict using our model, press "Open Application" on the left. 

### Scoreboard
You can track the performance of our predictor in the [challenge scoreboard](https://biolib.com/biohackathon/antibody-pairing-scoreboard/).
