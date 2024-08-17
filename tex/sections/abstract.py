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
    doc.append("Extensions to the Gravity Model of Trade are used to empirically estimate across regions the heterogeneous partial effects of Trade Agreements (TAs) signed between 2000 and 2010 on trade volumes and value per unit of manufacturing products exported, as well as the effects on North-North, North-South and South-South bilateral trade relationships. We find that the average “total” partial effects of TAs in the period studied are similar to the estimates of the relevant literature, but there are heterogeneous effects of specific agreements within regions both on trade volume and value per unit. We also find heterogeneous effects of TAs on the different categories of bilateral trade relationships. We found examples of TAs having both positive and negative effects on both North-South and South-South trade.")
    doc.append(NoEscape(r'\end{minipage}'))
    doc.append(NoEscape(r'\end{center}'))
    doc.append(NoEscape(r'\vspace*{\fill}'))  # Add flexible vertical space after the abstract
    doc.append(NoEscape(r'%TC:endignore'))