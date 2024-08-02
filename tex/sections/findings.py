# This function will be called from your main.py file
from pylatex import Subsection, NoEscape, NewPage, Subsubsection

def add_findings(doc):
    with doc.create(Subsection('Estimation Results')):
        doc.append(NoEscape(r'\input{tables/benchmark_results_table.tex}'))



def add_findings(doc):
    with doc.create(Subsection('Estimation Results')):
        with doc.create(Subsubsection('NS and SS Post Model Results')):
            doc.append(NoEscape(r'\input{tables/ns_ss_post_table.tex}'))
    
        doc.append(NewPage())
        with doc.create(Subsubsection('Additional Findings')):
            doc.append('Here you can include additional findings and discussions.')
