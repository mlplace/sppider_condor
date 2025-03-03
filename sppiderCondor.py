#!/usr/bin/env python
"""sppiderCondor.py

Using the docker image for sppIDER run a both the combineRefGenomes.py and
sppIDer.py for a list of Reference genomes and fastq files.

Notes
----- 
Activate conda environment to run this script.

    conda activate /home/glbrc.org/mplace/miniforge3

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
    
    after running the script you should see:

    Ready to submit:
    enter: condor_submit_dag MasterDagman.dsf

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

def process_Submit():
    """process_Submit
    
    Create a generic sppIDer.py submit file.
    """
    with open('sppider-process.submit', 'w') as out:
        out.write('docker_image = glbrc/sppider\n')
        out.write('\n')
        out.write('# Enable custom docker scratch dir /tmp/sppIDer/working\n')
        out.write('# The published docker image is hard coded to use this path\n')
        out.write('+DockerSppIDerScratchMount=True\n')
        out.write('\n')
        out.write('# sppIDer.py\n')
        out.write('# --out Output prefix for files, required -  Written to /tmp/sppIDer/working\n')
        out.write('# --ref Combined Reference Genome, required\n')
        out.write('# --r1 Read1, required\n')
        out.write('# --r2 Read2, optional\n')
        out.write("# --byBP Calculate coverage by basepair, optional, DEFAULT, can't be used with -byGroup\n")
        out.write("# --byGroup   Calculate coverage by chunks of same coverage, optional, can't be used with -byBP\n")
        out.write('arguments = /tmp/sppIDer/sppIDer.py  --out $(out)  --ref $(ref)  --r1 $(read) --byGroup \n')
        out.write('\n')
        out.write('# Collect data written to the custom docker scratch dir\n')
        out.write('should_transfer_files = YES\n')
        out.write('when_to_transfer_output = ON_EXIT\n')
        out.write('transfer_output_files = tmp/sppIDer/working/\n')
        out.write('\n')
        out.write('output = process-$(sample)-out.txt\n')
        out.write('error = process-$(sample).err\n')
        out.write('log = process-$(sample).log\n')
        out.write('\n')
        out.write('request_cpus = 2\n')
        out.write('request_memory = 256GB\n')
        out.write('\n')
        out.write('queue\n')
    out.close()


def combine_Submit():
    """combine_Submit

    Create a generic combineRefGenomes.py submit file.    
    """
    with open('sppider-combine.submit','w') as out:
        out.write('docker_image = glbrc/sppider\n')
        out.write('\n')
        out.write('# Enable custom docker scratch dir /tmp/sppIDer/working\n')
        out.write('# The published docker image is hard coded to use this path\n')
        out.write('+DockerSppIDerScratchMount=True\n')
        out.write('\n')
        out.write('# The docker image entrypoint is "/usr/bin/python2.7"\n')
        out.write('# for interactive job testing, set "docker_override_entrypoint = True"\n')
        out.write('# docker_override_entrypoint = True\n')
        out.write('# executable = /bin/sh\n')
        out.write('\n')
        out.write('# sppIDer scripts are in the image under /tmp/sppIDer/\n')
        out.write('\n')
        out.write('# combineRefGenomes.py\n')
        out.write('# --out Output prefix for combined genome files. Written to /tmp/sppIDer/working/\n')
        out.write("# --key list of genome names and filepaths. Expected in '/tmp/sppIDer/working' + args.key\n")
        out.write('arguments = /tmp/sppIDer/combineRefGenomes.py')
        out.write(' --out $(out)')
        out.write('	--key ../../../$(refKey)\n')
        out.write('\n')
        out.write("# It's not convenient, but chaining parent directory navigation allows accessing shared filesystem paths, instead of hard coded paths\n")
        out.write('# make sure the keyfile contents use the same pathing:\n')
        out.write('# Smik	/mnt/bigdata/processed_data/data_ops/examples/sppider/set1/fasta/Smik.concat.fasta\n')
        out.write('\n')
        out.write('# Collect data written to the custom docker scratch dir\n')
        out.write('should_transfer_files = YES\n')
        out.write('when_to_transfer_output = ON_EXIT\n')
        out.write('transfer_output_files = tmp/sppIDer/working/\n')
        out.write('\n')
        out.write('output = combine-$(sample)-out.txt\n')
        out.write('error = combine-$(sample).err\n')
        out.write('log = combine-$(sample).log\n')
        out.write('\n')
        out.write('request_cpus = 2\n')
        out.write('request_memory = 16GB\n')
        out.write('queue\n')
    out.close()

def cleanUpSubmitFile():
    """cleanUpSubmitFile

    Create a submit file to run the cleanup script.        
    """
    with open('cleanup.submit', 'w') as submit:
        submit.write("Universe                 = vanilla\n")
        submit.write("Executable               = run_cleanup.sh\n")
        submit.write("Arguments                = $(sample)\n")
        submit.write("Getenv                   = True\n") 
        submit.write("Error                    = cleanup.submit.err\n")
        submit.write("Queue\n")                 
    submit.close()        

def cleanUpShellScript():
    """cleanUpShellScript
    Write bash script to call CleanUp.py.
    """
    with open('run_cleanup.sh', 'w') as out:
        out.write("#!/bin/bash\n")                                             # set shell
        out.write("source /opt/bifxapps/miniconda3/etc/profile.d/conda.sh\n")  # add conda to path
        out.write("unset $PYTHONPATH\n")                                       # remove default PYTHONPATH         
        out.write(f"conda activate /home/glbrc.org/mplace/miniforge3\n")       # start up environment 
        out.write("/home/glbrc.org/mplace/scripts/sppider_condor/CleanUp.py -s $1\n") 
        out.write("conda deactivate\n")
    out.close()

    os.chmod('run_cleanup.sh', 0o0777)                                   # change file permissions to run

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
                    cmdparser.exit(1)
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
                    cmdparser.exit(1)
    else:
        cmdparser.print_help()
        cmdparser.exit(1, "Reference genome file is missing.")       

    # create submit files for the dagman
    combine_Submit()
    process_Submit()
    cleanUpSubmitFile()
    cleanUpShellScript()

    mydag = Dagfile()        # set up dagman
    num = 1                  # for job steps
    currDir = os.getcwd() + '/'
    # create the sets to run
    for sample in fastq.keys():
        print(f'Setting up job for {sample}')
        prefix = "ref_" + sample + '.fasta'
        refSet = set(refs.keys())   # get a set of all reference names
        refSet.discard(sample)      # remove the fastq name 
        keyFile = 'job-' + sample + '-keylist.txt'
        with open(keyFile, 'w') as out:
            for r in refSet:
                if r in refs:
                    outLine = f'{r}\t{refs[r]}\n'
                    out.write(outLine)
        
        combineJob = Job('sppider-combine.submit', 'job' + str(num))
        combineJob.pre_skip(1)
        combineJob.add_var('out', prefix)
        combineJob.add_var('refKey', currDir + keyFile)
        combineJob.add_var('sample', sample)
        mydag.add_job(combineJob)    
        num += 1

        processJob = Job('sppider-process.submit', 'job' + str(num))
        processJob.pre_skip(1)
        processJob.add_var('out', 'process-' + sample + 'out')
        processJob.add_var('ref', currDir + prefix)
        processJob.add_var('read', fastq[sample])
        processJob.add_var('sample', sample)
        processJob.add_parent(combineJob)
        mydag.add_job(processJob)
        num += 1

        cleanJob = Job('cleanup.submit', 'job' + str(num))
        cleanJob.pre_skip(1)
        cleanJob.add_var('sample', sample)
        cleanJob.add_parent(processJob)
        mydag.add_job(cleanJob)
        num += 1

    mydag.save('MasterDagman.dsf')
    
    print('Ready to submit:')
    print('enter: condor_submit_dag MasterDagman.dsf ')

if __name__ == "__main__":
    main()
