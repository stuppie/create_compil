"""
>1:102-1212(+),ID=SRS011310.polypeptide.8;Parent=SRS011310.mRNA.8;Dbxref=EC:2.1.1.74;product_name=tRNA:m(5)U-54 methyltransferase;Ontology_term=GO:0006400,GO:0016740
>1:102-1212(+),ID=SRS011310.polypeptide.8|tRNA:m(5)U-54 methyltransferase|hmp2||dbxref=EC:2.1.1.74,go=GO:0006400,go=GO:0016740

"""

import sys
from fasta_io import parser, Writer

w = Writer(sys.stdout)
for rec in parser(sys.stdin):
    defline = rec['defline']
    _id, *rest = defline.split(";")
    d = dict(x.split('=') for x in rest)

    xrefs=[]
    onto = d.get("Ontology_term", '')
    if onto:
        for x in onto.split(","):
            xrefs.append(("go", x))
    xref = d.get("Dbxref", '')
    if xref:
        xrefs.append(("dbxref", xref))
    xrefs = ",".join([k + "=" + v for k,v in xrefs])
    name = d.get("product_name", '')
    out = "{}|{}|hmp2||{}".format(_id, name, xrefs)

    w.write(out, rec['sequence'])