import os

# Input file
#input_file = "dag123.asc"
#input_file = "/home/pth/WORKSHOP/QAANAAQ/DATA/i18dk2022123.asc"
nlines = 3
input_file = "/dmidata/users/nje/Work/Infrasound/Datafiles/i18dk2023259.asc"
nlines = 4 #3 # see the number of alpha lines in the input file, could be 4 or 3

# Initialize variables
output_dir = "./"
os.makedirs(output_dir, exist_ok=True)

sta = ""
chan = ""
nsamp = 0
samprate = 0.0
time = 0.0
data_lines = []

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
            # Extract values from the first line
            sta = line.split('sta=')[1].split()[0]
            chan = line.split('chan=')[1].split()[0]
            nsamp = int(line.split('nsamp=')[1].split()[0])
            samprate = float(line.split('samprate=')[1].split()[0])
            time = float(line.split('time=')[1].split()[0])
        elif count < nlines:
            # Collect first 'nlines'lines (do nothing special) (might have to edit 3 to 4)
            pass
        else:
            # Collect data lines
            data_lines.append(line)
        
        # Increment count
        count += 1
        print(count)
        # If collected the required number of samples, process the block
#       if count == (nsamp + 4):
        if count == (nsamp + nlines):
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

