from pylatex import Section, NoEscape

def add_methodology(doc):
    with doc.create(Section('Methodology')):
        with open('sections/methodology.tex', 'r') as file:
            methodology_content = file.read()
        doc.append(NoEscape(methodology_content))