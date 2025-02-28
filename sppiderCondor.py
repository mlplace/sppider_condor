#!/usr/bin/env python
"""sppiderCondor.py

Using the docker image for sppIDER run a both the combineRefGenomes.py and
sppIDer.py for a list of Reference genomes and fastq files.

Notes
----- 
Activate the conda environment /home/glbrc.org/mplace/.conda/envs/metagenomics to run this script.

    conda activate /home/glbrc.org/mplace/.conda/envs/metagenomics

Method
------
The list of Reference genome names are the same as the fastq files. 
Here we will leave the actual reference genome of interest out of the combineRefGenomes.py
step comparing it to the other genomes to the fastq files.

For examples given reference genomes A,B,C,D and fastq files A.fastq, B.fastq,
C.fastq, D.fastq

The first job will be

combineRefGenomes.py using B,C,D ref genomes then using A.fastq to run sppIDer.py.
    
Parameters
----------

f : str
    A file containing a list of sample names and full path to sample fastq files, tab delimited.

    yHDO590_kloeckera_taiwanica_180604.haplomerger2  /mnt/bigdata/processed_data/hittinger/y1000_final_files/reads/yHDO590_kloeckera_taiwanica_R1.fastq

r : str
    A file containing a list of genome names and the genome fasta files.

    yHDO590_kloeckera_taiwanica_180604.haplomerger2  /mnt/bigdata/processed_data/hittinger/fungal_genomes/from_vanderbilt/to_uw/y1000_final_files.fixed/genomes/yHDO590_kloeckera_taiwanica_180604.haplomerger2.fas

Example
-------
    usage:

        sppiderCondor.py -f Saccharomycodales_read_paths.txt -r Saccharomycodales_genome_paths.txt

Requirements
------------

    1. pydagman must be in the conda environment.  https://gitpub.wei.wisc.edu/mplace/pydagman

References
----------
 sppIDer: A Species Identification Tool to Investigate Hybrid Genomes with High-Throughput Sequencing,
 Molecular Biology and Evolution, Volume 35, Issue 11, November 2018, Pages 2835–2849, https://doi.org/10.1093/molbev/msy166
 Published: 01 September 2018

 https://github.com/GLBRC/sppIDer/tree/master
"""
import os
import re
import sys
import argparse            

from pydagman.dagfile import Dagfile 
from pydagman.job import Job


def main():
    cmdparser = argparse.ArgumentParser(description="Run sppIDer on a set of genomes and sample fastqs.", 
                                        usage='%(prog)s -f <fastq-list.txt> -r <refgenome-list.txt',
                                        prog='sppiderCondor.py'  )
    cmdparser.add_argument('-f', '--fastqs',    action='store', dest='FASTQS', 
                           help='''Sample Name and fastq file path, tab delimited. (Forward read file)\n
                           Sample Name must match Ref Genome name in ref genome file.''', metavar='')
    cmdparser.add_argument('-r', '--refgenomes', action='store', dest='REF', 
                           help='Ref Genome name and ref file path, tab delimited.', metavar='')
    cmdResults = vars(cmdparser.parse_args())

    # if no args print help
    if len(sys.argv) == 1:
        print("")
        cmdparser.print_help()
        sys.exit(1)

    # dictionary to hold fastq information
    # key = fastq name
    # value = path to fastq file
    fastq = {}
    if cmdResults['FASTQS'] is not None:
        with open(cmdResults['FASTQS'], 'r') as f:
            for ln in f:
                sample, fastqPath = ln.rstrip().split('\t')
                if sample not in fastq:
                    fastq[sample] = fastqPath
                else:
                    print('\nDuplicate sample names not allowed.')
                    print(f'Duplicate sample name : {sample}\n')
                    cmdparser.print_help()
    else:
        cmdparser.print_help()
        cmdparser.exit(1, "Fastq file is missing.")

    # dictionary to hold reference genome information
    # key = sample name, expected to match the name in the fastq file
    # value = path to ref genome
    refs = {}
    if cmdResults['REF'] is not None:
        with open(cmdResults['REF']) as f:
            for ln in f:
                reference, refPath = ln.rstrip().split('\t')
                if reference not in refs:
                    refs[reference] = refPath
                else:
                    print('\nDuplicate reference names not allowed.')
                    print(f'Duplicate reference name : {reference}\n')
                    cmdparser.print_help()
    else:
        cmdparser.print_help()
        cmdparser.exit(1, "Reference genome file is missing.")                
                    
    
       

if __name__ == "__main__":
    main()
