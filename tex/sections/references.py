from pylatex import Section, NoEscape

def add_references(doc):
    doc.append(NoEscape(r'%TC:ignore'))
    with doc.create(Section('References')):
        doc.append(NoEscape(r'\printbibliography'))
    doc.append(NoEscape(r'%TC:endignore'))
