#!/usr/bin/env python3

"""
usage:
parse_refseq.py in_file out_file

"""

import os
import sys
from itertools import chain

from fasta_io import Writer
import gzip
from Bio import SeqIO

database = "refseq_" + os.path.split(sys.argv[1])[1].split(".")[0]
f = sys.argv[1]
parser = SeqIO.parse(gzip.open(f, 'rt', encoding='utf8'), 'gb')
writer = Writer(sys.argv[2])

for record in parser:
    try:
        tax_ids = [f.qualifiers['db_xref'] for f in record.features if f.type == 'source']
        assert (len(tax_ids) == 1)
        tax_ids = tax_ids[0]
        tax_ids = [t for t in tax_ids if t.startswith('taxon:')]
        assert (len(tax_ids) == 1)
        tax_id = str(tax_ids[0])
        tax_id = tax_id.replace("taxon:", "")
    except:
        tax_id = None

    db_accession = ','.join(record.annotations['accessions'])
    if 'sequence_version' in record.annotations:
        db_accession = db_accession + '.' + str(record.annotations['sequence_version'])

    record.description = record.description.strip()
    descr = record.description if not record.description.endswith('.') else record.description[:-1]

    # TODO: assert no stray commas or equals in these values....
    annotations = set(record.dbxrefs)
    annotations.update(set(chain(*[x for x in [f.qualifiers.get("db_xref") for f in record.features] if x])))
    ann_str = ",".join([x.split(":")[0] + "=" + x.split(":",1)[1] for x in annotations])

    if tax_id:
        writer.write('|'.join([db_accession, descr, database, "taxid:" + tax_id, ann_str]), str(record.seq))
    else:
        writer.write('|'.join([db_accession, descr, database, "", ann_str]), str(record.seq))