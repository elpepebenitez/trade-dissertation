from pylatex import Section, NoEscape

def add_abbreviations(doc):
    doc.append(NoEscape(r'%TC:ignore'))
    with doc.create(Section('Abbreviations', numbering=False)):
        doc.append(NoEscape(r'\begin{tabbing}'))
        doc.append(NoEscape(r'\hspace{3cm} \= \kill'))  # Set tab stops

        # Add abbreviations here
        abbreviations = [
            ("TAs", "Trade Agreements"),
            ("NRPTAs", "Non-reciprocal Preferential Trade Agreements"),
            ("PTAs", "Preferential Trade Agreements"),
            ("FTA", "Free Trade Agreements"),
            ("CU", "Customs Union"),
            ("CMs", "Common Markets"),
            ("EUs", "Economic Unions"),
            ("EPUV", "Export Product Unit Value"),
            ("HS", "Harmonysed System"),
            ("DESTA", "The Design of International Trade Agreements Database"),
            ("TradeProd", "The Trade and Production Database"),
            ("COMTRADE", "UN Commodity Trade Statistics Database"),
            ("INDSTAT ", "UNIDO Industrial Statistics database")
        ]

        # Sort abbreviations alphabetically
        abbreviations.sort(key=lambda x: x[0])

        # Add each abbreviation to the list
        for abbr, full_text in abbreviations:
            doc.append(NoEscape(r'\textbf{' + abbr + r'} \> ' + full_text + r' \\'))

        doc.append(NoEscape(r'\end{tabbing}'))
    doc.append(NoEscape(r'%TC:endignore'))
