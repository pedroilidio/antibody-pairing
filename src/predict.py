import joblib
import pandas as pd
import onehot_encode
import feature_extraction
from pathlib import Path
from argparse import ArgumentParser

DIR_PSEINONE = Path('Pse-in-One-2.0')
DIR_DATA = Path('preprocessed_input')
PATH_ONEHOT = DIR_DATA/'onehot_encoded.csv'
PATH_FEATURES = DIR_DATA/'sequence_features.csv'
PATH_PREPROCESSED = DIR_DATA/'preprocessed.csv'
#PATH_MODEL = 'models/LightGBM_NT.pkl'  # Only receives 1hot seqs.
PATH_MODEL = 'models/LightGBM_NT.pkl'


def preprocess(infile, path_onehot=PATH_ONEHOT,
               dir_data=DIR_DATA, path_features=PATH_FEATURES,
               dir_pseinone=DIR_PSEINONE,
               path_preprocessed=PATH_PREPROCESSED):

    onehot_encoded = onehot_encode.main(infile, path_onehot)
    seq_features = feature_extraction.main(infile, dir_data,
                                           path_features, dir_pseinone)
    input_data = pd.concat((seq_features, onehot_encoded), axis=1)
    input_data.to_csv(path_preprocessed, index=False)
    return input_data


def main():
    argparser = ArgumentParser()
    argparser.add_argument('--infile', dest='infile', required=True)
    args = argparser.parse_args()

    input_data = preprocess(args.infile)

    print('Loading model...')
    with open(PATH_MODEL, 'rb') as model_file:
        model = joblib.load(model_file)

    print('Predicting values...')
    apreds = model.predict_proba(input_data)
    predictions = pd.Series(((1-apreds[:,0]) + apreds[:,1])/2)
    predictions.name = 'prediction'
    predictions.to_csv('predictions.csv', index=False)
    print('Done.')


if __name__ == '__main__':
    res = main()
