#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from glob import glob
import numpy as np
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
import os


def main(input_path, dir_data, path_features):
    data = pd.read_csv(input_path)

    # Builds Fasta files to process data
    records = []
    i = 1
    for seq in data['Hchain']:
        records.append(SeqRecord(Seq(seq), id='sequence #' + str(i),
                       description = 'Heavy'))
        i += 1
    SeqIO.write(records, dir_data/"fasta_heavy.fa", "fasta")

    records = []
    i = 1
    for seq in data['Lchain']:
        records.append(SeqRecord(Seq(seq), id='sequence #'+str(i), description='Light'))
        i += 1
    SeqIO.write(records, dir_data/"fasta_light.fa", "fasta")

    os.system(f"python2 acc.py {dir_data}/fasta_heavy.fa Protein ACC -out {dir_data}/fasta_heavy_ACC.out")
    os.system(f"python2 acc.py {dir_data}/fasta_light.fa Protein ACC -out {dir_data}/fasta_light_ACC.out")

    ACC_heavy = pd.read_csv(dir_data/"fasta_heavy_ACC.out", sep='\t', header=None)
    ACC_light = pd.read_csv(dir_data/"fasta_heavy_ACC.out", sep='\t', header=None)

    d = {}
    for i in range(len(ACC_heavy.iloc[0])):
        d[i] = 'ACC_heavy_' + str(i)
    ACC_heavy = ACC_heavy.rename(columns=d, inplace=False)

    d = {}
    for i in range(len(ACC_light.iloc[0])):
        d[i] = 'ACC_light_' + str(i)
    ACC_light = ACC_light.rename(columns=d, inplace=False)

    data['Heavy_Length'] = data['Hchain'].str.len()
    data['Light_Length'] = data['Lchain'].str.len()

    data['Heavy_SmallNonpolar'] = data['Hchain'].str.count('[GAST]')
    data['Light_SmallNonpolar'] = data['Lchain'].str.count('[GAST]')
    data['Heavy_Hydrophobic'] = data['Hchain'].str.count('[CVILPFYMW]')
    data['Light_Hydrophobic'] = data['Lchain'].str.count('[CVILPFYMW]')

    data['Heavy_Polar'] = data['Hchain'].str.count('[NQH]')
    data['Light_Polar'] = data['Lchain'].str.count('[NQH]')

    data['Heavy_Negative'] = data['Hchain'].str.count('[DE]')
    data['Light_Negative'] = data['Lchain'].str.count('[DE]')
    data['Heavy_Positive'] = data['Hchain'].str.count('[KR]')
    data['Light_Positive'] = data['Lchain'].str.count('[KR]')

    data['Heavy_Cystein'] =  data['Hchain'].str.count('C')
    data['Light_Cystein'] =  data['Lchain'].str.count('C')

    data = pd.concat([data, ACC_heavy], axis=1)
    data = pd.concat([data, ACC_light], axis=1)
    data.to_csv(path_features, index=False)
