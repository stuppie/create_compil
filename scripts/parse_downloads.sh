#!/usr/bin/env bash
[[ -e parse_downloads.sh ]] || { echo >&2 "Please cd into the root folder before running this script."; exit 1; }

set -e
shopt -s nullglob
source params.sh
CWD=`pwd`
cd "$(dirname "$0")"

mkdir -p $PROCESSED_DATA


# hmgi srs
for FILE in $HMGI_DATA/*.gff3.bz2; do
  echo $FILE
  FN=$(basename "${FILE}")
  FN="${FN%.gff3.bz2}.fasta"
  OUT=$PROCESSED_DATA/$FN
  bzcat $FILE | python3 parse_hmgi_srs.py > $OUT
done

# hmgi ref
python3 parse_hmgi.py $HMGI_DATA $PROCESSED_DATA

# metahit
echo metahit
python3 parse_metahit.py $METAHIT_DATA $PROCESSED_DATA

# refseq
for FILE in $REFSEQ_DATA/*.gpff.gz; do
  echo $FILE
  FN=$(basename "${FILE}")
  FN="${FN%.gpff.gz}.fasta"
  OUT=$PROCESSED_DATA/$FN
  python3 parse_refseq.py $FILE $OUT
done

# crapome
python3 parse_crapome.py $CRAPOME_DATA $PROCESSED_DATA

# uniprot
for FILE in $UNIPROT_DATA/*.dat.gz; do
  echo $FILE
  FN=$(basename "${FILE}")
  FN="${FN%.dat.gz}.fasta"
  OUT=$ROOT/processed/$FN
  python3 parse_uniprot.py $FILE $OUT
done


