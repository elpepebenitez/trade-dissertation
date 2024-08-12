# This function will be called from your main.py file
from pylatex import Section, Subsection, NoEscape, NewPage, Subsubsection

def add_findings(doc):
    with doc.create(Section('Findings')):
        with open('sections/findings.tex', 'r') as file:
            findings_content = file.read()
        doc.append(NoEscape(findings_content))
    
    with doc.create(Subsection('Benchmark Estimation Results by Region')):
        with doc.create(Subsubsection('Benchmark Model Results by Region')):
            doc.append(NoEscape(r'\input{tables/benchmark_region_table.tex}'))
    
    with doc.create(Subsection('PTA Estimation Results by Region')):
        with doc.create(Subsubsection('PTA Model Results by Region')):
            doc.append(NoEscape(r'\input{tables/benchmark_Africa_pta_table.tex}'))
            doc.append(NoEscape(r'\input{tables/benchmark_Americas_pta_table.tex}'))
            doc.append(NoEscape(r'\input{tables/benchmark_Asia_pta_table.tex}'))
            doc.append(NoEscape(r'\input{tables/benchmark_Europe_pta_table.tex}'))
            doc.append(NoEscape(r'\input{tables/benchmark_Intercontinental_pta_table.tex}'))

    with doc.create(Subsection('NS Estimation Results by Region')):
        with doc.create(Subsubsection('NS Model Results by Region')):
            doc.append(NoEscape(r'\input{tables/benchmark_ns_table.tex}'))
    
    with doc.create(Subsection('NS PTA Estimation Results by Region')):
        with doc.create(Subsubsection('NS PTA Model Results by Region')):
            doc.append(NoEscape(r'\input{tables/ns_pta_Africa.tex}'))
            doc.append(NoEscape(r'\input{tables/ns_pta_Americas.tex}'))
            doc.append(NoEscape(r'\input{tables/ns_pta_Asia.tex}'))
            doc.append(NoEscape(r'\input{tables/ns_pta_Europe.tex}'))
            doc.append(NoEscape(r'\input{tables/ns_pta_Intercontinental.tex}'))

    # with doc.create(Subsection('NS and SS Post Model Estimation Results')):
    #     with doc.create(Subsubsection('NS and SS Post Model Results')):
    #         doc.append(NoEscape(r'\input{tables/ns_ss_post_table.tex}'))
    
        doc.append(NewPage())
        with doc.create(Subsubsection('Additional Findings')):
            doc.append('Here you can include additional findings and discussions.')