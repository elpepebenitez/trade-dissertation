from pylatex import Document, Command, NoEscape
import subprocess
import os

# Import section functions
from sections.title import add_title
from sections.abstract import add_abstract
# from sections.abbreviations import add_abbreviations
# from sections.list_of_figures import add_list_of_figures
# from sections.list_of_tables import add_list_of_tables
from sections.introduction import add_introduction
# from sections.literature_review import add_literature_review
# from sections.methodology import add_methodology
# from sections.findings import add_findings
# from sections.analysis_and_discussion import add_analysis_and_discussion
# from sections.conclusion import add_conclusion
from sections.references import add_references
# from sections.appendix import add_appendix

# Change the current working directory to the tex folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create a new document
doc = Document('dissertation')

# Add necessary packages for bibliography
doc.packages.append(NoEscape(r'\usepackage[backend=biber]{biblatex}'))
doc.preamble.append(NoEscape(r'\addbibresource{references.bib}'))

# Add a title
add_title(doc)

# Add abstract
add_abstract(doc)

# Add table of contents
doc.append(NoEscape(r'\tableofcontents'))
doc.append(NoEscape(r'\newpage'))

# Add abbreviations
# add_abbreviations(doc)

# Add list of figures
doc.append(NoEscape(r'\listoffigures'))
doc.append(NoEscape(r'\newpage'))

# Add list of tables
doc.append(NoEscape(r'\listoftables'))
doc.append(NoEscape(r'\newpage'))

# Add main sections
add_introduction(doc)
# add_literature_review(doc)
# add_methodology(doc)
# add_findings(doc)
# add_analysis_and_discussion(doc)
# add_conclusion(doc)

# Add references
doc.append(NoEscape(r'\newpage'))
add_references(doc)

# Add appendix
# add_appendix(doc)

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
