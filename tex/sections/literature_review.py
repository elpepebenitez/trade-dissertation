from pylatex import Section, NoEscape, Subsection, NewPage, Subsubsection

def add_literature_review(doc):
    with doc.create(Section('Literature Review')):
        doc.append('This section reviews the literature on the theoretical and empirical potential effects of PTAs on exports and welfare and situates the analysis in the relevant field of research.')
        with doc.create(Subsection('Theoretical Framework')):
            doc.append('Stumbling block vs building block dichotomy.')
            with doc.create(Subsubsection('Comparative Advantage and Trade Creation and Diversion')):
                with open('sections/compad_literature_review.tex', 'r') as file:
                    compad_litreview_content = file.read()
            doc.append(NoEscape(compad_litreview_content))

            with doc.create(Subsubsection('Economies of Scale, Input-Output linkages and Products Exported')):
                with open('sections/scale_literature_review.tex', 'r') as file:
                    scale_litreview_content = file.read()
            doc.append(NoEscape(scale_litreview_content))

            # with doc.create(Subsubsection('')):
            #     with open('sections/literature_review.tex', 'r') as file:
            #         _litreview_content = file.read()
            # doc.append(NoEscape(_litreview_content))
        
        with doc.create(Subsection('Empirical Evidence')):
            with open('sections/empirical_literature_review.tex', 'r') as file:
                empirical_litreview_content = file.read()
        doc.append(NoEscape(empirical_litreview_content))

        with doc.create(Subsection('Significance of Exports')):
            with open('sections/exports_literature_review.tex', 'r') as file:
                exports_litreview_content = file.read()
        doc.append(NoEscape(exports_litreview_content))
        
        # with open('sections/literature_review.tex', 'r') as file:
        #             literature_review_content = file.read()
        #     doc.append(NoEscape(literature_review_content))