#!/bin/bash
# need tree package to install
# Get the current date and time
current_datetime=$(date "+%Y-%m-%d %H:%M:%S")

# Create a temporary file for the tree output
temp_file=$(mktemp)

# Read .gitignore and convert to tree ignore pattern
if [ -f .gitignore ]; then
    gitignore_patterns=$(grep -v '^#' .gitignore | grep -v '^$' | tr '\n' '|' | sed 's/|$//')
    if [ -n "$gitignore_patterns" ]; then
        ignore_patterns="node_modules|.git|$gitignore_patterns"
    else
        ignore_patterns="node_modules|.git"
    fi
else
    ignore_patterns="node_modules|.git"
fi

# ignore the file in folder list 
ignore_folder_list=("scripts" "migrations")

# Generate tree structure with combined ignore patterns
echo "## Tree Diagram" > "$temp_file"
echo "" >> "$temp_file"
echo "Generated on: $current_datetime" >> "$temp_file"
echo "" >> "$temp_file"
echo "\`\`\`" >> "$temp_file"

# Convert ignore_folder_list to pipe-separated string for tree command
folder_ignore_pattern=$(printf "%s|" "${ignore_folder_list[@]}" | sed 's/|$//')
if [ -n "$folder_ignore_pattern" ]; then
    full_ignore_pattern="$ignore_patterns|$folder_ignore_pattern"
else
    full_ignore_pattern="$ignore_patterns"
fi

tree -L 3 -I "$full_ignore_pattern" >> "$temp_file"
echo "\`\`\`" >> "$temp_file"

# Find the line number where "## Tree Diagram" appears in README.md
line_number=$(grep -n "^## Tree Diagram" README.md | cut -d: -f1)

if [ -n "$line_number" ]; then
    # If "## Tree Diagram" section exists, replace everything after it
    head -n "$((line_number-1))" README.md > README.md.tmp
    cat "$temp_file" >> README.md.tmp
    mv README.md.tmp README.md
else
    # If section doesn't exist, append to the end of the file
    cat "$temp_file" >> README.md
fi

# Clean up temporary file
rm "$temp_file"
