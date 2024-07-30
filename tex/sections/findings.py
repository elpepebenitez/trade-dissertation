from pylatex import Subsection, NoEscape

def add_findings(doc):
    with doc.create(Subsection('Estimation Results')):
        doc.append(NoEscape(r'\input{tables/benchmark_results_table.tex}'))

# This function will be called from your main.py file