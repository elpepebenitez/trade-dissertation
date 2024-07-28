from pylatex import NoEscape

def add_list_of_figures(doc):
    doc.append(NoEscape(r'%TC:ignore'))
    doc.append(NoEscape(r'\listoffigures'))
    doc.append(NoEscape(r'%TC:endignore'))