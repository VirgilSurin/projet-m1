#!/bin/bash

# Check if a file and an output directory were specified as arguments
if [ $# -lt 2 ]
then
    echo "Error: No input file or output directory specified"
    exit 1
fi

# Save the input file name and output directory
input_file=$1
output_dir=$2

# Initialize a counter variable
counter=1

# Read each line in the input file
while IFS= read -r line
do
    # Create a new .in file in the specified output directory and write the line to it
    echo "$line" > "$output_dir/$counter".in
    # Increment the counter variable
    counter=$((counter+1))
done < "$input_file"
