#!/bin/bash

# Input file
input_file="dag123.asc"

# Initialize variables
output_dir="./"
mkdir -p "$output_dir"
sta=""
chan=""
nsamp=0
data_lines=()
count=0

# Function to process a block of data
process_block() {
  # Generate output filename
  output_file="$output_dir/${sta}_${chan}.txt"
  echo "Processing block: sta=$sta, chan=$chan, nsamp=$nsamp"

  # Write data to output file
  printf "%s\n" "${data_lines[@]}" > "$output_file"

  # Reset variables
  sta=""
  chan=""
  nsamp=0
  data_lines=()
  count=0
}

# Read input file line by line
while IFS= read -r line || [ -n "$line" ]; do
  echo "Reading line: $line"
  if [ $count -eq 0 ]; then
    # Extract values from the first line
    sta=$(echo "$line" | grep -oP '(?<=sta=)[^\s]+')
    chan=$(echo "$line" | grep -oP '(?<=chan=)[^\s]+')
    nsamp=$(echo "$line" | grep -oP '(?<=nsamp=)[^\s]+')
    echo "Extracted values: sta=$sta, chan=$chan, nsamp=$nsamp"
  elif [ $count -lt 4 ]; then
    # Collect first four lines (do nothing special)
    :
  else
    # Collect data lines
    data_lines+=("$line")
    echo "Collected data line: $line"
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

