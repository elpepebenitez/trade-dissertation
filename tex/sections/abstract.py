from pylatex import NoEscape

def add_abstract(doc):
    doc.append(NoEscape(r'%TC:ignore'))
    doc.packages.append(NoEscape(r'\usepackage{ragged2e}'))
    doc.append(NoEscape(r'\vspace*{\fill}'))  # Add flexible vertical space before the abstract
    doc.append(NoEscape(r'\begin{center}'))
    doc.append(NoEscape(r'\begin{minipage}{0.8\textwidth}'))  # Adjust the width as needed
    doc.append(NoEscape(r'\begin{center}'))
    doc.append(NoEscape(r'\section*{Abstract}'))
    doc.append(NoEscape(r'\end{center}'))
    doc.append(NoEscape(r'\justify'))
    doc.append("This is the abstract text. It should be centered on the page, and the text should be justified. " * 5)
    doc.append(NoEscape(r'\end{minipage}'))
    doc.append(NoEscape(r'\end{center}'))
    doc.append(NoEscape(r'\vspace*{\fill}'))  # Add flexible vertical space after the abstract
    doc.append(NoEscape(r'%TC:endignore'))