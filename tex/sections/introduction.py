from pylatex import Section, Subsection, NoEscape, NewPage, Subsubsection, Command, Figure

def add_introduction(doc):
    with doc.create(Section('Introduction')):      
        with open('sections/introduction.tex', 'r') as file:
            introduction_content = file.read()
        doc.append(NoEscape(introduction_content))

        with doc.create(Figure(position='h!')) as tas_per_year:
                tas_per_year.add_image('figures/all_entries_agreements_per_year.jpg', width=NoEscape(r'0.8\textwidth'))
                tas_per_year.add_caption('Trade Agreements Per Year')
        # Adding the source as a separate paragraph
        doc.append(Command('FloatBarrier'))
        doc.append(NoEscape(r'\textit{Source: Visualisation made by author. Data by The Design of International Trade Agreements Database (DESTA).}'))
        doc.append(Command('FloatBarrier'))

        doc.append('Moreover, the vast majority of TAs have been signed between developing countries, what is referred to as “South-South” trade cooperation, covering an increasingly important share of global trade across industries. Figure 2 shows the historical evolution of South-South TAs, Figure 3 shows the historical evolution of North-South TAs, and Figure 4 shows the historical evolution of North-North TAs, showcasing the significant difference in the number of agreements and countries belonging to each group.')
        
        with doc.create(Figure(position='h!')) as ss_tas_per_year:
                ss_tas_per_year.add_image('figures/agreements_per_year_South-South.jpg', width=NoEscape(r'0.8\textwidth'))
                ss_tas_per_year.add_caption('Trade Agreements Per Year (South-South).')
                # ss_tas_per_year.add_text(NoEscape(r'\textbf{Source:} Visualisation made by author. Data by The Design of International Trade Agreements Database (DESTA).'))
        doc.append(Command('FloatBarrier'))
        doc.append(NoEscape(r'\textit{Source: Visualisation made by author. Data by The Design of International Trade Agreements Database (DESTA).}'))
        doc.append(Command('FloatBarrier'))
        
        with doc.create(Figure(position='h!')) as ns_tas_per_year:
                ns_tas_per_year.add_image('figures/agreements_per_year_North-South.jpg', width=NoEscape(r'0.8\textwidth'))
                ns_tas_per_year.add_caption('Trade Agreements Per Year (North-South).')
                # ns_tas_per_year.add_text(NoEscape(r'\textbf{Source:} Visualisation made by author. Data by The Design of International Trade Agreements Database (DESTA).'))
        doc.append(Command('FloatBarrier'))
        doc.append(NoEscape(r'\textit{Source: Visualisation made by author. Data by The Design of International Trade Agreements Database (DESTA).}'))
        doc.append(Command('FloatBarrier'))
        
        with doc.create(Figure(position='h!')) as nn_tas_per_year:
                nn_tas_per_year.add_image('figures/agreements_per_year_North-North.jpg', width=NoEscape(r'0.8\textwidth'))
                nn_tas_per_year.add_caption('Trade Agreements Per Year (North-North).')
                # nn_tas_per_year.add_text(NoEscape(r'\textbf{Source:} Visualisation made by author. Data by The Design of International Trade Agreements Database (DESTA).'))
        doc.append(Command('FloatBarrier'))
        doc.append(NoEscape(r'\textit{Source: Visualisation made by author. Data by The Design of International Trade Agreements Database (DESTA).}'))
        doc.append(Command('FloatBarrier'))

        with open('sections/research_introduction.tex', 'r') as file:
            research_introduction_content = file.read()
        doc.append(NoEscape(research_introduction_content))