from pylatex import Section, Subsection, NoEscape, NewPage, Subsubsection, Command, Figure

def add_appendix(doc):
    doc.append(NoEscape(r'%TC:ignore'))   
    with doc.create(Section('Appendix')):
        with doc.create(Subsection('Appendix I - Sample Countries')):
            # doc.append('Content in the appendix should not be counted in the word count.')
            # Insert the PDF for Appendix I
            # with doc.create(Figure(position='h!')) as countries_figure:
            #     countries_figure.add_image('figures/countries.jpg', width=NoEscape(r'1.0\textwidth'))
            #     # countries_figure.add_caption('TA Heterogeneity Across Regions')
            # doc.append(Command('FloatBarrier'))
            doc.append(Command('includepdf', options=NoEscape('pages=-, fitpaper=true'), arguments=NoEscape('tables/countries.pdf')))
            # doc.append(NoEscape(r'\includepdf[pages=-, offset=0 -1cm, frame]{DV410_Dissertation Cover Sheet_ Consent Form_Front Page_2023-24.pdf}'))
        
        with doc.create(Subsection('Appendix II - Sample TAs')):
            # with doc.create(Figure(position='h!')) as ptas_figure:
            #     ptas_figure.add_image('figures/pta_list.jpg', width=NoEscape(r'0.8\textwidth'))
            #     # countries_figure.add_caption('TA Heterogeneity Across Regions')
            # doc.append(Command('FloatBarrier'))
            # doc.append('Content in the appendix should not be counted in the word count.')
            # Insert the PDF for Appendix II
            doc.append(Command('includepdf', options=NoEscape('pages=-, fitpaper=true'), arguments=NoEscape('tables/pta_list.pdf')))
            # doc.append(NoEscape(r'\includepdf[pages=-, offset=0 -1cm, frame]{DV410_Dissertation Cover Sheet_ Consent Form_Front Page_2023-24.pdf}'))
        
        with doc.create(Subsection('Appendix III - Regression Tables by Region for TA Heterogeneity Model')):
            # doc.append('Content in the appendix should not be counted in the word count.')
            doc.append(Command('FloatBarrier'))
            doc.append(NoEscape(r'\input{tables/benchmark_Africa_pta_table.tex}'))
            doc.append(Command('FloatBarrier'))
            doc.append(NoEscape(r'\input{tables/benchmark_Americas_pta_table.tex}'))
            doc.append(Command('FloatBarrier'))
            doc.append(NoEscape(r'\input{tables/benchmark_Asia_pta_table.tex}'))
            doc.append(Command('FloatBarrier'))
            doc.append(NoEscape(r'\input{tables/benchmark_Europe_pta_table.tex}'))
            doc.append(Command('FloatBarrier'))
            doc.append(NoEscape(r'\input{tables/benchmark_Intercontinental_pta_table.tex}'))
            doc.append(Command('FloatBarrier'))

        with doc.create(Subsection('Appendix IV - Regression Tables by Region for TA Heterogeneity Extended Model')):
            doc.append(Command('FloatBarrier'))
            doc.append(NoEscape(r'\input{tables/ns_pta_Africa.tex}'))
            doc.append(Command('FloatBarrier'))
            doc.append(NoEscape(r'\input{tables/ns_pta_Americas.tex}'))
            doc.append(Command('FloatBarrier'))
            doc.append(NoEscape(r'\input{tables/ns_pta_Asia.tex}'))
            doc.append(Command('FloatBarrier'))
            doc.append(NoEscape(r'\input{tables/ns_pta_Europe.tex}'))
            doc.append(Command('FloatBarrier'))
            doc.append(NoEscape(r'\input{tables/ns_pta_Intercontinental.tex}'))
            doc.append(Command('FloatBarrier'))
    doc.append(NoEscape(r'%TC:endignore'))