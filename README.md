#extract coordinates into the gene limits (+- 5000 pb from TSS and TTS, respectively) from the methylation bed files.

## command : case of CG context with the 1000 most highly (top1000) expressed genes 
perl extractMetFromBed_CG.pl TOP_1000_genes subjectsall.csv CG



###  -1///  gene body commands:
---------------------------------

## normalization with respect to gene length: define bins of 500pb and calculate the average methylation in each bin.

#---example 1 : CG context, top1000 genes, antisense strand.
python normalizeGeneParallelProcess_sm.py TOP_strandminus_genes 500 CG top_1000_CG_TEST_sm.tsv subjectsall.csv

#---example 2 : CG context, top1000 genes, sense strand.
python normalizeGeneParallelProcess_sp.py TOP_strandplus_genes 500 CG top_1000_CG_TEST_sp.tsv subjectsall.csv


## merging the methylation in each bin by subject for the top1000 and bot1000 expressed genes

#---example 1 : CG context, top1000 genes
for i in `cut -f 1 subjectsall.csv`; do python merge_met_by_subject.py TOP_1000_genes $i CG > csv/CG/gene/s${i}.CG.top1000.csv ; done

#---example 2 : CG context, bot1000 genes
for i in `cut -f 1 subjectsall.csv` ; do python merge_met_by_subject.py BOT_1000_genes $i CG > csv/CG/gene/s${i}.CG.bot1000.csv ; done



### -2///  5' and 3' gene sides (-5000 pb from TSS to TSS site and TTS site to +5000pb from TTS, respectively) commands:
------------------------------------------------------------------------------------------------------------------------

## normalization with respect to the length: define bins of 100pb and calculate the average methylation in each bin.


#---example : 3' gene side, CG context, top1000 genes and sense / antisense strand
python normalizeFlanking3RegParallelProcess_sm.py TOP_strandminus_genes 100 CG top_1000_CG_TEST_3_sm.tsv subjectsall.csv

python normalizeFlanking3RegParallelProcess_sp.py TOP_strandplus_genes 100 CG top_1000_CG_TEST_3_sp.tsv subjectsall.csv


#---example : 5' gene side, CG context, top1000 genes and sense / antisense strand
python normalizeFlankingRegParallelProcess_sm.py TOP_strandminus_genes 100 CG top_1000_CG_TEST_5_sm.tsv subjectsall.csv

python normalizeFlankingRegParallelProcess_sp.py TOP_strandplus_genes 100 CG top_1000_CG_TEST_5_sp.tsv subjectsall.csv



## merging the methylation in each bin by subject for the top1000 and bot1000 expressed genes

#---example 1: 3' gene side, CG context, top1000 expressed genes
for i in `cut -f 1 subjectsall.csv` ; do python met_3fl_met_by_subject.py TOP_1000_genes $i CG > csv/CG/3f/s${i}.3.CG.top1000.csv ; done


#---example 2: 5' gene side, CG context, top1000 expressed genes
for i in `cut -f 1 subjectsall.csv` ; do python met_5fl_met_by_subject.py TOP_1000_genes $i CG > csv/CG/5f/s${i}.5.CG.top1000.csv ; done
