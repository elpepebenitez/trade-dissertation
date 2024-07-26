from pylatex import NoEscape

def add_references(doc):
    doc.append(NoEscape(r'\printbibliography'))