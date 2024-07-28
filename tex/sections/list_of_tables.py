from pylatex import NoEscape

def add_list_of_tables(doc):
    doc.append(NoEscape(r'%TC:ignore'))
    doc.append(NoEscape(r'\listoftables'))
    doc.append(NoEscape(r'%TC:endignore'))