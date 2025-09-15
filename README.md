Universal Univariate Analysis Tool
A command-line Python script that automates univariate analysis for any given CSV file. It intelligently distinguishes between numeric and categorical columns to generate and display relevant statistical insights.

For each column, the script prints a detailed summary to the console. It also generates and saves distribution plots as PNG images in a plots/ directory, making it an ideal tool for rapid initial data exploration.

Features
Automatic Analysis: Detects whether each column is numeric or categorical and applies the appropriate analysis.

In-Depth Summaries: Calculates key statistics (mean, median, percentiles) for numeric data and frequency counts for categorical data.

Smart Visualizations: Creates styled bar plots for each column's distribution. To maintain clarity, it automatically skips plotting for categorical columns with more than 50 unique values.

Simple CLI Interface: Just provide the path to your CSV file and let the script do the rest.

How to Use
Install Dependencies: Make sure you have the required Python libraries installed.

bash
pip install pandas numpy matplotlib
Run from Terminal: Execute the script and pass the path to your CSV file as an argument.

bash
python analysis.py "path/to/your/dataset.csv"
Output
Console: Detailed statistical summaries for each column will be printed directly to your terminal.

Image Files: Bar plots for each column's distribution will be saved as .png files inside a newly created plots/ directory.
