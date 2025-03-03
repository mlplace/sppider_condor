#!/usr/bin/env python
"""CleanUp.py

Organize the results for each run of the sppider script.


Method
------

    
Parameters
----------


Example
-------
    usage:

        

"""
import os
import re
import sys
import argparse            





def main():
    cmdparser = argparse.ArgumentParser(description="Clean up each run of sppider condor job.", 
                                        usage='%(prog)s -d <Directory Name> ',
                                        prog='sppiderCondor.py'  )    

    cmdparser.add_argument('-d', '--directory', action='store', dest='DIR', 
                           help='Sample directory name.', metavar='')                       
    cmdResults = vars(cmdparser.parse_args())

    # if no args print help
    if len(sys.argv) == 1:
        print("")
        cmdparser.print_help()
        cmdparser.exit(1,"-d <directory name> required" )
    
    if cmdResults['DIR'] is not None:
        sampleDir = cmdResults['DIR']
        print(sampleDir)
    else:
        print("")
        cmdparser.print_help()
        cmdparser.exit(1,"-d <directory name> required" )


    


     
    
       

if __name__ == "__main__":
    main()
