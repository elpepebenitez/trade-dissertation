from pylatex import Section, NoEscape

def add_literature_review(doc):
    with doc.create(Section('Literature Review')):
        with open('sections/literature_review.tex', 'r') as file:
            literature_review_content = file.read()
        doc.append(NoEscape(literature_review_content))