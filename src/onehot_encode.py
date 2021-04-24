# Pre Processing

import pandas as pd
from glob import glob
import numpy as np
from pathlib import Path


def main(infile, path_onehot):
    ### Principal Dataset
    print(f'Reading {infile}...')
    data = pd.read_csv(infile)

    # Aliases.
    Heavy_Partial = data[['Hchain']].copy()
    Light_Partial = data[['Lchain']].copy()

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
    AMINO = 'ARNDCEQGHILKMFPSTWYV'

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
    onehot_encoded.to_csv(path_onehot, index=False)
    return onehot_encoded
