# Makefile for dissertation project

# Define directories
DOC_DIR = ./tex/sections/docs
TEX_DIR = ./tex/sections
PY_DIR = ./tex

# Define Word documents and corresponding LaTeX files
DOCS = introduction literature_review methodology findings analysis_and_discussion conclusion
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

# Rule to convert .docx files to .tex using pandoc
$(TEX_DIR)/%.tex: $(DOC_DIR)/%.docx
	pandoc $< -o $@

# Compile the PyLaTeX document
compile_tex:
	python $(MAIN_PY)

# Clean up auxiliary files
clean:
	rm -f $(TEX_DIR)/*.aux $(TEX_DIR)/*.bbl $(TEX_DIR)/*.bcf $(TEX_DIR)/*.blg $(TEX_DIR)/*.log $(TEX_DIR)/*.out $(TEX_DIR)/*.run.xml $(TEX_DIR)/*.toc $(TEX_DIR)/*.lof $(TEX_DIR)/*.lot
	rm -f $(PY_DIR)/$(MAIN_TEX) $(PY_DIR)/$(basename $(MAIN_TEX)).pdf

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
