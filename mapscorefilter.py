
def read_bedgraph(bed_path):   #Read a BED file and extract positions and scores
    positions = []
    scores = []
    with open(bed_path, 'r') as bed:
        for line in bed:
            if line.startswith('track') or line.startswith('#'):
                continue  # Skip header lines
            parts = line.strip().split()
            if len(parts) < 4:
                continue  # Skip invalid lines
            chrom, start, end, score = parts[:4]
            start, end, score = int(start), int(end), float(score)
            positions.extend(range(start, end))
            scores.extend([score] * (end - start))
    return positions, scores


def read_fasta(file_path):  #Loads a FASTA file that will be edited later
    sequences = {}
    with open(file_path, 'r') as file:
        sequence_id = None
        sequence = ''
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                if sequence_id:
                    sequences[sequence_id] = sequence
                sequence_id = line[1:]
                sequence = ''
            else:
                sequence += line
        if sequence_id:
            sequences[sequence_id] = sequence
    return sequences


def process_sequences(vector, threshold, fasta_file):   #Rewrites base pairs under the given threshold to N
    sequences = read_fasta(fasta_file)
    base_pairs_changed = 0
    for seq_id, seq in sequences.items():
        if len(seq) != len(vector):
            print(f"Length mismatch for sequence {seq_id}. Skipping.")
            continue
        modified_seq = ''
        for i in range(len(seq)):
            if vector[i] <= threshold:
                modified_seq += 'N'
                base_pairs_changed += 1     #Keeps track of the number of base pairs changed
            else:
                modified_seq += seq[i]
        sequences[seq_id] = modified_seq
    return sequences, base_pairs_changed

def write_fasta(sequences, output_file):    #Writes the new FASTA file
    with open(output_file, 'w') as file:
        for seq_id, seq in sequences.items():
            file.write(f">{seq_id}\n{seq}\n")


def log_notes(original_file, threshold, base_pairs_changed, notes_file):    #Logs the process
    with open(notes_file, 'w') as file:
        file.write(f"Original file: {original_file}\n")
        file.write(f"Threshold value: {threshold}\n")
        file.write(f"Number of base pairs changed: {base_pairs_changed}\n")


if __name__ == "__main__":
    bedgraph_file = input("Input bedgraph file with mapscores:")
    positions, scores = read_bedgraph(bedgraph_file)

    print("Length of original data:", len(positions))

    vector = scores  # Example vector of values
    threshold = float(input("Threshold value:"))  # Threshold value under which all base pairs are discarded
    fasta_file = input("Input fasta file:")  # Input multi-FASTA file
    output_file = input("Output file name:")  # Output file name
    processed_sequences, base_pairs_changed = process_sequences(vector, threshold, fasta_file)
    write_fasta(processed_sequences, output_file)
    print("Output written to", output_file)

    notes_file = input("Output log file:")
    log_notes(fasta_file, threshold, base_pairs_changed, notes_file)
    print("Notes logged in", notes_file)
