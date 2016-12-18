import sys
from fasta_io import Writer, parser
database = "hmgi_srs"

f = sys.stdin
id_dict = dict()
line = ''
while True:
    line = next(f)
    if line.strip() == "##FASTA":
        break
    if line.startswith('#'):
        continue
    line = line.split('\t')
    if line[2] != "CDS":
        continue
    descr_dict = dict(d.split('=') for d in line[8].split(';'))
    id_dict[descr_dict['ID']] = (descr_dict['product'].strip(), descr_dict.get('Ontology_term', '').strip())


w = Writer(sys.stdout)
for fasta_record in parser(sys.stdin):
    if fasta_record['sequence'].count('x'):
        continue
    if "scaffold" in fasta_record['defline']:
        continue
    if len(set(list(fasta_record['sequence']))) <= 4:
        continue
    db_accession = fasta_record['defline']
    name = id_dict.get(db_accession, [''])[0]
    metadata = id_dict.get(db_accession, ['',''])[1]

    if metadata:
        metadata = ",".join(["GO=" + x for x in metadata.split(",")])

    defline = "{}|{}|{}|{}|{}".format(db_accession, name, database, '', metadata)

    w.write(defline, fasta_record['sequence'])