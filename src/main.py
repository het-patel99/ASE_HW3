import sys, getopt
from tests import *
from pathlib import Path

def run_tests():
    print("Executing tests...\n")

    passCount = 0
    failCount = 0
    test_suite = [test_data, test_syms, test_nums, test_the, test_clone, test_around,test_half, test_cluster, test_optimize] 
    
    for test in test_suite:
        try:
            test()
            passCount = passCount + 1
        except AssertionError as e:
            failCount = failCount + 1
    print("\nPassing: " + str(passCount) + "\nFailing: " + str(failCount))

argumentList = sys.argv[1:]
b4={}
ENV = {}
for k,v in ENV:
    b4[k]=v

options = "hg"
long_options = []
the = {"seed": 937162211, "dump": False, "go": "data", "help": False, "min" : 0.5, "p" : 2, "Sample" : 512, "Far" : 0.95}
    
def help():
    help_string = """cluster.lua : an example csv reader script
    (c)2022, Tim Menzies <timm@ieee.org>, BSD-2 

    USAGE: cluster.lua  [OPTIONS] [-g ACTION]

    OPTIONS:
    -d  --dump    on crash, dump stack   = false
    -f  --file    name of file           = ../etc/data/auto93.csv
    -F  --Far     distance to "faraway"  = .95
    -g  --go      start-up action        = data
    -h  --help    show help              = false
    -m  --min     stop clusters at N^min = .5
    -p  --p       distance coefficient   = 2
    -s  --seed    random number seed     = 937162211
    -S  --Sample  sampling data size     = 512

    ]]"""

def main():
    try:    
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        # checking each argument
        for currentArgument, currentValue in arguments:
             if currentArgument in ('-h', ''):
                 help()
             if currentArgument in ("-g", ''):
                run_tests()
                
    except getopt.error as err:
        print (str(err))

if __name__ == "__main__":
    main()