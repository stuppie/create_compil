"""
parse_food.py input_file
input_file: full path to gzipped fasta file. downloaded from uniprot

will print to stdout

>sp|P02604|MLE1_CHICK Myosin light chain 1, skeletal muscle isoform OS=Gallus gallus PE=1 SV=3

"""


import os
import sys
import gzip
from fasta_io import parser, Writer

database = "food"
data_root = os.path.expanduser(sys.argv[1])

f_path = os.path.expanduser(sys.argv[1])
taxid = os.path.split(f_path)[1].split(".")[0]
f = gzip.open(f_path, 'rt', encoding='utf8')
writer = Writer(sys.stdout)

for doc in parser(f):
    _, db_accession, *name = doc['defline'].split("|")
    if isinstance(name, list):
        name = '|'.join(name)
    defline = "{}|{}|{}|taxid:{}|".format(db_accession, name, database, taxid)
    writer.write(defline, doc['sequence'])

writer.close()