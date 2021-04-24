import joblib
import pandas as pd
import preprocessing
from argparse import ArgumentParser

PATH_MODEL = 'models/LightGBM_NT.pkl'
argparser = ArgumentParser()
argparser.add_argument('--infile', dest='infile', required=True)
args = argparser.parse_args()

#if not preprocessing.DIR_DATA.exists():
preprocessing.main(args.infile)

with open(PATH_MODEL, 'rb') as model_file:
    model = joblib.load(model_file)

print('Reading preprocessed data...')
input_data = pd.read_csv(preprocessing.PATH_PREPROCESSED)
print('Predicting values...')
predictions = pd.Series(model.predict_proba(input_data)[:,1])
predictions.name = 'prediction'
predictions.to_csv('predictions.csv', index=False)

