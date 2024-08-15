from pylatex import Section, NoEscape, Subsection, NewPage, Subsubsection

def add_methodology(doc):
    with doc.create(Section('Methodology')):    
        with doc.create(Subsection('Empirical Strategy')):
            with doc.create(Subsubsection('The Gravity Model of Trade')):
                with open('sections/methodology_gravity.tex', 'r') as file:
                    gravity_content = file.read()
            doc.append(NoEscape(gravity_content))

            with doc.create(Subsubsection('Benchmark Model')):
                with open('sections/methodology_benchmark.tex', 'r') as file:
                    benchmark_content = file.read()
            doc.append(NoEscape(benchmark_content))

            with doc.create(Subsubsection('PTA Heterogeneity Model')):
                with open('sections/methodology_het.tex', 'r') as file:
                    het_content = file.read()
            doc.append(NoEscape(het_content))

            with doc.create(Subsubsection('North-North, North-South and South-South PTAs')):
                with open('sections/methodology_ns.tex', 'r') as file:
                    ns_content = file.read()
            doc.append(NoEscape(ns_content))

        with doc.create(Subsection('Export Product Unit Value')):
            with open('sections/methodology_epuv.tex', 'r') as file:
                epuv_content = file.read()
        doc.append(NoEscape(epuv_content))

        with doc.create(Subsection('Defining North and South')):
            with open('sections/methodology_south.tex', 'r') as file:
                south_content = file.read()
        doc.append(NoEscape(south_content))

        with doc.create(Subsection('Data')):
            with open('sections/methodology_data.tex', 'r') as file:
                data_content = file.read()
        doc.append(NoEscape(data_content))

        # with doc.create(Section('Methodology')):
            # with open('sections/methodology.tex', 'r') as file:
        #       methodology_content = file.read()
        # doc.append(NoEscape(methodology_content))