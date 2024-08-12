from pylatex import Section, NoEscape

def add_introduction(doc):
    with doc.create(Section('Introduction')):
        with open('sections/introduction.tex', 'r') as file:
            introduction_content = file.read()
        doc.append(NoEscape(introduction_content))
        doc.append('This is the introduction section. Here is a citation: ')
        doc.append(NoEscape(r'\cite{dahi_preferential_2013}'))