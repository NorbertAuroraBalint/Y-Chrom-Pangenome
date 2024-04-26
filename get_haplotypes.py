
import gzip
import os

def convert_tsv_to_fasta(tsv_file, reference_fasta, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open reference FASTA and create a dictionary with the chromosome sequence
    with gzip.open(reference_fasta, "rt") as f:
        ref_seq = ""
        for line in f:
            if line.startswith(">"):
                continue
            ref_seq += line.strip()

    # Open the tsv file and read the haplotype SNPs
    with open(tsv_file) as f:
        haplotype_dict = {}
        for line in f:
            # Split the line into columns
            cols = line.strip().split("\t")
            haplotype_name = cols[1]
            try:
                pos = int(cols[2]) - 1  # 0-based indexing
            except:
                continue
            ref_base = cols[3]
            alt_base = cols[4]

            # Store the SNP position and alternate base in a dictionary
            if haplotype_name in haplotype_dict:
                haplotype_dict[haplotype_name][pos] = alt_base
            else:
                haplotype_dict[haplotype_name] = {pos: alt_base}

    # Create a new FASTA file for each haplotype
    for haplotype_name, snps in haplotype_dict.items():
        haplotype_file = os.path.join(output_dir, haplotype_name + ".fasta.gz")
        with gzip.open(haplotype_file, "wt") as out:
            out.write(">" + haplotype_name + "\n")
            # Replace the reference base with the alternate base at each SNP position
            new_seq = list(ref_seq)
            for pos, alt_base in snps.items():
                new_seq[pos] = alt_base
            out.write("".join(new_seq))


convert_tsv_to_fasta("211108.snps_isogg_curated.b38.txt", "GRCH38.p12_Y.fa.gz", "haplotypes")