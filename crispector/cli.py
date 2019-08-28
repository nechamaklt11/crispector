# -*- coding: utf-8 -*-

"""Console script for crispector."""
import sys
import click
import crispector
import os

# TODO - add a config from user + window_size + effective qualification window
@click.command()
@click.option('--tx_in1', '-t_r1', type=click.Path(exists=True), required=True,
              help="Treatment read 1 input path (string)")
@click.option('--tx_in2', '-t_r2', type=click.Path(exists=True), help="Treatment read 2 input path (string)")
@click.option('--mock_in1', '-m_r1', type=click.Path(exists=True), required=True,
              help="Mock read 1 input path (string)")
@click.option('--mock_in2', '-m_r2', type=click.Path(exists=True), help="Mock read 2 input path (string)")
@click.option("--amplicons_csv", '-a', type=click.Path(exists=True), required=True,
              help="A CSV (Comma-separated values‏) file with all amplicon sequences. Table has 4 columns:\
              amplicon_name (string) - A unique identifier.\
              amplicon_sequence (4 letter string) - The amplicon reference sequence.\
              sgRNA_sequence (4 letter string) - The sgRNA sequence without the PAM. Should be inside the\
              amplicon_sequence.\
              on_target (Bool) - Indicate if the site is on-targer or off-target.\
              All fields are required. No header should be specified.\
              Please check the README file for further details and examples.")
@click.option('--output', '-o', type=click.Path(), default="CRISPECTOR", show_default=True,
              help="Output folder path (string)")
@click.option('--fastp_options_string', type=click.STRING, default="", help="Try \"fastp --help\" for more details")
@click.option('--override_fastp', is_flag=True, default=False, show_default=True,
              help="Override fastp and require merged fastq files (pre-processing is necessary).\
                    Set paths to merged fastq files at --tx_in1 and --mock_in1.\
                    Can't be used with --fastp_options_string")
# TODO -delete this option
@click.option('--override_alignment', is_flag=True, default=False, show_default=True,
              help="Delete this option. Set paths to alignment fastq files at --tx_in1 and --mock_in1")
@click.option('--verbose', is_flag=True, default=False, show_default=True, help="Higher verbosity")
@click.option('--keep_fastp_output', is_flag=True, default=False, show_default=True, help="Keep fastp output directory")
@click.option("--min_num_of_reads", type=click.INT, default=500, show_default=True,
              help="Minimum number of reads (per site) to evaluate edit events")
@click.option("--cut_site_position", type=click.INT, default=-3, show_default=True,
              help="Cut-site position relative to PAM (minus sign for upstream)")
@click.option("--config", '-c', type=click.Path(),
              help="Path YAML configuration file. See README on GitHub (####) for more details.")
@click.option("--override_binomial_p", is_flag=True, default=False, show_default=True,
              help="Override binomial coin estimation with default value from config file. It's advisable to set"
              "this flag for low number of sites (< ############)") # TODO - fix this option, currently True
@click.option("--confidence_interval", type=click.FloatRange(min=0, max=1), default=0.95, show_default=True,
              help="Confidence interval for the evaluted editing activity")
@click.option('--amplicon_min_alignment_score', type=click.FloatRange(min=0, max=100), default=20, show_default=True,
              help="Minimum alignment score to consider a read alignment to a specific amplicon reference sequence."
                   "Score is normalized between 0 (not even one bp match) to 100 (the read is identical to"
                   "the reference). Below this alignment threshold, reads are discarded."
                   "This is useful for filtering erroneous reads that do not align to any target amplicon.")
def main(tx_in1, tx_in2, mock_in1, mock_in2, output, fastp_options_string, override_fastp, override_alignment,
         keep_fastp_output, verbose, min_num_of_reads, amplicons_csv, cut_site_position, amplicon_min_alignment_score,
         config, override_binomial_p, confidence_interval):
    """CRISPECTOR - Console script"""

    # Input verification
    if override_fastp:
        if (tx_in2 is not None) or (mock_in2 is not None):
            raise click.BadOptionUsage(override_fastp,
                                       "--tx_in2 and --mock_in2 can't be set when override_fastp is used!")
    else:
        if tx_in2 is None:
            raise click.BadOptionUsage(tx_in2, "--tx_in2 is missing!")

        if mock_in2 is None:
            raise click.BadOptionUsage(mock_in2, "--mock_in2 is missing!")

    # Create output folder
    if not os.path.exists(output):
        os.makedirs(output)

    # Run crispector
    return crispector.run(tx_in1, tx_in2, mock_in1, mock_in2, output, amplicons_csv, fastp_options_string,
                          override_fastp, keep_fastp_output, verbose, min_num_of_reads, cut_site_position,
                          amplicon_min_alignment_score, override_alignment, config, override_binomial_p,
                          confidence_interval)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
