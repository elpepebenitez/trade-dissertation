from pylatex import Section, Command, NoEscape

def add_title(doc):
    doc.preamble.append(NoEscape(r'%TC:ignore'))
    doc.preamble.append(Command('title', "Master's Dissertation"))
    doc.preamble.append(Command('author', 'Your Name'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))
    doc.preamble.append(NoEscape(r'%TC:endignore'))