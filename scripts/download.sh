set -e
#UniProt - accessed 11/30/2016; last updated 11/30/2016 
wget "ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/taxonomic_divisions/uniprot_sprot_*.dat.gz" -P ~/create_compil/scripts/data -nv -a download.log 
wget "ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/taxonomic_divisions/uniprot_trembl*.dat.gz" -P ~/create_compil/scripts/data -nv -a download.log

#MetaHit-Qin, et al 2010 - accessed 12/5/2016; last updated 06/2009
wget "http://www.bork.embl.de/~arumugam/Qin_et_al_2010/BGI_GeneSet20090523.fa.gz" -P ~/create_compil/scripts/data -nv -a download.log 
wget "http://www.bork.embl.de/~arumugam/Qin_et_al_2010/BGI_GeneSet20090523_annotation.fa.gz" -P ~/create_compil/scripts/data -nv -a download.log 
wget "http://www.bork.embl.de/~arumugam/Qin_et_al_2010/BGI_GeneSet20090523_taxonomic.fa.gz" -P ~/create_compil/scripts/data -nv -a download.log 
wget "http://www.bork.embl.de/~arumugam/Qin_et_al_2010/frequent_microbe_proteins.fasta.gz" -P ~/create_compil/scripts/data -nv -a download.log 

#RefSeq - accessed 12/5/2016; last updated 11/3/2016
wget "ftp://ftp.ncbi.nlm.nih.gov/refseq/release/bacteria/bacteria.nonredundant*.protein.gpff.gz" -P ~/create_compil/scripts/data -nv -a download.log 
wget "ftp://ftp.ncbi.nlm.nih.gov/refseq/release/archaea/archaea.nonredundant*.protein.gpff.gz" -P ~/create_compil/scripts/data -nv -a download.log 
wget "ftp://ftp.ncbi.nlm.nih.gov/refseq/release/fungi/fungi.*.protein.gpff.gz" -P ~/create_compil/scripts/data -nv -a download.log 
wget "ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.*.protein.gpff.gz" -P ~/create_compil/scripts/data -nv -a download.log 

#HMPI Stool - accessed 12/5/2016; last updated 2011
wget "ftp://public-ftp.hmpdacc.org/HMGI/stool/*.with_fasta.gff3.bz2" -P ~/create_compil/scripts/data -nv -a downoad.log 

#cRAPome - accessed 12/6/2016; last updated 01/30/2015
wget "ftp://ftp.thegpm.org/fasta/crap/crap.fasta" -P ~/create_compil/scripts/data -nv -a download.log 
