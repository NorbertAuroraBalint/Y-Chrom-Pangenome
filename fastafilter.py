
def parse_multifasta(input_file, n, output_file):       #Takes a FASTA or multi-FASTA file and extracts the first n number of sequences
    with open(input_file, 'r') as f, open(output_file, 'w') as out:
        current_header = None
        current_sequence = ''
        for line in f:
            if line.startswith('>'):
                if current_header:
                    out.write(current_header + '\n')
                    out.write(current_sequence[:n] + '\n')
                current_header = line.strip()
                current_sequence = ''
            else:
                current_sequence += line.strip()

        # Write the last sequence
        if current_header:
            out.write(current_header + '\n')
            out.write(current_sequence[:n] + '\n')

if __name__ == "__main__":
    input_file = input("Enter the path to the multifasta file: ")
    n = int(input("Enter the number of nucleotides to extract from each sequence: "))
    output_file = input("Enter the path to the output file: ")

    parse_multifasta(input_file, n, output_file)