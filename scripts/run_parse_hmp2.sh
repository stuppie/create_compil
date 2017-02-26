#!/usr/bin/env bash
[[ -e run_parse_hmp2.sh ]] || { echo >&2 "Please cd into the root folder before running this script."; exit 1; }

set -e
shopt -s nullglob
HMP2_DATA=/home/gstupp/projects/create_compil/data/hmp2/v2
OUT_DIR=/home/gstupp/projects/create_compil/processed/


function finish {
    kill $PARALLEL_PID
}
trap finish EXIT


function hmp2 {
    for GFF_BZ in $HMP2_DATA/*.gff3.bz2; do
      echo "./parse_hmp2.sh $GFF_BZ" >> jobqueue
    done
}

[ -f jobqueue ] && rm jobqueue
echo >jobqueue; tail -f jobqueue | parallel &
PARALLEL_PID=$!

hmp2
wc -l jobqueue

wait
