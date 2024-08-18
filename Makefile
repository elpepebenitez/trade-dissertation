# Makefile for dissertation project

# Define directories
DOC_DIR = ./tex/sections/docs/
TEX_DIR = ./tex/sections/
PY_DIR = ./tex
BIB_FILE = $(PY_DIR)/references.bib

# Define Word documents and corresponding LaTeX files
# All docs:
# DOCS = introduction research_introduction compad_literature_review scale_literature_review empirical_literature_review exports_literature_review methodology_benchmark methodology_data methodology_epuv methodology_gravity methodology_het methodology_ns methodology_south findings_benchmark findings_het findings_nsb findings_nsh findings_epuv determinants_analysis limitations_analysis conclusion
# DOCS = introduction literature_review methodology_benchmark methodology_data methodology_epuv methodology_gravity methodology_het methodology_ns methodology_south findings analysis_and_discussion conclusion
# DOCS = findings_benchmark findings_het findings_nsb findings_nsh findings_epuv
# DOCS = compad_literature_review scale_literature_review empirical_literature_review exports_literature_review
# DOCS = introduction analysis_and_discussion conclusion
# DOCS = empirical_literature_review
# DOCS = determinants_analysis limitations_analysis


TEX_FILES = $(patsubst %, $(TEX_DIR)/%.tex, $(DOCS))

# Define the main LaTeX file name
MAIN_TEX = 23802_DV410_2024.tex

# Define the main Python script
MAIN_PY = $(PY_DIR)/main.py

# Phony targets
.PHONY: all data figures tables convert_tex compile_tex clean

# Default target
all: data figures tables convert_tex compile_tex

# Run data analysis scripts
data:
	python scripts/analysis.py

# Generate figures
figures:
	python scripts/generate_figures.py

# Generate tables
tables:
	python scripts/generate_tables.py

# Convert Word documents to LaTeX files
convert_tex: $(TEX_FILES)

# Rule to convert .docx files to .tex using pandoc with citation processing
$(TEX_DIR)/%.tex: $(DOC_DIR)/%.docx $(BIB_FILE)
	pandoc --bibliography=$(BIB_FILE) --citeproc $< -o $@

# Compile the PyLaTeX document
compile_tex:
	python $(MAIN_PY)

# Clean up auxiliary files
clean:
	rm -f $(TEX_DIR)/*.aux $(TEX_DIR)/*.bbl $(TEX_DIR)/*.bcf $(TEX_DIR)/*.blg $(TEX_DIR)/*.log $(TEX_DIR)/*.out $(TEX_DIR)/*.run.xml $(TEX_DIR)/*.toc $(TEX_DIR)/*.lof $(TEX_DIR)/*.lot
	rm -f $(PY_DIR)/$(MAIN_TEX) $(PY_DIR)/$(basename $(MAIN_TEX)).pdf
	rm -f $(TEX_FILES)

# # Makefile for dissertation project

# # Phony targets
# .PHONY: all data figures tables tex clean

# # Default target
# all: data figures tables tex

# # Run data analysis scripts
# data:
# 	python scripts/analysis.py

# # Generate figures
# figures:
# 	python scripts/generate_figures.py

# # Generate tables
# tables:
# 	python scripts/generate_tables.py

# # Compile the PyLaTeX document
# tex: 
# 	python tex/main.py

# # Clean up auxiliary files
# clean:
# 	rm -f tex/*.aux tex/*.bbl tex/*.bcf tex/*.blg tex/*.log tex/*.out tex/*.run.xml tex/*.toc tex/*.lof tex/*.lot
# 	rm -f tex/dissertation.pdf
