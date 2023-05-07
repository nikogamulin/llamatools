import re
import os

# Get the absolute path of the script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script folder
os.chdir(script_dir)

print(f'Working directory set to: {script_dir}')

# Open the original requirements.txt file
with open('../requirements.txt', 'r') as f:
    # Read all lines from the file
    lines = f.readlines()

# Create a regular expression to match local paths
pattern = re.compile(r'\s+@ file:\/\/.*')

# Filter out any lines that match the pattern
filtered_lines = [line for line in lines if not pattern.search(line)]

# Write the filtered lines to a new requirements.txt file
with open('../requirements_filtered.txt', 'w') as f:
    f.writelines(filtered_lines)

print('Local paths removed successfully!')