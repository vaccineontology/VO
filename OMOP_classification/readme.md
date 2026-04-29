# Extraction of OMOP subset from VO

## [Extraction of Classification terms](https://github.com/vaccineontology/VO/tree/master/OMOP_classification/classification_terms)

Extract VO terms that have at least one OMOP term as a subclass; these VO terms function as OMOP classification terms.

1. Retrieve OMOP intermediate terms from VO using SPARQL. The query returns VO terms that have at least one OMOP term as a subclass.

   Run following command under VO git repository:

   `robot query --input vo.owl \
     --query SPARQL/get_OMOP_intermediate.rq OMOP_classification/OMOP_intermediate.tsv`

2. Generate OntoFox input file, [OMOP_classification_input.txt](https://github.com/vaccineontology/VO/blob/master/OMOP_classification/classification_terms/OMOP_classification_input.txt), based on OMOP_intermediate.tsv using a text editor.

   a. Edit file OMOP_intermediate.tsv
   
      - remove first line
      - remove "
      - replace tab with ' #'

   b. Copy all terms in OMOP_intermediate.tsv to OMOP_classification_input.txt file, under [Low level source term URIs] section

   c. Add 'http://purl.obolibrary.org/obo/VO_0000001 #vaccine' as [Top level source term URIs and target direct superclass URIs]

3. Retrieve OMOP classification terms from VO using OntoFox

Go to ontoFox site:
https://ontofox.hegroup.org.
Using '[OMOP_classification_input.txt](https://github.com/vaccineontology/VO/blob/master/OMOP_classification/classification_terms/OMOP_classification_input.txt)' as the input file (section 2. Data input using local text file). 
Download the output file, named as: [OMOP_classification.owl](https://raw.githubusercontent.com/vaccineontology/VO/refs/heads/master/OMOP_classification/classification_terms/OMOP_classification.owl).

## [Extraction of Classification terms with OMOP terms](https://github.com/vaccineontology/VO/tree/master/OMOP_classification/classification_terms_with_OMOPterms)

1. Generate OntoFox input file, [VO_OMOP_input.txt](https://github.com/vaccineontology/VO/blob/master/OMOP_classification/classification_terms_with_OMOPterms/VO_OMOP_input.txt) based on two template files, [vo_CVX_code.csv](https://github.com/vaccineontology/VO/blob/master/src/templates/vo_CVX_code.csv) and [vo_RxNorm.csv](https://github.com/vaccineontology/VO/blob/master/src/templates/vo_RxNorm.csv) using a text editor.

   a. Copy the terms including ID and lable in these two template files under [Low level source term URIs] section
   
      - remove first two lines
      - replace 'VO:' with 'http://purl.obolibrary.org/obo/VO_'
      - replace tab with ' #'

   b. Add a few VO terms as [Top level source term URIs and target direct superclass URIs]

        http://purl.obolibrary.org/obo/VO_0000001 #vaccine
        http://purl.obolibrary.org/obo/VO_0000179 #vaccine component
        http://purl.obolibrary.org/obo/PR_000000001 #protein
        http://purl.obolibrary.org/obo/OBI_1110034 #antigen

2. Retrieve OMOP classification terms with OMOP terms from VO using OntoFox

Go to ontoFox site:
https://ontofox.hegroup.org.
Using '[VO_OMOP_input.txt](https://github.com/vaccineontology/VO/blob/master/OMOP_classification/classification_terms_with_OMOPterms/VO_OMOP_input.txt)' as the input file (section 2. Data input using local text file).
Download the output file, named as: [VO_OMOP.owl](https://raw.githubusercontent.com/vaccineontology/VO/refs/heads/master/OMOP_classification/classification_terms_with_OMOPterms/VO_OMOP.owl).
