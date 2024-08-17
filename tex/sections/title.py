from pylatex import Command, NoEscape

def add_title(doc):
    doc.preamble.append(NoEscape(r'%TC:ignore'))
    doc.preamble.append(Command('title', NoEscape(r'''
        \begin{flushright}
        \large \textbf{Candidate Number: 23802}
        \end{flushright}
        \vspace*{30mm}
        \begin{center}
        \large MSc in Development Management 2023 \\
        \large (Applied Development Economics Specialism) \\
        \vspace*{5mm}
        Dissertation submitted in partial fulfilment of the requirements of the degree. \\
        \vspace*{35mm}
        \large \textbf{Building and Stumbling Blocks: An Empirical Analysis of the Heterogenous Effects of Trade Agreements Between North and South Countries} \\
        \vspace*{20mm}
        \end{center}
    ''')))
    doc.preamble.append(Command('date', ''))  # Explicitly set the date to be empty
    doc.append(NoEscape(r'\maketitle'))
    doc.preamble.append(NoEscape(r'%TC:endignore'))