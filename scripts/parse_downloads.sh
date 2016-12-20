#!/usr/bin/env bash
[[ -e parse_downloads.sh ]] || { echo >&2 "Please cd into the root folder before running this script."; exit 1; }

set -e
shopt -s nullglob
source params.sh

mkdir -p $PROCESSED_DATA

# food
rm $PROCESSED_DATA/food.fasta
for FILE in $FOOD_DATA/*.fasta.gz; do
  echo $FILE
  python parse_food.py $FILE >> $PROCESSED_DATA/food.fasta
done

# hmgi srs
for FILE in $HMGI_DATA/*.gff3.bz2; do
  echo $FILE
  FN=$(basename "${FILE}")
  FN="${FN%.gff3.bz2}.fasta"
  OUT=$PROCESSED_DATA/$FN
  echo $OUT
  bzcat $FILE | python3 parse_hmgi_srs.py > $OUT
done

# hmgi ref
python3 parse_hmgi.py $HMGI_DATA > $PROCESSED_DATA/hmp_ref_GI.fasta

# metahit
echo metahit
zcat $METAHIT_DATA/frequent_microbe_proteins.fasta.gz | python3 parse_metahit.py  > $PROCESSED_DATA/metahit.fasta

# refseq
for FILE in $REFSEQ_DATA/*.gpff.gz; do
  echo $FILE
  FN=$(basename "${FILE}")
  FN="${FN%.gpff.gz}.fasta"
  python3 parse_refseq.py $FILE > $PROCESSED_DATA/$FN
done

# crapome
python3 parse_crapome.py $CRAPOME_DATA $PROCESSED_DATA

# uniprot
for FILE in $UNIPROT_DATA/*.dat.gz; do
  echo $FILE
  FN=$(basename "${FILE}")
  FN="${FN%.dat.gz}.fasta"
  python3 parse_uniprot.py $FILE > $PROCESSED_DATA/$FN
done

# mouse gut microbiome
python3 parse_mgm.py $MGM_DATA > $PROCESSED_DATA/mgm.fasta