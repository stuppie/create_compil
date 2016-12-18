#!/usr/bin/env python3

"""input file looks like
>sp|ALBU_BOVIN|
AAAAAAA
...


"""


import os
import sys
from fasta_io import parser, Writer

database = "crapome"
data_root = os.path.expanduser(sys.argv[1])
f = os.path.join(data_root, "crap.fasta")
f_out = os.path.join(os.path.expanduser(sys.argv[2]), "crap.fasta")
writer = Writer(f_out)

for doc in parser(f):
    try:
        db_accession = name = doc['defline'].split("|")[1]
    except IndexError:
        print("Error processing defline: {}".format(doc['defline']))
        continue
    defline = "{}|{}|{}||".format(db_accession, name, database)
    writer.write(defline, doc['sequence'])

writer.close()