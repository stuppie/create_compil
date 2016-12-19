#!/usr/bin/env bash
set -e
source "params.sh"

#UniProt - accessed 11/30/2016; last updated 11/30/2016
wget "ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/taxonomic_divisions/uniprot_*.dat.gz" -P $UNIPROT_DATA -nv -a download.log

#MetaHit-Qin, et al 2010 - accessed 12/5/2016; last updated 06/2009
#wget "http://www.bork.embl.de/~arumugam/Qin_et_al_2010/BGI_GeneSet20090523.fa.gz" -P $METAHIT_DATA -nv -a download.log
wget "http://www.bork.embl.de/~arumugam/Qin_et_al_2010/BGI_GeneSet20090523_annotation.gz" -P $METAHIT_DATA -nv -a download.log
wget "http://www.bork.embl.de/~arumugam/Qin_et_al_2010/BGI_GeneSet20090523_taxonomic.gz" -P $METAHIT_DATA -nv -a download.log
wget "http://www.bork.embl.de/~arumugam/Qin_et_al_2010/frequent_microbe_proteins.fasta.gz" -P $METAHIT_DATA -nv -a download.log

#RefSeq - accessed 12/5/2016; last updated 11/3/2016
wget "ftp://ftp.ncbi.nlm.nih.gov/refseq/release/bacteria/bacteria.nonredundant*.protein.gpff.gz" -P $REFSEQ_DATA -nv -a download.log
wget "ftp://ftp.ncbi.nlm.nih.gov/refseq/release/archaea/archaea.nonredundant*.protein.gpff.gz" -P $REFSEQ_DATA -nv -a download.log
wget "ftp://ftp.ncbi.nlm.nih.gov/refseq/release/fungi/fungi.*.protein.gpff.gz" -P $REFSEQ_DATA -nv -a download.log
wget "ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.*.protein.gpff.gz" -P $REFSEQ_DATA -nv -a download.log

#HMGI Stool - accessed 12/5/2016; last updated 2011
wget "ftp://public-ftp.hmpdacc.org/HMGI/stool/*.with_fasta.gff3.bz2" -P $HMGI_DATA -nv -a downoad.log

#HMGI ref
wget "http://downloads.hmpdacc.org/data/reference_genomes/body_sites/Gastrointestinal_tract.pep.fsa" -P $HMGI_DATA -nv -a downoad.log

#cRAPome - accessed 12/6/2016; last updated 01/30/2015
wget "ftp://ftp.thegpm.org/fasta/crap/crap.fasta" -P $CRAPOME_DATA -nv -a download.log

# food
#    mouse          rat           wheat          barley        rice         maize         Pig          Cow           Chicken
ids=("UP000000589" "UP000002494" "UP000019116" "UP000011116" "UP000059680" "UP000007305" "UP000008227" "UP000009136" "UP000000539")
taxids=(10090       10116         4565          112509        39947         4577          9823          9913          9031)
for i in ${!ids[*]}; do
  echo ${ids[i]}
  wget "http://www.uniprot.org/uniprot/?query=proteome:${ids[i]}&compress=yes&force=true&format=fasta" -nv -a downoad.log -O $FOOD_DATA/${taxids[i]}.fasta.gz
done

#peptide calibration
echo "P00000|Pierce Peptide Retention Time Calibration Mixture|calibration||
SSAAPPPPPRGISNEGQNASIKHVLTSIGEKDIPVPKPKIGDYAGIKTASEFDSAIAQDKSAAGAFGPELSRELGQSGVDTYLQTKGLILVGGYGTR
GILFVGSGVSGGEEGARSFANQPLEVVYSKLTILEELRNGFILDGFPRELASGLSFPVGFKLSSEAPALFQFDLK" > $PROCESSED_DATA/peptide_calibration.fasta

# Mouse Gut Metagenome Xiao 2015
wget "ftp://climb.genomics.cn/pub/10.5524/100001_101000/100114/Genecatalog/184sample_2.6M.GeneSet.pep.gz" -P $MGM_DATA -nv -a downoad.log
# taxonomy
wget "ftp://climb.genomics.cn/pub/10.5524/100001_101000/100114/Annotation/184sample.uniq_gene.NR.anno.merge.gz" -P $MGM_DATA -nv -a downoad.log
wget "ftp://climb.genomics.cn/pub/10.5524/100001_101000/100114/MGS/MmCAG2geneID.txt.gz" -P $MGM_DATA -nv -a downoad.log