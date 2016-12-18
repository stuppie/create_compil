#!/usr/bin/env python3

"""
usage:
parse_uniprot.py in_file out_file

"""

import os
import sys
from fasta_io import Writer
from Bio import SwissProt
import gzip

database = os.path.split(sys.argv[1])[1].split(".")[0]
parser = SwissProt.parse(gzip.open(sys.argv[1]))
writer = Writer(sys.argv[2])
while True:
    try:
        record = next(parser)
    except StopIteration:
        break
    except Exception as e:
        print(e, file=sys.stderr)
        continue
    tax_id = str(record.taxonomy_id[0])
    descr = record.description if not record.description.endswith(';') else record.description[:-1]
    descr = descr.replace("RecName: Full=","")
    db_accession = ','.join(record.accessions)

    # TODO: assert no stray commas or equals in these values....
    annotations = ",".join([x[0]+"="+x[1] for x in record.cross_references])

    writer.write('|'.join([db_accession, descr, database, "taxid:" + tax_id, annotations]), record.sequence)