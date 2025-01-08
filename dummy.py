# Configuration
nlines = 1  # Number of lines to read for each header
import os
import re

# Configuration
input_file = "/home/pth/WORKSHOP/QAANAAQ/DATA/IS18_2018206.dat"
output_dir = "OUTPUT/IS18/"
os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

# Number of lines to read for each header
nlines = 1  # Number of header lines

# Initialize variables
data_lines = []

def process_block(output_dir, sta, chan, nsamp, time, samprate, data_lines):
    """
    Processes a block of data and writes it to a file.
    """
    identifier = sta  # Use 'sta' as the identifier for the filename (customize as needed)
    output_file = os.path.join(output_dir, f"{identifier}_{chan}_{nsamp}.txt")
    print(f"Writing to {output_file}")

    try:
        with open(output_file, 'w') as f:
            for i, line in enumerate(data_lines):
                current_time = time + i / samprate
                f.write(f"{current_time:.2f} {line}\n")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

# Main script
try:
    with open(input_file, 'r') as f:
        count = 0
        while True:
            line = f.readline().strip()
            if not line:  # Break if the end of the file is reached
                break

            # Check if the line is a header line
            if re.match(r"^\s*[\w.]+", line):  # Match the header identifier format
                # If we have collected data, process it before reading a new header
                if data_lines:
                    process_block(output_dir, sta, chan, nsamp, time, samprate, data_lines)

                    # Reset variables for the next block
                    data_lines = []
                    count = 0

                # Parse the current header
                parts = line.split('|')
                if len(parts) >= 2:
                    header_info = parts[0].strip().split()
                    if len(header_info) >= 3:
                        # Extract the metadata (e.g., 'IM.I18H1..BDF', '20.0 Hz', '1728000 samples')
                        sta = header_info[0]
                        chan = header_info[1]
                        time = float(header_info[2].split('T')[0].strip())

                        # Extract the sample rate and number of samples
                        match = re.search(r"([\d.]+) Hz", line)
                        if match:
                            samprate = 1 / float(match.group(1))
                        else:
                            raise ValueError("Invalid frequency value in header: Hz not found or improperly formatted")

                        match = re.search(r"(\d+) samples", line)
                        if match:
                            nsamp = int(match.group(1))
                        else:
                            raise ValueError("Invalid number of samples in header: 'samples' not found or improperly formatted")
                    else:
                        raise ValueError("Invalid metadata in header: Missing necessary fields")

                else:
                    raise ValueError("Invalid metadata in header: Missing necessary fields")

                continue  # Skip to the next line after parsing the header

            # Collect data lines for the current block
            if count < nsamp:
                data_lines.append(line)
                count += 1

        # Process any remaining data if present after reading the file
        if data_lines:
            process_block(output_dir, sta, chan, nsamp, time, samprate, data_lines)

    print("Finished processing file.")

except FileNotFoundError:
    print(f"Error: File {input_file} not found.")
except ValueError as ve:
    print(f"Metadata validation error: {ve}")
except Exception as e:
    print(f"An error occurred: {e}")

