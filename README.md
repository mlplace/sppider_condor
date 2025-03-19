## Name 
sppiderCondor.py

## Description
Using the docker image for sppIDER run a both the combineRefGenomes.py and
sppIDer.py for a list of Reference genomes and fastq files.

The list of Reference genome names are the same as the fastq files. 
Here we will leave the actual reference genome of interest out of the combineRefGenomes.py
step comparing it to the other genomes to the fastq files.

For examples given reference genomes A,B,C,D and fastq files A.fastq, B.fastq,
C.fastq, D.fastq

The first job will be

combineRefGenomes.py using B,C,D ref genomes then using A.fastq to run sppIDer.py.

## Usage

Login into scarcity-submit.glbrc.org (Do not start a condor interactive job, you must be on the submit node.)

Navigate to your job directory, I recommend a "clean" directory just for running this job.

Activate this conda environment:

      conda activate  /home/glbrc.org/mplace/miniforge3

Input file format.

1) Genome Paths file, 2 columns , no header, tab delimited, each sample on a single line.

    Name   path (including ../../../ as a prefix) looks like:

    yHDO590_kloeckera_taiwanica_180604.haplomerger2 ../../../mnt/bigdata/processed_data/hittinger/fungal_genomes/from_vanderbilt/to_uw/y1000_final_files.fixed/genomes/yHDO590_kloeckera_taiwanica_180604.haplomerger2.fas
    

2) Read Paths file, 2 columns, no header, tab delimited,  each sample on a single line.

    Name Path, looks like: 

    yHDO590_kloeckera_taiwanica_180604.haplomerger2 /mnt/bigdata/processed_data/hittinger/y1000_final_files/reads/yHDO590_kloeckera_taiwanica_R1.fastq

Now run the job setup script:

 /home/glbrc.org/mplace/scripts/sppider_condor/sppiderCondor.py -f read_paths.txt -r genome_paths.txt -m 128

Screen output will show the jobs being setup, something like this: 


Setting up job for yHDO590_kloeckera_taiwanica_180604.haplomerger2
Setting up job for yHMPu5000026147_hanseniaspora_vineae_190924.haplomerger2

and at the end of the job list you will see:

Ready to submit:
enter: condor_submit_dag MasterDagman.dsf

using the terminal enter:  condor_submit_dag MasterDagman.dsf 

Check the inital job submission status:

condor_q 

This will show something like the following:

-- Schedd: scarcity-ap-1.glbrc.org : <144.92.98.163:9618?... @ 03/10/25 09:50:10
OWNER  BATCH_NAME                SUBMITTED   DONE   RUN    IDLE  TOTAL JOB_IDS
mplace MasterDagman.dsf+98363   3/10 09:49      _      _      8     66 98395.0 ... 98415.0

Then once the cluster starts picking up jobs it will show jobs running:

-- Schedd: scarcity-ap-1.glbrc.org : <144.92.98.163:9618?... @ 03/10/25 09:50:56
OWNER  BATCH_NAME                SUBMITTED   DONE   RUN    IDLE  TOTAL JOB_IDS
mplace MasterDagman.dsf+98363   3/10 09:49      _     22      _     66 98395.0 ... 98506.0

To see an example run on scarcity :

/home/glbrc.org/mplace/projects/sppider_condor

## Input

f : str
    A file containing a list of sample names and full path to sample fastq files, tab delimited, one sample per line.

    yHDO590_kloeckera_taiwanica_180604.haplomerger2  /mnt/bigdata/processed_data/hittinger/y1000_final_files/reads/yHDO590_kloeckera_taiwanica_R1.fastq

m : int
    Memory (RAM) in GB request for job, defaults to 64GB.

r : str
    A file containing a list of genome names and the genome fasta files, one sample per line.

    yHDO590_kloeckera_taiwanica_180604.haplomerger2  /mnt/bigdata/processed_data/hittinger/fungal_genomes/from_vanderbilt/to_uw/y1000_final_files.fixed/genomes/yHDO590_kloeckera_taiwanica_180604.haplomerger2.fas


## Requirements
python package shortuuid is required.  If you want to create your own environment install is using: 
 
 conda install conda-forge::shortuuid

Tested with Python 3.12.8.

## Support
Please address questions to compbio@glbrc.wisc.edu.

## Authors and acknowledgment
Linda Horianopoulos, Devlyn Zeng, Emily Ubbelohde, Nick Thrower

## License
Copyright 2024 Michael Place

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Project status
Currently under development.
