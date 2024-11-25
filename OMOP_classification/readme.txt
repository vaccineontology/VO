1. Retrieve OMOP intermediate terms from VO using SPARQL

Run following command under VO git repository:

robot query --input vo.owl \
  --query SPARQL/get_OMOP_intermediate.rq OMOP_classification/OMOP_intermediate.tsv


2. Generate OntoFox input file based on OMOP_intermediate.tsv (all terms are 'Low level source terms') using text editor

2a. Edit file OMOP_intermediate.tsv
- remove first line
- remove "
- replace tab by ' #'

2b. Copy all terms in OMOP_intermediate.tsv to OMOP_classification_input.txt file, under [Low level source term URIs] section


3. Retrieve OMOP classification terms from VO using OntoFox

Go to ontoFox site:
https://ontofox.hegroup.org
Using 'OMOP_classification_input.txt' as input file (section 2. Data input using local text file)
Download the output file, named as: 
OMOP_classification.owl