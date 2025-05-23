#!/bin/bash

# Input file
input_file="dag123.asc"

# Initialize variables
output_dir="./"
mkdir -p "$output_dir"
sta=""
chan=""
nsamp=0
samprate=0
time=0
data_lines=()
count=0

# Function to process a block of data
process_block() {
  # Generate output filename
  output_file="$output_dir/${sta}_${chan}_${nsamp}.txt"

  # Write data to output file with computed time values
  for i in "${!data_lines[@]}"; do
    current_time=$(echo "$time + $i / $samprate" | bc -l)
    echo "$current_time ${data_lines[i]}" >> "$output_file"
#   echo $current_time ${data_lines[i]}
  done

  # Reset variables
  sta=""
  chan=""
  nsamp=0
  samprate=0
  time=0
  data_lines=()
  count=0
}

# Read input file line by line
while IFS= read -r line || [ -n "$line" ]; do
  if [ $count -eq 0 ]; then
    # Extract values from the first line
    sta=$(echo "$line" | grep -oP '(?<=sta=)[^\s]+')
    chan=$(echo "$line" | grep -oP '(?<=chan=)[^\s]+')
    nsamp=$(echo "$line" | grep -oP '(?<=nsamp=)[^\s]+')
    samprate=$(echo "$line" | grep -oP '(?<=samprate=)[^\s]+')
    time=$(echo "$line" | grep -oP '(?<=time=)[^\s]+')
  elif [ $count -lt 4 ]; then
    # Collect first four lines (do nothing special)
    :
  else
    # Collect data lines
    data_lines+=("$line")
  fi

  # Increment count
  ((count++))

  # If collected the required number of samples, process the block
  if [ $count -eq $((nsamp + 4)) ]; then
    process_block
  fi
done < "$input_file"

# Process any remaining data block
if [ $count -eq $((nsamp + 4)) ]; then
  process_block
fi

echo "Finished processing file."

