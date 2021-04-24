#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from glob import glob
import numpy as np
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
import os

data = pd.read_csv('input.csv')

# Builds Fasta files to process data
records = []
i = 1
for seq in data['Hchain']:
    records.append(SeqRecord(Seq(seq), id='sequence #' + str(i),
                   description = 'Heavy'))
    i += 1
SeqIO.write(records, "fasta_heavy.fa", "fasta")

records = []
i = 1
for seq in data['Lchain']:
    records.append(SeqRecord(Seq(seq),id = 'sequence #' + str(i),description = 'Light'))
    i += 1
SeqIO.write(records, "fasta_light.fa", "fasta")


# In[40]:


os.system("python2 acc.py fasta_heavy.fa Protein ACC -out fasta_heavy_ACC.out")
os.system("python2 acc.py fasta_light.fa Protein ACC -out fasta_light_ACC.out")


# In[41]:


ACC_heavy = pd.read_csv("fasta_heavy_ACC.out",sep = '\t', header = None)
ACC_light = pd.read_csv("fasta_heavy_ACC.out",sep = '\t', header = None)


# In[42]:


d = {}
for i in range(len(ACC_heavy.iloc[0])):
    d[i] = 'ACC_heavy_' + str(i)
ACC_heavy = ACC_heavy.rename(columns = d, inplace = False)

d = {}
for i in range(len(ACC_light.iloc[0])):
    d[i] = 'ACC_light_' + str(i)
ACC_light = ACC_light.rename(columns = d, inplace = False)


# In[43]:


data['Heavy_Length'] = data['Hchain'].str.len()
data['Light_Length'] = data['Lchain'].str.len()

data['Heavy_SmallNonpolar'] = data['Hchain'].str.count('G') + data['Hchain'].str.count('A') + data['Hchain'].str.count('S') + data['Hchain'].str.count('T')

data['Light_SmallNonpolar'] = data['Lchain'].str.count('G') + data['Lchain'].str.count('A') + data['Lchain'].str.count('S') + data['Lchain'].str.count('T')

data['Heavy_Hydrophobic'] =   data['Hchain'].str.count('C') + data['Hchain'].str.count('V') + data['Hchain'].str.count('I') + data['Hchain'].str.count('L') + data['Hchain'].str.count('P') + data['Hchain'].str.count('F') + data['Hchain'].str.count('Y') + data['Hchain'].str.count('M') + data['Hchain'].str.count('W')

data['Light_Hydrophobic'] =   data['Lchain'].str.count('C') + data['Lchain'].str.count('V') + data['Lchain'].str.count('I') + data['Lchain'].str.count('L') + data['Lchain'].str.count('P') + data['Lchain'].str.count('F') + data['Lchain'].str.count('Y') + data['Lchain'].str.count('M') + data['Lchain'].str.count('W')

data['Heavy_Polar'] = data['Hchain'].str.count('N') + data['Hchain'].str.count('Q') + data['Hchain'].str.count('H') 

data['Light_Polar'] = data['Lchain'].str.count('N') + data['Lchain'].str.count('Q') + data['Lchain'].str.count('H')

data['Heavy_Negative'] = data['Hchain'].str.count('D') + data['Hchain'].str.count('E') 

data['Light_Negative'] = data['Lchain'].str.count('D') + data['Lchain'].str.count('E') 

data['Heavy_Positive'] = data['Hchain'].str.count('K') + data['Hchain'].str.count('R') 

data['Light_Positive'] = data['Lchain'].str.count('K') + data['Lchain'].str.count('R') 

data['Heavy_Cystein'] =  data['Hchain'].str.count('C') 

data['Light_Cystein'] =  data['Lchain'].str.count('C')

data = pd.concat([data, ACC_heavy],
                           axis=1)
data = pd.concat([data, ACC_light],
                           axis=1)
data


# In[34]:




