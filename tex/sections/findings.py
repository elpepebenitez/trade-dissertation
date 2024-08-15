# This function will be called from your main.py file
from pylatex import Section, Subsection, NoEscape, NewPage, Subsubsection, Command

def add_findings(doc):
    with doc.create(Section('Findings')):
        doc.append('This section presents and describes the results of estimating our gravity models.')
        
        # with open('sections/findings.tex', 'r') as file:
        #     findings_content = file.read()
        # doc.append(NoEscape(findings_content))
    
    with doc.create(Subsection('Benchmark Results')):
        with open('sections/findings_benchmark.tex', 'r') as file:
            benchmark_content = file.read()
        doc.append(NoEscape(benchmark_content))
        doc.append(NoEscape(r'\input{tables/benchmark_region_table.tex}'))
        doc.append(Command('FloatBarrier'))
    
    with doc.create(Subsection('PTA Heterogeneity Results')):
        with open('sections/findings_het.tex', 'r') as file:
            het_content = file.read()
        doc.append(NoEscape(het_content))
        doc.append(NoEscape(r'\input{tables/benchmark_Africa_pta_table.tex}'))
        doc.append(NoEscape(r'\input{tables/benchmark_Americas_pta_table.tex}'))
        doc.append(NoEscape(r'\input{tables/benchmark_Asia_pta_table.tex}'))
        doc.append(NoEscape(r'\input{tables/benchmark_Europe_pta_table.tex}'))
        doc.append(NoEscape(r'\input{tables/benchmark_Intercontinental_pta_table.tex}'))
        doc.append(Command('FloatBarrier'))

    with doc.create(Subsection('North-North, North-South and South-South PTAs')):
        with doc.create(Subsubsection('North-South Benchmark Results')):
            with open('sections/findings_nsb.tex', 'r') as file:
                nsb_content = file.read()
            doc.append(NoEscape(nsb_content))
            doc.append(NoEscape(r'\input{tables/benchmark_ns_table.tex}'))
            doc.append(Command('FloatBarrier'))
        with doc.create(Subsubsection('North-South PTA Heterogeneity Results')):
            with open('sections/findings_nsh.tex', 'r') as file:
                nsh_content = file.read()
            doc.append(NoEscape(nsh_content))
            doc.append(NoEscape(r'\input{tables/ns_pta_Africa.tex}'))
            doc.append(NoEscape(r'\input{tables/ns_pta_Americas.tex}'))
            doc.append(NoEscape(r'\input{tables/ns_pta_Asia.tex}'))
            doc.append(Command('FloatBarrier'))
            doc.append(NoEscape(r'\input{tables/ns_pta_Europe.tex}'))
            doc.append(Command('FloatBarrier'))
            doc.append(NoEscape(r'\input{tables/ns_pta_Intercontinental.tex}'))
            doc.append(Command('FloatBarrier'))
    
    with doc.create(Subsection('Export Product Unit Value Results')):
        with open('sections/findings_epuv.tex', 'r') as file:
            epuv_content = file.read()
        doc.append(NoEscape(epuv_content))
        doc.append(NoEscape(r'\input{tables/84_trade_benchmark_table.tex}'))
        doc.append(NoEscape(r'\input{tables/84_benchmark_table.tex}'))
        doc.append(NoEscape(r'\input{tables/85_trade_benchmark_table.tex}'))
        doc.append(NoEscape(r'\input{tables/85_benchmark_table.tex}'))
        doc.append(NoEscape(r'\input{tables/84_trade_nsb_table.tex}'))
        doc.append(NoEscape(r'\input{tables/84_nsb_table.tex}'))
        doc.append(NoEscape(r'\input{tables/85_trade_nsb_table.tex}'))
        doc.append(NoEscape(r'\input{tables/85_nsb_table.tex}'))
        doc.append(NoEscape(r'\input{tables/84_85_trade_africa.tex}'))
        doc.append(NoEscape(r'\input{tables/epuv_Africa.tex}'))
        doc.append(NoEscape(r'\input{tables/84_85_trade_americas.tex}'))
        doc.append(NoEscape(r'\input{tables/epuv_Americas.tex}'))
        doc.append(Command('FloatBarrier'))
        

    # with doc.create(Subsection('NS and SS Post Model Estimation Results')):
    #     with doc.create(Subsubsection('NS and SS Post Model Results')):
    #         doc.append(NoEscape(r'\input{tables/ns_ss_post_table.tex}'))
    
    # doc.append(NewPage())
    # with doc.create(Subsubsection('Additional Findings')):
    #     doc.append('Here you can include additional findings and discussions.')