from pylatex import Document, PageStyle, Command, NoEscape
import subprocess
import os

# Import section functions
from sections.title import add_title
from sections.abstract import add_abstract
from sections.abbreviations import add_abbreviations
from sections.list_of_figures import add_list_of_figures
from sections.list_of_tables import add_list_of_tables
from sections.introduction import add_introduction
# from sections.literature_review import add_literature_review
# from sections.methodology import add_methodology
# from sections.findings import add_findings
# from sections.analysis_and_discussion import add_analysis_and_discussion
# from sections.conclusion import add_conclusion
from sections.references import add_references
from sections.appendix import add_appendix

# Change the current working directory to the tex folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create a new document
doc = Document('dissertation')

# Add necessary packages
doc.packages.append(NoEscape(r'\usepackage[backend=biber]{biblatex}'))
doc.packages.append(NoEscape(r'\usepackage{fancyhdr}'))
doc.packages.append(NoEscape(r'\usepackage{lastpage}'))
doc.packages.append(NoEscape(r'\usepackage{ragged2e}'))
doc.preamble.append(NoEscape(r'\addbibresource{references.bib}'))

# Configure the header
doc.preamble.append(NoEscape(r'\pagestyle{fancy}'))
doc.preamble.append(NoEscape(r'\fancyhf{}'))  # Clear all header and footer fields
doc.preamble.append(NoEscape(r'\fancyhead[L]{DV410}'))
doc.preamble.append(NoEscape(r'\fancyhead[C]{Page \thepage\ of \pageref{LastPage}}'))
doc.preamble.append(NoEscape(r'\fancyhead[R]{23802}'))

# Add a title
add_title(doc)
doc.append(NoEscape(r'\newpage'))

# Add abstract
add_abstract(doc)
doc.append(NoEscape(r'\newpage'))

# Add table of contents
doc.append(NoEscape(r'\tableofcontents'))
doc.append(NoEscape(r'\newpage'))

# Add abbreviations
add_abbreviations(doc)
doc.append(NoEscape(r'\newpage'))

# Add list of figures
add_list_of_figures(doc)
# doc.append(NoEscape(r'\listoffigures'))
doc.append(NoEscape(r'\newpage'))

# Add list of tables
# doc.append(NoEscape(r'\listoftables'))
add_list_of_tables(doc)
doc.append(NoEscape(r'\newpage'))

# Add main sections
add_introduction(doc)
# add_literature_review(doc)
# add_methodology(doc)
# add_findings(doc)
# add_analysis_and_discussion(doc)
# add_conclusion(doc)
doc.append(NoEscape(r'\newpage'))

# Add references
add_references(doc)
doc.append(NoEscape(r'\newpage'))

# Add appendix
add_appendix(doc)

# Save the LaTeX document
doc.generate_tex('dissertation')

# Print current working directory and list files to debug path issues
# print("Current working directory:", os.getcwd())
# print("Files in current directory:", os.listdir('.'))

# Ensure that the LaTeX compiler is in the PATH
os.environ["PATH"] += os.pathsep + '/usr/texbin'  # Adjust the path as necessary

# Define a function to run a command and check for errors
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise Exception(f"Command '{command}' failed with return code {result.returncode}")

# Run the sequence of commands
try:
    # First pdflatex pass
    run_command('pdflatex -interaction=nonstopmode dissertation.tex')
    
    # Run biber
    run_command('biber dissertation')
    
    # Second pdflatex pass
    run_command('pdflatex -interaction=nonstopmode dissertation.tex')
    
    # Final pdflatex pass
    run_command('pdflatex -interaction=nonstopmode dissertation.tex')
    
    print("PDF generated successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

# Define word_count variable
word_count = "Error"  # Default value in case of an error

# Run texcount to get word count, excluding certain sections
try:
    texcount_command = 'texcount -inc -total -1 dissertation.tex'
    result = subprocess.run(texcount_command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise Exception(f"TeXcount command failed with return code {result.returncode}")
    
    # Extract the total word count
    output_lines = result.stdout.split('\n')
    print("Texcount Output:")
    print(result.stdout)  # Print the output for debugging
    
    for line in output_lines:
        if 'Total' in line:
            # Extract and sum the word counts
            counts = line.split(' ')[0].split('+')
            word_count = sum(map(int, counts))
            break
    
    if word_count == "Error":
        raise ValueError("Word count not found in texcount output.")
    
    print("Word count (excluding title, abstract, table of contents, abbreviation, list of figures, list of tables, references and appendix):")
    print(word_count)
except Exception as e:
    print(f"An error occurred while running TeXcount: {e}")

# Add the word count to the title page
with open('dissertation.tex', 'r') as f:
    lines = f.readlines()

with open('dissertation.tex', 'w') as f:
    for line in lines:
        f.write(line)
        if r'\maketitle' in line:
            f.write(f'\n\\vfill\n\\begin{{center}}\\textbf{{Total Word Count: {word_count}}}\\end{{center}}\n')

# Run the final pdflatex pass to include the word count
try:
    run_command('pdflatex -interaction=nonstopmode dissertation.tex')
    print("Final PDF with word count generated successfully.")
except Exception as e:
    print(f"An error occurred during the final PDF generation: {e}")
