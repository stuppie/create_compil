#!/usr/bin/env bash
set -e

HMP2_DATA=/home/gstupp/projects/create_compil/data/hmp2/v2

#for GFF_BZ in $HMP2_DATA/*.gff3.bz2; do
GFF_BZ=$1
echo $GFF_BZ
GFF=${GFF_BZ%.bz2}
FASTA_BZ=${GFF_BZ%.gff3.bz2}.fna.bz2
FASTA=${FASTA_BZ%.bz2}
bunzip2 -k $GFF_BZ &
bunzip2 -k $FASTA_BZ &
wait

# make bed file using only polypeptide
BED=${GFF%.gff3}.bed
/home/gstupp/bin/bedops/gff2bed < $GFF | grep -w polypeptide > $BED

# extract pp sequences from fasta
FASTA_PP=${GFF_BZ%.gff3.bz2}.pp.fna
bedtools getfasta -s -fullHeader -fi $FASTA -bed $BED -fo $FASTA_PP

# translate fasta
PP_FA=${FASTA_PP%.fna}.fa
cat $FASTA_PP | python3 fasta_translate.py > $PP_FA
#cat $FASTA_PP | parallel -j+4 --block 5M --recstart '\n>' --regexp --pipe python3 fasta_translate.py > $PP_FA

# grab column 10 (metadata) from the bed file, add to fasta defline
# then make compil version of defline
FASTA_RENAME=${PP_FA%.pp.fa}.fa.gz
python3 name_fasta_from_bed.py $BED $PP_FA | python3 hmp2_defline.py | gzip > $FASTA_RENAME

rm $GFF $FASTA
rm $BED $FASTA_PP $PP_FA
rm ${FASTA}.fai

#done

# start codon usage
# zcat SRS011061_pp.fa.gz | grep '^>' -A1 | grep -v '>' | grep -o '^.' | sort | uniq -c

# may want to filter by starting with M, L, or V
# https://en.wikipedia.org/wiki/Start_codon