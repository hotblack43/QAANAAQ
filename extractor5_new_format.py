import os
from datetime import datetime

# Input file
input_file = "/home/pth/WORKSHOP/QAANAAQ/DATA/IS18_2018206.dat"
nlines = 1 

# Initialize variables
output_dir = "/dmidata/projects/nckf/earthshine/Infrasound/I18/"
os.makedirs(output_dir, exist_ok=True)

sta = ""
chan = ""
nsamp = 0
samprate = 0.0
time = 0.0
data_lines = []


def process_new_header(header_line):
    """
    Parses the new header format and extracts relevant details.

    Args:
        header_line (str): A single line containing the new header format.

    Returns:
        tuple: (sta, chan, nsamp, samprate, time) extracted from the header.
    """
    # Split the header into components
    parts = header_line.split('|')

    # Extract `sta` and `chan` from the first part
    first_part = parts[0].strip()  # "IM.I18H1..BDF"
    sta = first_part.split('.')[1]  # Extract "I18"
    chan = first_part.split('..')[-1]  # Extract "BDF"

    # Extract `time` from the second part and convert it to a float (Unix timestamp)
    time_str = parts[1].strip().split(' ')[0]  # Extract "2018-07-25T00:00:00.000000Z"
    time = datetime.fromisoformat(time_str.replace('Z', '+00:00')).timestamp()  # Convert to Unix time

    # Extract `samprate` and `nsamp` from the third part
    third_part = parts[2].strip()  # "20.0 Hz, 1728000 samples"
    samprate = third_part.split(' ')[0]  # Extract "20.0"
    nsamp = int(third_part.split(',')[1].strip().split(' ')[0])  # Extract "1728000"

    return sta, chan, nsamp, float(samprate), time



def process_block():
    # Generate output filename
    output_file = f"{output_dir}/{sta}_{chan}_{nsamp}.txt"
    print(output_file)

    with open(output_file, 'w') as f:
        # Write data to output file with computed time values
        for i, line in enumerate(data_lines):
            current_time = time + i / samprate
            f.write(f"{current_time:.2f} {line}\n")

# Read input file line by line
with open(input_file, 'r') as f:
    count = 0
    for line in f:
        line = line.strip()
        if count == 0:
            # Extract values from the header line
            sta, chan, nsamp, samprate, time = process_new_header(line)
        else:
            # Collect data lines
            data_lines.append(line)

        # Increment count
        count += 1
        # If collected the required number of samples, process the block
        if count == (nsamp + 1):  # Adjusted for the new header (single-line)
            process_block()
            # Reset variables for next block
            sta = ""
            chan = ""
            nsamp = 0
            samprate = 0.0
            time = 0.0
            data_lines = []
            count = 0

# Process any remaining data block
if data_lines:
    process_block()

print("Finished processing file.")

