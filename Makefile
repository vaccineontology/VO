# Vaccine Ontology (VO) Makefile
# Jie Zheng
#
# This Makefile is used to build artifacts for the Vaccine Ontology.
#

### Configuration
#
# prologue:
# <http://clarkgrubb.com/makefile-style-guide#toc2>

MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := all
.DELETE_ON_ERROR:
.SUFFIXES:

### Definitions

SHELL := /bin/bash
OBO   := http://purl.obolibrary.org/obo
VO    := $(OBO)/VO_
TODAY := $(shell date +%Y-%m-%d)

### Directories
#
# This is a temporary place to put things.
build:
	mkdir -p $@


### ROBOT
#
# We use the latest official release version of ROBOT
build/robot.jar: | build
	curl -L -o $@ "https://github.com/ontodev/robot/releases/latest/download/robot.jar"

ROBOT := java -jar build/robot.jar

### Imports
#
# Use Ontofox to import various modules.
build/%_import.owl: src/Ontofox_input/%_import_input.txt | build/robot.jar build
	curl -s -F file=@$< -o $@ https://ontofox.hegroup.org/service.php

# Use ROBOT to remove external java axioms
src/imports/%_import.owl: build/%_import.owl
	$(ROBOT) remove --input build/$*_import.owl \
	--base-iri 'http://purl.obolibrary.org/obo/$*_' \
	--axioms external \
	--preserve-structure false \
	--trim false \
	--output $@ 

IMPORT_FILES := $(wildcard src/imports/*_import.owl)

.PHONY: imports
imports: $(IMPORT_FILES)

### Templates
#
src/modules/%.owl: src/templates/%.csv | build/robot.jar
	echo '' > $@
	$(ROBOT) merge \
	--input src/VO.owl \
	template \
	--template $< \
	--prefix "VO: http://purl.obolibrary.org/obo/VO_" \
	--ontology-iri "http://purl.obolibrary.org/obo/vo/dev/$(notdir $@)" \
	--output $@

# Update all modules
MODULE_NAMES := cancer_vaccine\
 vaccine\
 vaccine_adjuvant\
 vaccine_component\
 data_item\
 process\
 site\
 gene\
 protein\
 other\
 individuals\
 vo_annotationProp\
 vo_objectProp\
 obsolete

MODULE_FILES := $(foreach x,$(MODULE_NAMES),src/modules/$(x).owl)

.PHONY: modules
modules: $(MODULE_FILES)

### Build
#
# Here we create a standalone OWL file appropriate for release.
# This involves merging, reasoning, annotating,
# and removing any remaining import declarations.

build/vo-merged.owl: src/VO.owl | build/robot.jar build
	$(ROBOT) merge \
	--input $< \
	annotate \
	--ontology-iri "$(OBO)/vo/vo-merged.owl" \
	--version-iri "$(OBO)/vo/$(TODAY)/vo-merged.owl" \
	--annotation owl:versionInfo "$(TODAY)" \
	--output build/vo-merged.tmp.owl
	sed '/<owl:imports/d' build/vo-merged.tmp.owl > $@
	rm build/vo-merged.tmp.owl

vo.owl: build/vo-merged.owl
	$(ROBOT) reason \
	--input $< \
	--reasoner ELK \
	annotate \
	--ontology-iri "$(OBO)/vo.owl" \
	--version-iri "$(OBO)/vo/$(TODAY)/vo.owl" \
	--annotation owl:versionInfo "$(TODAY)" \
	--output $@

robot_report.tsv: build/vo-merged.owl
	$(ROBOT) report \
	--input $< \
        --fail-on none \
	--output $@

### 
#
# Full build
.PHONY: all
all: vo.owl robot_report.tsv

# Remove generated files
.PHONY: clean
clean:
	rm -rf build



