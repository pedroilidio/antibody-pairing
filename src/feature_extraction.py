#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
import os


def main(input_path, dir_data, path_features, dir_pseinone):
    idata = pd.read_csv(input_path)
    Hchain, Lchain = idata.Hchain, idata.Lchain
    data = pd.DataFrame()

    # Build Fasta files to process data
    print('Building fasta files...')
    records = []
    i = 1
    for seq in Hchain:
        records.append(SeqRecord(Seq(seq), id='sequence #' + str(i),
                       description = 'Heavy'))
        i += 1
    SeqIO.write(records, dir_data/"fasta_heavy.fa", "fasta")

    records = []
    i = 1
    for seq in Lchain:
        records.append(SeqRecord(Seq(seq), id='sequence #'+str(i), description='Light'))
        i += 1
    SeqIO.write(records, dir_data/"fasta_light.fa", "fasta")

    path_acc = dir_pseinone/'acc.py'
    print('Running Pse-in-One 2.0 for HEAVY chains...')
    os.system(f"python2 {path_acc} {dir_data}/fasta_heavy.fa Protein ACC -out {dir_data}/fasta_heavy_ACC.out")
    print('Running Pse-in-One 2.0 for LIGHT chains...')
    os.system(f"python2 {path_acc} {dir_data}/fasta_light.fa Protein ACC -out {dir_data}/fasta_light_ACC.out")

    ACC_heavy = pd.read_csv(dir_data/"fasta_heavy_ACC.out", sep='\t', header=None)
    ACC_light = pd.read_csv(dir_data/"fasta_light_ACC.out", sep='\t', header=None)

    d = {}
    for i in range(len(ACC_heavy.iloc[0])):
        d[i] = 'ACC_heavy_' + str(i)
    ACC_heavy = ACC_heavy.rename(columns=d, inplace=False)

    d = {}
    for i in range(len(ACC_light.iloc[0])):
        d[i] = 'ACC_light_' + str(i)
    ACC_light = ACC_light.rename(columns=d, inplace=False)

    print('Counting AA by polarity...')
    data['Heavy_Length'] = Hchain.str.len()
    data['Light_Length'] = Lchain.str.len()

    print('  Counting non-polar AA...')
    data['Heavy_SmallNonpolar'] = Hchain.str.count('[GAST]')
    data['Light_SmallNonpolar'] = Lchain.str.count('[GAST]')
    print('  Counting hydrophobic AA...')
    data['Heavy_Hydrophobic'] = Hchain.str.count('[CVILPFYMW]')
    data['Light_Hydrophobic'] = Lchain.str.count('[CVILPFYMW]')

    print('  Counting polar AA...')
    data['Heavy_Polar'] = Hchain.str.count('[NQH]')
    data['Light_Polar'] = Lchain.str.count('[NQH]')

    print('  Counting charged AA...')
    data['Heavy_Negative'] = Hchain.str.count('[DE]')
    data['Light_Negative'] = Lchain.str.count('[DE]')
    data['Heavy_Positive'] = Hchain.str.count('[KR]')
    data['Light_Positive'] = Lchain.str.count('[KR]')

    print('  Counting cysteins...')
    data['Heavy_Cystein'] =  Hchain.str.count('C')
    data['Light_Cystein'] =  Lchain.str.count('C')

    data = pd.concat([data, ACC_heavy], axis=1)
    data = pd.concat([data, ACC_light], axis=1)
    data.to_csv(path_features, index=False)
    return data
