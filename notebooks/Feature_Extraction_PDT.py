#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from glob import glob
import numpy as np
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
import os

data = pd.read_csv('mydata.csv')
new_data = data[['sequence_alignment_aa_heavy', 'sequence_alignment_aa_light']]
result_df = new_data.drop_duplicates(subset=['sequence_alignment_aa_heavy', 'sequence_alignment_aa_light'])


# Builds Fasta files to process data
records = []
i = 1
for seq in result_df['sequence_alignment_aa_heavy']:
    records.append(SeqRecord(Seq(seq),id = 'sequence #' + str(i),description = 'Heavy'))
    i += 1
SeqIO.write(records, "fasta_heavy.fa", "fasta")

records = []
i = 1
for seq in result_df['sequence_alignment_aa_light']:
    records.append(SeqRecord(Seq(seq),id = 'sequence #' + str(i),description = 'Light'))
    i += 1
SeqIO.write(records, "fasta_light.fa", "fasta")

os.system("python2 acc.py fasta_heavy.fa Protein ACC -out fasta_heavy_ACC.out")
os.system("python2 acc.py fasta_light.fa Protein ACC -out fasta_light_ACC.out")
os.system("python2 acc.py fasta_heavy.fa Protein PDT -out fasta_heavy_PDT.out")
os.system("python2 acc.py fasta_light.fa Protein PDT -out fasta_light_PDT.out")

ACC_heavy = pd.read_csv("fasta_heavy_ACC.out",sep = '\t', header = None)
ACC_light = pd.read_csv("fasta_light_ACC.out",sep = '\t', header = None)
PDT_heavy = pd.read_csv("fasta_heavy_PDT.out",sep = '\t', header = None)
PDT_light = pd.read_csv("fasta_light_PDT.out",sep = '\t', header = None)

d = {}
for i in range(len(ACC_heavy.iloc[0])):
    d[i] = 'ACC_heavy_' + str(i)
ACC_heavy = ACC_heavy.rename(columns = d, inplace = False)

d = {}
for i in range(len(ACC_light.iloc[0])):
    d[i] = 'ACC_light_' + str(i)
ACC_light = ACC_light.rename(columns = d, inplace = False)

d = {}
for i in range(len(PDT_heavy.iloc[0])):
    d[i] = 'PDT_heavy_' + str(i)
PDT_heavy = PDT_heavy.rename(columns = d, inplace = False)

d = {}
for i in range(len(PDT_light.iloc[0])):
    d[i] = 'PDT_light_' + str(i)
PDT_light = PDT_light.rename(columns = d, inplace = False)

Heavy_Partial = result_df['sequence_alignment_aa_heavy']
Heavy_Partial.index = ACC_heavy.index
Heavy_Partial

Heavy_Sequence = result_df['sequence_alignment_aa_heavy']
Heavy_Sequence.index = ACC_heavy.index
Light_Sequence = result_df['sequence_alignment_aa_light']
Light_Sequence.index = ACC_light.index

Heavy_Partial = pd.DataFrame()
Light_Partial = pd.DataFrame()
Heavy_Partial['Heavy_Length'] = Heavy_Sequence.str.len()
Light_Partial['Light_Length'] = Light_Sequence.str.len()

Heavy_Partial['Heavy_SmallNonpolar'] = Heavy_Sequence.str.count('[GAST]')

Light_Partial['Light_SmallNonpolar'] = Light_Sequence.str.count('[GAST]')

Heavy_Partial['Heavy_Hydrophobic'] = Heavy_Sequence.str.count('[CVILPFYMW]')

Light_Partial['Light_Hydrophobic'] = Light_Sequence.str.count('[CVILPFYMW]')

Heavy_Partial['Heavy_Polar'] = Heavy_Sequence.str.count('[NQH]')

Light_Partial['Light_Polar'] = Light_Sequence.str.count('[NQH]')

Heavy_Partial['Heavy_Negative'] = Heavy_Sequence.str.count('[DE]')

Light_Partial['Light_Negative'] = Light_Sequence.str.count('[DE]')

Heavy_Partial['Heavy_Positive'] = Heavy_Sequence.str.count('[KR]')

Light_Partial['Light_Positive'] = Light_Sequence.str.count('[KR]')

Heavy_Partial['Heavy_Cystein'] =  Heavy_Sequence.str.count('C') 

Light_Partial['Light_Cystein'] =  Light_Sequence.str.count('C') 

Heavy_Partial = pd.concat([Heavy_Partial, ACC_heavy],
                           axis=1)
Light_Partial = pd.concat([Light_Partial, ACC_light],
                           axis=1)
Heavy_Partial = pd.concat([Heavy_Partial, PDT_heavy],
                           axis=1)
Light_Partial = pd.concat([Light_Partial, PDT_light],
                           axis=1)


# In[7]:


compression_opts = dict(method='zip',archive_name='Heavy_Partial.csv')
Heavy_Partial.to_csv('Heavy_Partial.zip', index=False,compression=compression_opts)
compression_opts = dict(method='zip',archive_name='Light_Partial.csv')
Light_Partial.to_csv('Light_Partial.zip', index=False,compression=compression_opts)

