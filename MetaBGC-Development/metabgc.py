import click
from metabgc.src.metabgcbuild import mbgcbuild
from metabgc.src.metabgcidentify import mbgcidentify
from metabgc.src.metabgcquantify import mbgcquantify
from metabgc.src.metabgccluster import mbgccluster

__version__ = "1.2"

@click.group()
def cli():
    pass

@cli.command()
@click.option('--prot_alignment',required=True,
              type=click.Path(exists=True,file_okay=True,readable=True),
              help="Alignment of the protein homologs in FASTA format.")
@click.option('--tp_genes_nucl', required=True,
              type=click.Path(exists=True,file_okay=True,readable=True),
              help="Multi-FASTA with the nucleotide sequence of the true positive genes.")
@click.option('--f1_thresh', required=True,
              type=click.FLOAT, help="F1 score threshold.")
@click.option('--prot_family_name', required=True,
              help="Name of the protein family.")
@click.option('--cohort_name', required=True,
              help="Name of the sample/cohort.")
@click.option('--nucl_seq_directory', required=True,
              type=click.Path(exists=True,dir_okay=True,readable=True),
              help="Directory with synthetic read files of the cohort.")
@click.option('--seq_fmt', required=True,
              type=click.Choice(['fasta', 'fastq'],case_sensitive=False),
              help="Sequence file format and extension.")
@click.option('--pair_fmt', required=True,
              type=click.Choice(['single', 'split', 'interleaved'],case_sensitive=False),
              help="Sequence pair format.")
@click.option('--r1_file_suffix', required=False,
              help="Suffix including extension of the file name specifying R1 reads. Not specified for single or interleaved reads.")
@click.option('--r2_file_suffix', required=False,
              help="Suffix including extension of the file name specifying R2 reads. Not specified for single or interleaved reads.")
@click.option('--output_directory', required=True,
              type=click.Path(exists=True,dir_okay=True,writable=True),
              help="Directory to save results.")
@click.option('--cpu', required=False,
              type=click.INT,default=4,
              help="Number of threads. Def.: 4")
def build(prot_alignment,prot_family_name,cohort_name,
          nucl_seq_directory,seq_fmt,pair_fmt,r1_file_suffix,
          r2_file_suffix,tp_genes_nucl,f1_thresh,
          output_directory,cpu):
    click.echo('Invoking MetaBGC Build...')
    hp_hmm_directory = mbgcbuild(prot_alignment,prot_family_name,cohort_name,
          nucl_seq_directory,seq_fmt,pair_fmt,r1_file_suffix,
          r2_file_suffix,tp_genes_nucl,f1_thresh,
          output_directory,cpu)
    print('High performance SpHMMS saved here: '+hp_hmm_directory)

@cli.command()
@click.option('--sphmm_directory', required=True, help= "High performance spHMM directory generated by Build.")
@click.option('--prot_family_name', required=True,
              help="Name of the protein family.")
@click.option('--cohort_name', required=True,
              help="Name of the sample/cohort.")
@click.option('--nucl_seq_directory', required=True,
              type=click.Path(exists=True,dir_okay=True,readable=True),
              help="Directory with synthetic read files of the cohort.")
@click.option('--seq_fmt', required=True,
              type=click.Choice(['fasta', 'fastq'],case_sensitive=False),
              help="Sequence file format and extension.")
@click.option('--pair_fmt', required=True,
              type=click.Choice(['single', 'split', 'interleaved'],case_sensitive=False),
              help="Sequence pair format.")
@click.option('--r1_file_suffix', required=False,
              help="Suffix including extension of the file name specifying R1 reads. Not specified for single or interleaved reads.")
@click.option('--r2_file_suffix', required=False,
              help="Suffix including extension of the file name specifying R2 reads. Not specified for single or interleaved reads.")
@click.option('--output_directory', required=True,
              type=click.Path(exists=True,dir_okay=True,writable=True),
              help="Directory to save results.")
@click.option('--cpu', required=False,
              type=click.INT,default=4,
              help="Number of threads. Def.: 4")
def identify(sphmm_directory,cohort_name,nucl_seq_directory,
             seq_fmt,pair_fmt,r1_file_suffix,r2_file_suffix,
             prot_family_name,output_directory,cpu):
    click.echo('Invoking MetaBGC Identify...')
    ident_reads_file = mbgcidentify(sphmm_directory, cohort_name, nucl_seq_directory,
                 seq_fmt, pair_fmt, r1_file_suffix, r2_file_suffix,
                 prot_family_name, output_directory, cpu)
    print('Identified reads: ' + ident_reads_file)

@cli.command()
@click.option('--identify_fasta', required=True,
              type=click.Path(exists=True,file_okay=True,readable=True),
              help= "Path to the file produced by MetaBGC-Identify.")
@click.option('--prot_family_name', required=True,
              help="Name of the protein family.")
@click.option('--cohort_name', required=True,
              help="Name of the sample/cohort.")
@click.option('--nucl_seq_directory', required=True,
              type=click.Path(exists=True,dir_okay=True,readable=True),
              help="Directory with synthetic read files of the cohort.")
@click.option('--seq_fmt', required=True,
              type=click.Choice(['fasta', 'fastq'],case_sensitive=False),
              help="Sequence file format and extension.")
@click.option('--pair_fmt', required=True,
              type=click.Choice(['single', 'split', 'interleaved'],case_sensitive=False),
              help="Sequence pair format.")
@click.option('--r1_file_suffix', required=False,
              help="Suffix including extension of the file name specifying R1 reads. Not specified for single or interleaved reads.")
@click.option('--r2_file_suffix', required=False,
              help="Suffix including extension of the file name specifying R2 reads. Not specified for single or interleaved reads.")
@click.option('--output_directory', required=True,
              type=click.Path(exists=True,dir_okay=True,writable=True),
              help="Directory to save results.")
@click.option('--cpu', required=False,
              type=click.INT,default=4,
              help="Number of threads. Def.: 4")
def quantify(identify_fasta,prot_family_name,cohort_name,nucl_seq_directory,
             seq_fmt,pair_fmt,r1_file_suffix,r2_file_suffix,
             output_directory,cpu):
    click.echo('Invoking MetaBGC Quantify...')
    abund_file = mbgcquantify(identify_fasta, prot_family_name, cohort_name, nucl_seq_directory,
             seq_fmt, pair_fmt, r1_file_suffix, r2_file_suffix,
             output_directory, cpu)
    print('Reads abundance file: ' + abund_file)


@cli.command()
@click.option("--table",required=True,type=click.Path(exists=True,file_okay=True,readable=True),
              help="Path of tab-delimited abundance table.")
@click.option("--max_dist", type=float, default=0.1,help="Maximum Pearson distance between two reads to be in the same cluster. Default is 0.1")
@click.option("--min_samples", type=float, default=1,help="Minimum number of samples required for a cluster. " \
                                                          "If min_samples > 1, noise are labelled as -1")
@click.option("--cpu", type=int, default=1,help="Number of threads.")
def cluster(table,max_dist,min_samples,cpu):
    click.echo('Invoking MetaBGC Cluster...')
    cluster_file = mbgccluster(table,max_dist,min_samples,cpu)
    print('Clustered file: ' + cluster_file)


@cli.command()
@click.option('--sphmm_directory', required=True, help= "High performance spHMM directory generated by Build.")
@click.option('--prot_family_name', required=True,
              help="Name of the protein family.")
@click.option('--cohort_name', required=True,
              help="Name of the sample/cohort.")
@click.option('--nucl_seq_directory', required=True,
              type=click.Path(exists=True,dir_okay=True,readable=True),
              help="Directory with synthetic read files of the cohort.")
@click.option('--seq_fmt', required=True,
              type=click.Choice(['fasta', 'fastq'],case_sensitive=False),
              help="Sequence file format and extension.")
@click.option('--pair_fmt', required=True,
              type=click.Choice(['single', 'split', 'interleaved'],case_sensitive=False),
              help="Sequence pair format.")
@click.option('--r1_file_suffix', required=False,
              help="Suffix including extension of the file name specifying R1 reads. Not specified for single or interleaved reads.")
@click.option('--r2_file_suffix', required=False,
              help="Suffix including extension of the file name specifying R2 reads. Not specified for single or interleaved reads.")
@click.option("--max_dist", type=float, default=0.1,help="Maximum Pearson distance between two reads to be in the same cluster. Default is 0.1")
@click.option("--min_samples", type=float, default=1,help="Minimum number of samples required for a cluster. " \
                                                          "If min_samples > 1, noise are labelled as -1")
@click.option('--output_directory', required=True,
              type=click.Path(exists=True,dir_okay=True,writable=True),
              help="Directory to save results.")
@click.option('--cpu', required=False,
              type=click.INT,default=4,
              help="Number of threads. Def.: 4")
def search(sphmm_directory,prot_family_name,cohort_name,
            nucl_seq_directory,seq_fmt,pair_fmt,
            r1_file_suffix,r2_file_suffix,max_dist,
            min_samples,output_directory,cpu):
    click.echo('Invoking MetaBGC search...')
    ident_reads_file = mbgcidentify(sphmm_directory, cohort_name, nucl_seq_directory,
                                    seq_fmt, pair_fmt, r1_file_suffix, r2_file_suffix,
                                    prot_family_name, output_directory, cpu)

    abund_file = mbgcquantify(ident_reads_file, prot_family_name, cohort_name, nucl_seq_directory,
             seq_fmt, pair_fmt, r1_file_suffix, r2_file_suffix,
             output_directory, cpu)

    cluster_file = mbgccluster(abund_file, max_dist, min_samples, cpu)

    print('Clustered file: ' + cluster_file)

if __name__ == '__main__':
    cli()