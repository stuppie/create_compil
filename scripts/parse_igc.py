"""
http://meta.genomics.cn/meta/dataTools
719     MH0265_GL0148245        13287   Complete        EUR     Firmicutes      Eubacterium     K01183  NOG12793        0.0670876085240726      0.0672897196261682      Carbohydrate Metabolism Function unknown        EUR
id,name,length,completeness,origin,phylum,genus,kegg,eggnog,


>719|MH0265_GL0148245|igc||phylum=Firmicutes,genus=Eubacterium,kegg=K01183,eggnog=NOG12793

python3 parse_igc.py <(zcat IGC.annotation_OF.summary.gz) <(zcat IGC.pep.gz) | gzip > igc.fa.gz

"""
import sys

from tqdm import tqdm

from fasta_io import parser, Writer

annotation_path = sys.argv[1]
fasta_path = sys.argv[2]

#annotation_path = "IGC.annotation_OF.summary.gz"
#fasta_path = "IGC.pep.gz"

d = dict()
for line in tqdm(open(annotation_path), mininterval=1):
    _id, name, length, completeness, origin, phylum, genus, kegg, eggnog, *rest = line.split("\t")
    xrefs = []

    if phylum != "unknown":
        xrefs.append("phylum=" + phylum)

    if genus != "unknown":
        xrefs.append("genus=" + genus)

    if kegg != "unknown":
        xrefs.append("kegg=" + kegg)

    if eggnog != "unknown":
        xrefs.append("eggnog=" + eggnog)

    xrefs = ','.join(xrefs)

    out = "{}|{}|igc||{}".format(_id, name, xrefs)
    d[name] = out

w = Writer(sys.stdout)
for rec in parser(fasta_path):
    name = rec['defline'].split(" ")[0]
    w.write(d[name], rec['sequence'])

