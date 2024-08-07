from pylatex import Section, NoEscape

def add_conclusion(doc):
    with doc.create(Section('Conclusion')):
        with open('sections/conclusion.tex', 'r') as file:
            conclusion_content = file.read()
        doc.append(NoEscape(conclusion_content))