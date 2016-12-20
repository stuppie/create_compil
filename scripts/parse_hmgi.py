#!/usr/bin/env python3

"""
parse_hmgi.py HMGI_DATA

HMGI_DATA: path to folder containing "Gastrointestinal_tract.pep.fsa". will be used to store temp files

writes to stdout

input file looks like:
>CW1_2700 transcriptional regulator, LuxR family [Bacteroides xylanisolvens SD CC 2a]
MKNNEVVRIAIAETSVIIRGGLTAALKRLSNVKVQPIELLSVEALHDCVRTQCPEMLIVN
PAFGDYFDVAKFREEISGKRIRLIALVTSFVDASLLGKYDESISIFDDLETLSKKIAGLL
NVVSEEEGMDNQDTLSQREKEIVICVVKGMTNKEIAEKLFLSIHTVITHRRNISKKLQIH
SAAGLTIYAIVNKLVALSDVKDL


output:
>CW1_2700|transcriptional regulator, LuxR family [Bacteroides xylanisolvens SD CC 2a]|hmgi_ref|taxid:702444|
MKNNEVVRIAIAETSVIIRGGLTAALKRLSNVKVQPIELLSVEALHDCVRTQCPEMLIVNPAFGDYFDVAKFREEISGKRIRLIALVTSFVDASLLGKYDESISIFDDLETLSKKIAGLLNVVSEEEGMDNQDTLSQREKEIVICVVKGMTNKEIAEKLFLSIHTVITHRRNISKKLQIHSAAGLTIYAIVNKLVALSDVKDL

"""

import os
import sys

import requests
from tqdm import tqdm

from fasta_io import Writer, parser
import pickle

database = "hmgi_ref"
data_root = os.path.expanduser(sys.argv[1])

def parse_brackets(string):
    """Generate parenthesized contents in string as pairs (level, contents).
    http://stackoverflow.com/questions/4284991/parsing-nested-parentheses-in-python-grab-content-by-level
    """
    if string.count('[') != string.count(']'):
        return None
    stack = []
    for i, c in enumerate(string):
        if c == '[':
            stack.append(i)
        elif c == ']' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])

def get_organisms():
    with open(os.path.join(data_root, "Gastrointestinal_tract.pep.fsa")) as f:
        for line in f:
            if line.startswith('>'):
                brackets = parse_brackets(line)
                organism = [x[1] for x in brackets if x[0] == 0][-1]
                yield organism


def lookup_organisms_taxid():

    organisms = set(get_organisms())
    url = "http://www.ebi.ac.uk/ena/data/taxonomy/v1/taxon/any-name/{}"
    taxdict = {}
    for organism in tqdm(organisms):
        response = requests.get(url.format(organism))
        if response.status_code == 200:
            r = response.json()
            taxid = r[0]['taxId']
            taxdict[organism] = taxid
    return taxdict


taxdict_path = os.path.join(data_root, "taxdict.pkl")
if os.path.exists(os.path.join(data_root, "taxdict.pkl")):
    with open(taxdict_path, 'rb') as f:
        taxdict = pickle.Unpickler(f).load()
else:
    taxdict = lookup_organisms_taxid()
    with open(taxdict_path,'wb') as f:
        pickle.Pickler(f).dump(taxdict)


writer = Writer(sys.stdout)

with open(os.path.join(data_root, "Gastrointestinal_tract.pep.fsa")) as f:
    p = parser(f)
    for fasta_record in p:
        defline = fasta_record['defline']
        brackets = parse_brackets(defline)
        organism = [x[1] for x in brackets if x[0] == 0][-1]
        db_accession = defline.split(' ')[0].strip()
        name = defline[defline.index(' '):].strip()
        if organism in taxdict:
            defline = "{}|{}|{}|taxid:{}|".format(db_accession, name, database, taxdict[organism])
        else:
            defline = "{}|{}|{}||".format(db_accession, name, database)
        writer.write(defline, fasta_record['sequence'])

writer.close()