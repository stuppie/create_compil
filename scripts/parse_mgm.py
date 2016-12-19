#!/usr/bin/env python3

"""

184sample.uniq_gene.NR.anno.merge.gz
29_GL0004906    1/1     Clostridiales   order   root|cellular organisms|Bacteria|Firmicutes|Clostridia|Clostridiales    no rank|no rank|superkingdom|phylum|class|order

184sample_2.6M.GeneSet.pep.gz
>S-Fe10_GL0000007  [gene]  locus=scaffold65241_2:873:1022:+ [Complete] codon-table.11

MmCAG2geneID.txt.gz
MmMGS:0001 MH-0-5_GL0123062

"""


import os
import sys
import gzip
from fasta_io import parser, Writer

database = "mgm"
