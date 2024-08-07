from pylatex import Section, NoEscape

def add_analysis_and_discussion(doc):
    with doc.create(Section('Analysis and Discussion')):
        with open('sections/analysis_and_discussion.tex', 'r') as file:
            analysis_and_discussion_content = file.read()
        doc.append(NoEscape(analysis_and_discussion_content))