#!/usr/bin/env python3

"""
parse_mgm.py root_dir
root_dir: folder containing the files listed below
prints fasta to stdout


184sample.uniq_gene.NR.anno.merge.gz
29_GL0004906    1/1     Clostridiales   order   root|cellular organisms|Bacteria|Firmicutes|Clostridia|Clostridiales    no rank|no rank|superkingdom|phylum|class|order

184sample_2.6M.GeneSet.pep.gz
>S-Fe10_GL0000007  [gene]  locus=scaffold65241_2:873:1022:+ [Complete] codon-table.11

MmCAG2geneID.txt.gz
MmMGS:0001 MH-0-5_GL0123062

sigh... no taxid




OUT:
>S-Fe10_GL0003403|[gene]  locus=scaffold65558_1:4632:5072:+ [Complete] codon-table.11|mgm||taxon=Bacteroidales
MMVGGGTNKSPPPFFICFMEKNAAKIVSSAVLGMDFRTAVINGKVYMISPPTIHKIAGAGYYLSGLKGDNDLDAVLGMMKDMGNAAHALSYLINGDDSLFDELSHGTVEEVVNALKEGLSLISVENFMTLSVSARNVANLIAKQKQ

or

>S-Fe10_GL0003387|[gene]  locus=scaffold62376_1:581:976:- [Complete] codon-table.11|mgm||
MGKKILTWIETHWIATTVMTMAIVGAIVMTPILTSRWILDGKVKQYQNLLKTEESAEETTQKEQFEIEIMENPEEYKIVTKYKKPMKNWTKSEKTEFLEKVEELQQAQEGARKIENFVRSGLEDNQNSEIE

"""


import os
import sys
import gzip
from fasta_io import parser, Writer
import pandas as pd

database = "mgm"

root_dir = os.path.expanduser(sys.argv[1])
tax_file = os.path.join(root_dir, "184sample.uniq_gene.NR.anno.merge.gz")
pep_file = os.path.join(root_dir, "184sample_2.6M.GeneSet.pep.gz")

tax = pd.read_csv(tax_file, sep="\t", names=['id', '?', 'name', 'rank', '??', '???'])
tax = tax.set_index("id")
taxd = dict(tax['name'])
del tax

writer = Writer(sys.stdout)
f = gzip.open(pep_file, 'rt', encoding='utf8')
for doc in parser(f):
    db_accession, name = doc['defline'].split(" ", 1)
    db_accession = db_accession.strip()
    name = name.strip()
    taxon = taxd.get(db_accession, '')
    if taxon:
        defline = "{}|{}|{}||taxon={}".format(db_accession, name, database, taxon)
    else:
        defline = "{}|{}|{}||".format(db_accession, name, database)
    writer.write(defline, doc['sequence'])