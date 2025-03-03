#!/usr/bin/env python
"""CleanUp.py

Organize the results for each run of the sppider script.

Method
------
Search for and move all related job files to a sample directory.
    
Parameters
----------
s : str
    sample directory name1

Example
-------
    usage:
           ~/scripts/sppider_condor/CleanUp.py -s yHDO590_kloeckera_taiwanica_180604.haplomerger2

"""
import glob
import os
import re
import sys
import argparse            


def main():
    cmdparser = argparse.ArgumentParser(description="Clean up each run of sppider condor job.", 
                                        usage='%(prog)s -s <Sample Name> ',
                                        prog='sppiderCondor.py'  )    
    cmdparser.add_argument('-s', '--sample', action='store', dest='SAMPLE', 
                           help='Sample directory name.', metavar='')                      
    cmdResults = vars(cmdparser.parse_args())

    # if no args print help
    if len(sys.argv) == 1:
        print("")
        cmdparser.print_help()
        cmdparser.exit(1,"-d <directory name> required" )
    
    # retrieve the directory name
    if cmdResults['SAMPLE'] is not None:
        sampleName = cmdResults['SAMPLE']
    else:
        print("")
        cmdparser.print_help()
        cmdparser.exit(1,"-s <Sample Name> required" )
    
    # create the directory, must not exist 
    if not os.path.exists(sampleName):
        os.mkdir(sampleName)
    else:
        cmdparser.exit(1, f'Error: {sampleName} already exists.\n')

    # move all sample files to sample results directory
    for item in glob.glob(f'*{sampleName}*'):
        if not os.path.isdir(item):
            os.rename(item, sampleName + '/' + item)

    # send log files to sample results directory
    [os.rename(x, sampleName + '/' + x) for x in glob.glob('combine-*.*')]
    [os.rename(x, sampleName + '/' + x) for x in glob.glob('process-*.*')]

    for joblist in glob.glob('job-*-keylist.txt'):
        os.rename(joblist, sampleName + '/' + joblist)
 
if __name__ == "__main__":
    main()