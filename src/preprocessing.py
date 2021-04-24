# Pre Processing

import pandas as pd
from glob import glob
import numpy as np
from pathlib import Path

DIR_DATA = Path('data')
PATH_PREPROCESSED = DIR_DATA/'preprocessed.csv'

def main(infile):
    DIR_DATA.mkdir(exist_ok=True)
    ### Principal Dataset
    print(f'Reading {infile}...')
    data = pd.read_csv(infile)
    # Alias when not using sequence features.
    Heavy_Partial = data[['Hchain']].copy()
    Light_Partial = data[['Lchain']].copy()

    # ### Load New columns
    # SeqsHeavy = pd.read_csv('SeqsHeavyRenan.csv')
    # SeqsLight = pd.read_csv('SeqsLightRenan.csv')
    # SeqsHeavy = SeqsHeavy.drop('Unnamed: 0', axis=1)
    # SeqsLight = SeqsLight.drop('Unnamed: 0', axis=1)
    # ACC_Heavy = pd.read_csv('ACC_data_heavy.zip')
    # ACC_Light = pd.read_csv('ACC_data_light.zip')

    # #### Join Columns
    # Heavy_Partial = pd.concat([SeqsHeavy, ACC_Heavy],
    #                            axis=1)
    # Heavy_Partial['Hchain'] = result_df['Hchain']
    # Heavy_Shuffled_Partial = pd.concat([SeqsHeavy, ACC_Heavy],
    #                            axis=1)
    # Heavy_Shuffled_Partial['Hchain'] = result_df['Hchain']
    # Light_Partial = pd.concat([SeqsLight, ACC_Light],
    #                            axis=1)
    # Light_Partial['Lchain'] = result_df['Lchain']

    #### Get_dummies For Sequence
    print('One-hot encoding sequences...')
    ByPosition_Amino_Heavy = Heavy_Partial['Hchain'].apply(lambda x:pd.Series(list(x)))
    Light_Partial['Lchain'] = Light_Partial['Lchain'].astype(str)
    ByPosition_Amino_Light = Light_Partial.Lchain.apply(lambda x:pd.Series(list(x)))

    Heavy_Partial = Heavy_Partial.drop(['Hchain'], axis=1)
    Heavy_Partial = pd.concat([Heavy_Partial, pd.get_dummies(ByPosition_Amino_Heavy)], axis=1)

    Light_Partial = Light_Partial.drop(['Lchain'], axis=1)
    Light_Partial = pd.concat([Light_Partial, pd.get_dummies(ByPosition_Amino_Light)], axis=1)

    Heavy_Partial = Heavy_Partial.add_suffix('_heavy')
    Light_Partial = Light_Partial.add_suffix('_light')

    POSITION = list(range(0, 151))
    AMINO = ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V']

    for i in POSITION:
        for j in AMINO:
            new_col = str(i) + "_" + str(j)+ "_heavy"
            if str(new_col) not in Heavy_Partial:
                Heavy_Partial[str(new_col)] = 0

    for i in POSITION:
        for j in AMINO:
            new_col = str(i) + "_" + str(j)+ "_light"
            if str(new_col) not in Light_Partial:
                Light_Partial[str(new_col)] = 0

    onehot_encoded = pd.concat([Heavy_Partial, Light_Partial], axis=1)
    # preprocessed_input = pd.concat()
    preprocessed_input = onehot_encoded
    preprocessed_input.to_csv(PATH_PREPROCESSED, index=False)
