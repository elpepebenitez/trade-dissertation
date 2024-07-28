from pylatex import Section, Subsection, NoEscape

def add_appendix(doc):
    doc.append(NoEscape(r'%TC:ignore'))
    with doc.create(Section('Appendix')):
        with doc.create(Subsection('Subsection in Appendix')):
            doc.append('Content in the appendix should not be counted in the word count.')
    doc.append(NoEscape(r'%TC:endignore'))