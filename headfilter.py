

# Specify the input multifasta file name
input_file = "multiychrom10000.fasta"

# Specify the output file name for headers
output_file = "haplotypeheaders.fasta"

# Open the input file for reading
with open(input_file, "r") as file:
    # Open the output file for writing
    with open(output_file, "w") as output:
        # Iterate over each line in the input file
        for line in file:
            # Check if the line starts with ">" (header line)
            if line.startswith(">"):
                # Write the header line to the output file
                output.write(line)

print("Headers extracted and saved to", output_file)