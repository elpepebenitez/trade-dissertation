from pylatex import Document, PageStyle, Command, NoEscape, Package
import subprocess
import os

# Import section functions
from sections.title import add_title
from sections.abstract import add_abstract
from sections.abbreviations import add_abbreviations
from sections.list_of_figures import add_list_of_figures
from sections.list_of_tables import add_list_of_tables
from sections.introduction import add_introduction
from sections.literature_review import add_literature_review
from sections.methodology import add_methodology
from sections.findings import add_findings
from sections.analysis_and_discussion import add_analysis_and_discussion
from sections.conclusion import add_conclusion
from sections.references import add_references
from sections.appendix import add_appendix

# Change the current working directory to the tex folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create a new document
doc = Document('23802_DV410_2024', documentclass='article')

# Add necessary packages
# doc.packages.append(NoEscape(r'\usepackage[backend=biber]{biblatex}'))
doc.packages.append(Package('biblatex', options='backend=biber'))
doc.packages.append(NoEscape(r'\usepackage{fancyhdr}'))
doc.packages.append(NoEscape(r'\usepackage{lastpage}'))
doc.packages.append(NoEscape(r'\usepackage{ragged2e}'))
doc.packages.append(NoEscape(r'\usepackage{pdfpages}'))  # Add pdfpages package
doc.packages.append(NoEscape(r'\usepackage{hyperref}'))  # Add hyperref package for links
doc.packages.append(Package('booktabs'))
doc.packages.append(Package('float'))
doc.packages.append(Package('threeparttable'))
doc.packages.append(Package('amssymb'))
doc.packages.append(Package('amsmath'))
doc.packages.append(Package('adjustbox'))
doc.packages.append(Package('geometry'))  # Add the geometry package
doc.packages.append(Package('inputenc', options='utf8'))

# Set the margins using the geometry package
doc.preamble.append(NoEscape(r'\geometry{left=1in, right=1in, top=1in, bottom=1in}'))

doc.preamble.append(NoEscape(r'\addbibresource{references.bib}'))
doc.preamble.append(NoEscape(r'\hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue}'))

# Define page styles
front_matter_style = PageStyle("frontmatter")
front_matter_style.append(NoEscape(r'\fancyhf{}'))
front_matter_style.append(NoEscape(r'\fancyhead[L]{DV410}'))
front_matter_style.append(NoEscape(r'\fancyhead[C]{\thepage}'))
front_matter_style.append(NoEscape(r'\fancyhead[R]{23802}'))
doc.preamble.append(front_matter_style)

main_matter_style = PageStyle("mainmatter")
main_matter_style.append(NoEscape(r'\fancyhf{}'))
main_matter_style.append(NoEscape(r'\fancyhead[L]{DV410}'))
main_matter_style.append(NoEscape(r'\fancyhead[C]{Page \thepage\ of \pageref{LastPage}}'))
main_matter_style.append(NoEscape(r'\fancyhead[R]{23802}'))
doc.preamble.append(main_matter_style)

# Include the external PDF at the beginning (excluded from TOC and page count)
doc.append(NoEscape(r'\includepdf[pages=-, offset=0 -1cm, frame]{DV410_Dissertation Cover Sheet_ Consent Form_Front Page_2023-24.pdf}'))

# Set roman numbering for the front matter
doc.preamble.append(NoEscape(r'\pagenumbering{roman}'))
doc.append(NoEscape(r'\pagestyle{frontmatter}'))

# Configure the header
doc.preamble.append(NoEscape(r'\pagestyle{fancy}'))
doc.preamble.append(NoEscape(r'\fancyhf{}'))  # Clear all header and footer fields
doc.preamble.append(NoEscape(r'\fancyhead[L]{DV410}'))
doc.preamble.append(NoEscape(r'\fancyhead[C]{Page \thepage\ of \pageref{LastPage}}'))
doc.preamble.append(NoEscape(r'\fancyhead[R]{23802}'))

add_title(doc)
doc.append(NoEscape(r'\newpage'))
add_abstract(doc)
doc.append(NoEscape(r'\newpage'))
doc.append(NoEscape(r'\tableofcontents'))
doc.append(NoEscape(r'\newpage'))
add_abbreviations(doc)
doc.append(NoEscape(r'\newpage'))
add_list_of_figures(doc)
doc.append(NoEscape(r'\newpage'))
add_list_of_tables(doc)
doc.append(NoEscape(r'\newpage'))

# Switch to Arabic numbering starting from the introduction
doc.append(NoEscape(r'\pagenumbering{arabic}'))
doc.append(NoEscape(r'\pagestyle{mainmatter}'))

# Add main sections
add_introduction(doc)
add_literature_review(doc)
add_methodology(doc)
add_findings(doc)
add_analysis_and_discussion(doc)
add_conclusion(doc)
doc.append(NoEscape(r'\newpage'))

# Add references
add_references(doc)
doc.append(NoEscape(r'\newpage'))

# Add appendix
add_appendix(doc)

# Save the LaTeX document
doc.generate_tex('23802_DV410_2024')

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
    run_command('pdflatex -interaction=nonstopmode 23802_DV410_2024.tex')
    
    # Run biber
    run_command('biber 23802_DV410_2024')
    
    # Second pdflatex pass
    run_command('pdflatex -interaction=nonstopmode 23802_DV410_2024.tex')
    
    # Final pdflatex pass
    run_command('pdflatex -interaction=nonstopmode 23802_DV410_2024.tex')
    
    print("PDF generated successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

# Define word_count variable
word_count = "Error"  # Default value in case of an error

# Run texcount to get word count, excluding certain sections
try:
    texcount_command = 'texcount -inc -total -1 23802_DV410_2024.tex'
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
with open('23802_DV410_2024.tex', 'r') as f:
    lines = f.readlines()

with open('23802_DV410_2024.tex', 'w') as f:
    for line in lines:
        f.write(line)
        if r'\maketitle' in line:
            f.write(f'\n\\vfill\n\\begin{{center}}\\textbf{{Word Count: {word_count}}}\\end{{center}}\n')

# Run the final pdflatex pass to include the word count
try:
    print(run_command('pdflatex -interaction=nonstopmode 23802_DV410_2024.tex'))
    print("Final PDF with word count generated successfully.")
except Exception as e:
    print(f"An error occurred during the final PDF generation: {e}")
