from pylatex import Section, NoEscape

def add_abbreviations(doc):
    doc.append(NoEscape(r'%TC:ignore'))
    with doc.create(Section('Abbreviations', numbering=False)):
        doc.append(NoEscape(r'\begin{tabbing}'))
        doc.append(NoEscape(r'\hspace{3cm} \= \kill'))  # Set tab stops

        # Add abbreviations here
        abbreviations = [
            ("AI", "Artificial Intelligence"),
            ("API", "Application Programming Interface"),
            ("CPU", "Central Processing Unit"),
            ("GPU", "Graphics Processing Unit"),
            ("IoT", "Internet of Things"),
            ("ML", "Machine Learning"),
            ("NLP", "Natural Language Processing"),
            ("RAM", "Random Access Memory"),
            ("UX", "User Experience"),
            ("UI", "User Interface")
        ]

        # Sort abbreviations alphabetically
        abbreviations.sort(key=lambda x: x[0])

        # Add each abbreviation to the list
        for abbr, full_text in abbreviations:
            doc.append(NoEscape(r'\textbf{' + abbr + r'} \> ' + full_text + r' \\'))

        doc.append(NoEscape(r'\end{tabbing}'))
    doc.append(NoEscape(r'%TC:endignore'))
