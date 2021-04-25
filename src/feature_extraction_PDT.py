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
    os.system('chmod 777 ./pdt/pdt')
    os.system(f"python3 {path_acc} {dir_data}/fasta_heavy.fa Protein ACC -out {dir_data}/fasta_heavy_ACC.out")
    os.system('chmod 777 ./pdt/pdt')
    os.system(f"python3 {path_acc} {dir_data}/fasta_light.fa Protein PDT -out {dir_data}/fasta_light_PDT.out")

    print('Running Pse-in-One 2.0 for LIGHT chains...')
    os.system('chmod 777 ./pdt/pdt')
    os.system(f"python3 {path_acc} {dir_data}/fasta_light.fa Protein ACC -out {dir_data}/fasta_light_ACC.out")
    os.system('chmod 777 ./pdt/pdt')
    os.system(f"python3 {path_acc} {dir_data}/fasta_heavy.fa Protein PDT -out {dir_data}/fasta_heavy_PDT.out")

    ACC_heavy = pd.read_csv(dir_data/"fasta_heavy_ACC.out", sep='\t', header=None)
    ACC_light = pd.read_csv(dir_data/"fasta_light_ACC.out", sep='\t', header=None)
    PDT_heavy = pd.read_csv(dir_data/"fasta_heavy_PDT.out", sep='\t', header=None)
    PDT_light = pd.read_csv(dir_data/"fasta_light_PDT.out", sep='\t', header=None)

    ACC_heavy.columns = 'ACC_heavy_' + ACC_heavy.columns
    ACC_light.columns = 'ACC_light_' + ACC_light.columns
    PDT_heavy.columns = 'PDT_heavy_' + PDT_heavy.columns
    PDT_light.columns = 'PDT_light_' + PDT_light.columns

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

    data = pd.concat((data, ACC_heavy, ACC_light,
                      PDT_heavy, PDT_light), axis=1)
    data.to_csv(path_features, index=False)
    return data
