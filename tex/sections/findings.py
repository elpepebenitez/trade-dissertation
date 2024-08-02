# This function will be called from your main.py file
from pylatex import Subsection, NoEscape, NewPage, Subsubsection

def add_findings(doc):
    with doc.create(Subsection('Benchmark Estimation Results')):
        with doc.create(Subsubsection('Benchmark Long and Short Models Results')):
            doc.append(NoEscape(r'\input{tables/benchmark_table.tex}'))

    with doc.create(Subsection('NS and SS Post Model Estimation Results')):
        with doc.create(Subsubsection('NS and SS Post Model Results')):
            doc.append(NoEscape(r'\input{tables/ns_ss_post_table.tex}'))
    
        doc.append(NewPage())
        with doc.create(Subsubsection('Additional Findings')):
            doc.append('Here you can include additional findings and discussions.')
