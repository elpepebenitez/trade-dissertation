# Makefile for dissertation project

# Phony targets
.PHONY: all data figures tables tex clean

# Default target
all: data figures tables tex

# Run data analysis scripts
data:
	python scripts/analysis.py

# Generate figures
figures:
	python scripts/generate_figures.py

# Generate tables
tables:
	python scripts/generate_tables.py

# Compile the PyLaTeX document
tex: 
	python tex/main.py

# Clean up auxiliary files
clean:
	rm -f tex/*.aux tex/*.bbl tex/*.bcf tex/*.blg tex/*.log tex/*.out tex/*.run.xml tex/*.toc tex/*.lof tex/*.lot
	rm -f tex/dissertation.pdf
