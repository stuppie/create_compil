#!/usr/bin/env python3

"""
parse_metahit.py
reads from stdin
writes to stdout


Uses file: frequent_microbe_proteins.fasta.gz
looks like:

>1000000853.C707.G1
MHISYQPLWDTLKERGMRKEDLRLSAGLTTNMIANMGKGKHISMETLLRI
CKALNCGILNVIELEHDEEAEISN


Output:
>1000000853.C707.G1|1000000853.C707.G1|metahit||
MHISYQPLWDTLKERGMRKEDLRLSAGLTTNMIANMGKGKHISMETLLRICKALNCGILNVIELEHDEEAEISN

"""
#TODO: annotation and fasta file have on IDs in common??!!?


import sys
from fasta_io import parser, Writer

database = "metahit"
writer = Writer(sys.stdout)

for doc in parser(sys.stdin):
    db_accession = name = doc['defline']
    defline = "{}|{}|{}||".format(db_accession, name, database)
    writer.write(defline, doc['sequence'])

writer.close()