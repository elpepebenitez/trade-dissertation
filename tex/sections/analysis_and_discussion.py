from pylatex import Section, NoEscape, Subsection, Subsubsection

def add_analysis_and_discussion(doc):
    with doc.create(Section('Analysis and Discussion')):
        doc.append('Our analysis finds evidence of positive, negative and not significant effects of TAs on both South-South and North-South trade relationships, on trade volumes and on the value per unit of manufacturing products exported, relative to trade with non-members. The magnitudes of our findings are similar to the estimates in the empirical literature on the effects of TAs on trade. Our findings on the heterogeneous of effects of TAs appear to indicate that TAs can have positive and negative effects on North-South and South-South bilateral trade relationships, and that declaring them as stumbling or building blocks of industrial development and growth is not straight forward.')
        with doc.create(Subsection('Potential Determinant Mechanisms of Heterogeneous Effects of TAs ')):
            with open('sections/determinants_analysis.tex', 'r') as file:
                determinants_analysis_content = file.read()
            doc.append(NoEscape(determinants_analysis_content))

        with doc.create(Subsection('Limitations')):
            with open('sections/limitations_analysis.tex', 'r') as file:
                limitations_analysis_content = file.read()
            doc.append(NoEscape(limitations_analysis_content))