import pandas as pd
import re

import pandas as pd
import re

# Paths to the .txt files
ns_file_path = "./data/estimations_results/results_ns_post_model.txt"
ss_file_path = "./data/estimations_results/results_ss_post_model.txt"

# Function to read and parse the .txt files
def parse_results(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    variables = []
    coefficients = {}
    std_errors = {}

    for line in lines:
        # Match lines with variable names and coefficients
        var_match = re.match(r"^(\w+)\s+(-?\d+\.\d+[\*]*)", line)
        std_err_match = re.match(r"^\s+\((\d+\.\d+)\)", line)
        
        if var_match:
            variable = var_match.group(1)
            coefficient = var_match.group(2)
            coefficients[variable] = coefficient
            variables.append(variable)
        elif std_err_match and variables:
            std_error = std_err_match.group(1)
            last_variable = variables[-1]
            std_errors[last_variable] = std_error
    
    return variables, coefficients, std_errors

# Parse the results from the NS and SS models
variables_ns, coefficients_ns, std_errors_ns = parse_results(ns_file_path)
variables_ss, coefficients_ss, std_errors_ss = parse_results(ss_file_path)

# Create a set of all unique variables
all_variables = set(variables_ns + variables_ss)

# Function to format LaTeX table rows
def format_latex_row(var, coef_ns, err_ns, coef_ss, err_ss):
    return f"            {var} & {coef_ns} & {err_ns} & {coef_ss} & {err_ss} \\\\\n"

# Create LaTeX table string
latex_table = r"""
\begin{table}[H]
    \centering
    \begin{threeparttable}
        \begin{tabular}{lcccc}
            \toprule
            & \multicolumn{2}{c}{NS Model} & \multicolumn{2}{c}{SS Model} \\
            \cmidrule(lr){2-3} \cmidrule(lr){4-5}
            Variable & Coefficient & Std. Error & Coefficient & Std. Error \\
            \midrule
"""

# Add rows for each variable
for var in sorted(all_variables):
    coef_ns = coefficients_ns.get(var, "")
    err_ns = f"({std_errors_ns.get(var, '')})" if var in std_errors_ns else ""
    coef_ss = coefficients_ss.get(var, "")
    err_ss = f"({std_errors_ss.get(var, '')})" if var in std_errors_ss else ""
    
    # Formatting coefficients with significance stars
    def format_coef(coef):
        if coef:
            coef_str = coef.replace('*', r'\ast')
            formatted_coefficient = re.sub(r'\*+', lambda m: r'\ast' * len(m.group(0)), coef_str)
            # formatted_coefficient = re.sub(r'\*+', lambda m: r'$^{\ast' * len(m.group(0)) + '}$', coef_str)
            if r'\ast' in formatted_coefficient:
                formatted_coefficient = re.sub(r'(\d+\.\d+)', r'\1$^{', formatted_coefficient) + '}$'
            return formatted_coefficient
        return ""
#             # Replace '*' with '\ast' and wrap in a single superscript block
#             formatted_coefficient = re.sub(r'\*+', lambda m: r'\ast' * len(m.group(0)), coeff_str)
            
#             # Wrap the entire coefficient with superscript braces
#             if r'\ast' in formatted_coefficient:
#                 formatted_coefficient = re.sub(r'(\d+\.\d+)', r'\1$^{', formatted_coefficient) + '}$'

    coef_ns = format_coef(coef_ns)
    coef_ss = format_coef(coef_ss)
    
    latex_table += format_latex_row(var, coef_ns, err_ns, coef_ss, err_ss)

# Add the closing lines for the table
latex_table += r"""
            \bottomrule
        \end{tabular}
        \begin{tablenotes}
            \footnotesize
            \item Robust standard errors in parentheses.
            \item $^{\ast\ast\ast}$ p<0.01, $^{\ast\ast}$ p<0.05, $^{\ast}$ p<0.1
        \end{tablenotes}
    \end{threeparttable}
    \caption{Estimation Results for NS and SS Models}
    \label{tab:ns_ss_post_model}
\end{table}
"""

# Save the LaTeX table string to a .tex file
tex_file_path = "./tex/tables/ns_ss_post_table.tex"
with open(tex_file_path, 'w') as file:
    file.write(latex_table)

print(f"LaTeX table saved to {tex_file_path}")

# # Paths to the .txt files
# ns_file_path = "./data/estimations_results/results_ns_post_model.txt"
# ss_file_path = "./data/estimations_results/results_ss_post_model.txt"

# def parse_results(file_path):
#     try:
#         with open(file_path, 'r') as file:
#             lines = file.readlines()
#     except FileNotFoundError:
#         print(f"File not found: {file_path}")
#         return [], [], []
    
#     variables = []
#     coefficients = []
#     std_errors = []

#     for line in lines:
#         var_match = re.match(r"^(\w+)\s+(-?\d+\.\d+[\*]*)", line)
#         std_err_match = re.match(r"^\s+\((\d+\.\d+)\)", line)
        
#         # if var_match:
#         #     variables.append(var_match.group(1))
#         #     coefficients.append(var_match.group(2).replace('*', r'\ast'))

#         # Assuming var_match is a match object from a regex search
#         if var_match:
#             variables.append(var_match.group(1))
            
#             # Extract the coefficient string
#             coeff_str = var_match.group(2)
            
#             # Replace '*' with '\ast' and wrap in a single superscript block
#             formatted_coefficient = re.sub(r'\*+', lambda m: r'\ast' * len(m.group(0)), coeff_str)
            
#             # Wrap the entire coefficient with superscript braces
#             if r'\ast' in formatted_coefficient:
#                 formatted_coefficient = re.sub(r'(\d+\.\d+)', r'\1$^{', formatted_coefficient) + '}$'
            
#             coefficients.append(formatted_coefficient)
#         elif std_err_match:
#             std_errors.append(f"({std_err_match.group(1)})")
    
#     return variables, coefficients, std_errors

# # Parse the results from the NS and SS models
# variables_ns, coefficients_ns, std_errors_ns = parse_results(ns_file_path)
# variables_ss, coefficients_ss, std_errors_ss = parse_results(ss_file_path)

# # Debugging: print lengths of the lists
# if len(variables_ns) != len(coefficients_ns) or len(coefficients_ns) != len(std_errors_ns):
#     print("Warning: NS model data lengths do not match!")
# if len(variables_ss) != len(coefficients_ss) or len(coefficients_ss) != len(std_errors_ss):
#     print("Warning: SS model data lengths do not match!")

# # Function to format LaTeX table rows
# def format_latex_row(var, coef_ns, err_ns, coef_ss, err_ss):
#     return f"            {var} & {coef_ns} & {err_ns} & {coef_ss} & {err_ss} \\\\\n"

# latex_table = r"""
# \begin{table}[H]
#     \centering
#     \begin{threeparttable}
#         \begin{tabular}{lcccc}
#             \toprule
#             & \multicolumn{2}{c}{NS Model} & \multicolumn{2}{c}{SS Model} \\
#             \cmidrule(lr){2-3} \cmidrule(lr){4-5}
#             Variable & Coefficient & Std. Error & Coefficient & Std. Error \\
#             \midrule
# """

# # Add rows for each variable
# for var, coef_ns, err_ns, coef_ss, err_ss in zip(variables_ns, coefficients_ns, std_errors_ns, coefficients_ss, std_errors_ss):
#     latex_table += format_latex_row(var, coef_ns, err_ns, coef_ss, err_ss)

# # Add the closing lines for the table
# latex_table += r"""
#             \bottomrule
#         \end{tabular}
#         \begin{tablenotes}
#             \footnotesize
#             \item Robust standard errors in parentheses.
#             \item $^{\ast\ast\ast}$ p<0.01, $^{\ast\ast}$ p<0.05, $^{\ast}$ p<0.1
#         \end{tablenotes}
#     \end{threeparttable}
#     \caption{Estimation Results for NS and SS Models}
#     \label{tab:ns_ss_post_model}
# \end{table}
# """

# # Save the LaTeX table string to a .tex file
# tex_file_path = "./tex/tables/ns_ss_post_table.tex"
# with open(tex_file_path, 'w') as file:
#     file.write(latex_table)

# print(f"LaTeX table saved to {tex_file_path}")

################################################################
# import pandas as pd
# from pylatex import Document, Section, Tabular, Package, NoEscape

# # Function to add significance stars
# def add_significance_stars(p_value):
#     if p_value < 0.01:
#         return '***'
#     elif p_value < 0.05:
#         return '**'
#     elif p_value < 0.1:
#         return '*'
#     else:
#         return ''

# # Read the CSV files
# file1 = "./data/estimations_results/results_ns_post_model.csv"
# file2 = "./data/estimations_results/results_ss_post_model.csv"

# results_ns_post = pd.read_csv(file1)
# results_ss_post = pd.read_csv(file2)

# # Combine the DataFrames for easier manipulation
# combined_results = pd.concat([results_ns_post, results_ss_post], axis=1)
# print(combined_results)

# combined_results.columns = ['Variable', 'Coefficient_NS', 'Std_Error_NS', 'P_Value_NS', 'Observations_NS', 'Variable_SS', 'Coefficient_SS', 'Std_Error_SS', 'P_Value_SS', 'Observations_SS']

# # Create LaTeX table string
# latex_table = """
# \\begin{table}[H]
#     \\centering
#     \\begin{tabular}{lcccc}
#         \\toprule
#         & \\multicolumn{2}{c}{NS Model} & \\multicolumn{2}{c}{SS Model} \\\\
#         \\cmidrule(lr){2-3} \\cmidrule(lr){4-5}
#         Variable & Coefficient & Std. Error & Coefficient & Std. Error \\\\
#         \\midrule
# """

# for idx, row in combined_results.iterrows():
#     coef_ns = f"{row['Coefficient_NS']:.4f}{add_significance_stars(row['P_Value_NS'])}"
#     coef_ss = f"{row['Coefficient_SS']:.4f}{add_significance_stars(row['P_Value_SS'])}"
#     latex_table += f"        {row['Variable']} & {coef_ns} & {row['Std_Error_NS']:.4f} & {coef_ss} & {row['Std_Error_SS']:.4f} \\\\\n"

# latex_table += """
#         \\bottomrule
#     \\end{tabular}
#     \\caption{Estimation Results}
#     \\label{tab:estimation_results}
# \\end{table}
# """

# # Save the LaTeX table string to a .tex file
# tex_file_path = "./tex/tables/ns_ss_post_table.tex"
# with open(tex_file_path, 'w') as file:
#     file.write(latex_table)

# print(f"LaTeX table saved to {tex_file_path}")

##################################################################

# # Read the CSV files
# file1 = "./data/estimations_results/results_ns_post_model.csv"
# file2 = "./data/estimations_results/results_ss_post_model.csv"

# results_ns_post = pd.read_csv(file1)
# results_ss_post = pd.read_csv(file2)

# # Combine the DataFrames for easier manipulation
# combined_results = pd.concat([results_ns_post, results_ss_post], axis=1)
# combined_results.columns = ['Variable', 'Coefficient_NS', 'Std_Error_NS', 'Observations_NS', 'Variable_SS', 'Coefficient_SS', 'Std_Error_SS', 'Observations_SS']

# # Create LaTeX table string
# latex_table = """
# \\begin{table}[H]
#     \\centering
#     \\begin{tabular}{lcccc}
#         \\toprule
#         & \\multicolumn{2}{c}{NS Model} & \\multicolumn{2}{c}{SS Model} \\\\
#         \\cmidrule(lr){2-3} \\cmidrule(lr){4-5}
#         Variable & Coefficient & Std. Error & Coefficient & Std. Error \\\\
#         \\midrule
# """

# for idx, row in combined_results.iterrows():
#     latex_table += f"        {row['Variable']} & {row['Coefficient_NS']:.4f} & {row['Std_Error_NS']:.4f} & {row['Coefficient_SS']:.4f} & {row['Std_Error_SS']:.4f} \\\\\n"

# latex_table += """
#         \\bottomrule
#     \\end{tabular}
#     \\caption{Estimation Results}
#     \\label{tab:estimation_results}
# \\end{table}
# """

# # Save the LaTeX table string to a .tex file
# tex_file_path = "./tex/tables/ns_ss_post_table.tex"
# with open(tex_file_path, 'w') as file:
#     file.write(latex_table)

# print(f"LaTeX table saved to {tex_file_path}")