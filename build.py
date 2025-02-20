#!/usr/bin/env python

import yaml

# Sample data for the table
data = [
    ["Name", "Age", "Occupation"],
    ["Alice", 30, "Engineer"],
    ["Bob", 25, "Designer"],
    ["Charlie", 35, "Teacher"]
]

# Function to generate LaTeX table code
def generate_latex_table(data):
    # Start the table
    latex_code = "\\begin{tabular}{|c|c|c|}\n\\hline\n"

    # Add headers and data rows
    for row in data:
        latex_code += " & ".join(str(cell) for cell in row) + " \\\\ \n\\hline\n"

    # End the table
    latex_code += "\\end{tabular}"

    return latex_code

# Generate the LaTeX code for the table
latex_table = generate_latex_table(data)

# Output the LaTeX table code
f = open("tables/test-python.tex", "a")
f.write(latex_table)
f.close()
