#!/usr/bin/env python3

"""
annotation and fasta file have on IDs in common??!!?

frequent_microbe_proteins.fasta.gz


"""


import os
import sys
import gzip
from fasta_io import parser, Writer

database = "mgm"
data_root = os.path.expanduser(sys.argv[1])
f = gzip.open(os.path.join(data_root, "frequent_microbe_proteins.fasta.gz"), 'rt', encoding='utf8')
f_out = os.path.join(os.path.expanduser(sys.argv[2]), "metahit.fasta")
writer = Writer(f_out)

for doc in parser(f):
    db_accession = name = doc['defline']
    defline = "{}|{}|{}||".format(db_accession, name, database)
    writer.write(defline, doc['sequence'])

writer.close()