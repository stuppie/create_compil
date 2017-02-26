"""
python3 fasta_translate.py ../data/hmp2/v2/SRS011061.out.fna > ../data/hmp2/v2/SRS011061.out.fa

"""

import sys
from fasta_io import parser, Writer
from Bio.Seq import Seq


w = Writer(sys.stdout)
for rec in parser(sys.stdin):
    s = str(Seq(rec['sequence']).translate(to_stop=True))
    w.write(rec['defline'], s)