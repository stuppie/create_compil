"""
python3 name_fasta_from_bed.py ../data/hmp2/v2/SRS011061.bed ../data/hmp2/v2/SRS011061.out.fna > ../data/hmp2/v2/SRS011061.out.fna2

"""

import sys
from fasta_io import parser, Writer

d = dict()
for line in open(sys.argv[1]):
    line = line.split("\t")
    d[line[0]] = line[9].strip()

w = Writer(sys.stdout)
for rec in parser(sys.argv[2]):
    rec['defline'] = rec['defline'] + "," + d[rec['defline'].split(":")[0]]
    w.write(rec['defline'], rec['sequence'])