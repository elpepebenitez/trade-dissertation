from pylatex import Section

def add_abstract(doc):
    with doc.create(Section('Abstract', numbering=False)):
        doc.append('This is the abstract of the dissertation. It provides a brief overview of the research, methodology, findings, and conclusions.')
