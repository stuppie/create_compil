#!/usr/bin/env bash
[[ -e parse_downloads.sh ]] || { echo >&2 "Please cd into the root folder before running this script."; exit 1; }

set -e
shopt -s nullglob
source params.sh

function finish {
    kill $PARALLEL_PID
}
trap finish EXIT


function refseq {
    for FILE in $REFSEQ_DATA/*.gpff.gz; do
        echo $FILE
        FN=$(basename "${FILE}")
        FN="${FN%.gpff.gz}.fasta"
        echo "python3 parse_refseq.py $FILE > $PROCESSED_DATA/$FN" >> jobqueue
    done
}

function uniprot {
    for FILE in $UNIPROT_DATA/*.dat.gz; do
      echo $FILE
      FN=$(basename "${FILE}")
      FN="${FN%.dat.gz}.fasta"
      echo "python3 parse_uniprot.py $FILE > $PROCESSED_DATA/$FN" >> jobqueue
    done
}

function hmgi_srs {
    for FILE in $HMGI_DATA/*.gff3.bz2; do
        echo $FILE
        FN=$(basename "${FILE}")
        FN="${FN%.gff3.bz2}.fasta"
        OUT=$PROCESSED_DATA/$FN
        echo $OUT
        echo "bzcat $FILE | python3 parse_hmgi_srs.py > $OUT" >> jobqueue
    done
}

function food {
    for FILE in $FOOD_DATA/*.fasta.gz; do
        echo $FILE
        python parse_food.py $FILE >> $PROCESSED_DATA/food.fasta
    done
}

function hmgi_ref {
    python3 parse_hmgi.py $HMGI_DATA > $PROCESSED_DATA/hmp_ref_GI.fasta
}

function metahit {
    zcat $METAHIT_DATA/frequent_microbe_proteins.fasta.gz | python3 parse_metahit.py  > $PROCESSED_DATA/metahit.fasta
}

function crapome {
    python3 parse_crapome.py $CRAPOME_DATA $PROCESSED_DATA
}

function mouse_gut_microbiome {
    python3 parse_mgm.py $MGM_DATA > $PROCESSED_DATA/mgm.fasta
}


[ -f jobqueue ] && rm jobqueue
true >jobqueue; tail -n+0 -f jobqueue | parallel -j16 &
PARALLEL_PID=$!

mkdir -p $PROCESSED_DATA


refseq
uniprot
hmgi_srs
food
hmgi_ref
metahit
crapome
mouse_gut_microbiome


wait