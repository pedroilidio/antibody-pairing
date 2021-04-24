import joblib
import pandas as pd
import onehot_encode
import feature_extraction
from pathlib import Path
from argparse import ArgumentParser

DIR_DATA = Path('data')
PATH_ONEHOT = DIR_DATA/'onehot_encoded.csv'
PATH_FEATURES = DIR_DATA/'sequence_features.csv'
PATH_MODEL = 'models/LightGBM_NT.pkl'

argparser = ArgumentParser()
argparser.add_argument('--infile', dest='infile', required=True)
args = argparser.parse_args()

if not PATH_ONEHOT.exists():
    onehot_encode.main(args.infile, PATH_ONEHOT)
# if not PATH_FEATURES.exists():
#     onehot_encode.main(args.infile, PATH_ONEHOT)

with open(PATH_MODEL, 'rb') as model_file:
    model = joblib.load(model_file)

print('Reading one-hot encoded data...')
input_data = pd.read_csv(PATH_ONEHOT)
print('Predicting values...')
predictions = pd.Series(model.predict_proba(input_data)[:,1])
predictions.name = 'prediction'
predictions.to_csv('predictions.csv', index=False)
print('Done.')

