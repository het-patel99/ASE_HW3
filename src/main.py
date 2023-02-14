from typing import List
import os
import random
import sys
import data
from tests import tests
import traceback

script_sir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_sir)
os.sys.path.insert(0,parent_dir)

# set to their default values
random_instance = random.Random()
file = '../etc/data/auto93.csv'
seed = 937162211
dump = False
min = 0.5
p = 2
Sample = 512
help = False
Far = 0.95

# ------------------- MAIN PROGRAM FLOW -------------------

## run_test counts the number of arguments that have been passed and failed and it also,
## it displays the names tests passed and failed.
def run_tests():
    print("Executing tests...\n")

    passCount = 0
    failCount = 0
    test_suite = [tests.test_data, tests.test_syms, tests.test_nums, tests.test_the, tests.test_clone, tests.test_around, tests.test_half, tests.test_cluster, tests.test_optimize] 
    
    for test in test_suite:
        try:
            test()
            passCount = passCount + 1
        except AssertionError as e:
            failCount = failCount + 1
    print("\nPassing: " + str(passCount) + "\nFailing: " + str(failCount))
    
# api-side function to get the current input csv filepath
def get_file() -> str:
    return file

# uses the value of the dump parameter and passed exception to determine what message to display to the user
def get_crashing_behavior_message(e: Exception):
    crash_message = str(e)
    if(dump):
        crash_message = crash_message + '\n'
        stack = traceback.extract_stack().format()
        for item in stack:
            crash_message = crash_message + item

    return crash_message

# api-side function to get the current seed value
def get_seed() -> int:
    return seed

# api-side function to get the current dump boolean status
def should_dump() -> bool:
    return dump



## find_arg_values gets the value of a command line argument
# first it gets set of args
# second it get option A (-h or -d or -s or -f )
# third is get option B (--help or --dump or --seed or --file)
def find_arg_value(args, optionA: str, optionB: str) -> str:
    index = args.index(optionA) if optionA in args else args.index(optionB)
    if (index + 1) < len(args):
        return args[index + 1]
    return None

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

if __name__ == "__main__":
    args = sys.argv
    try:
        if '-h' in args or '--help' in args:
            print(help_string)

        if '-d' in args or '--dump' in args:
            dump = True

        if '-f' in args or '--file' in args:
            file = data.data(find_arg_value(args, '-f', '--file'))

        if '-s' in args or '--seed' in args:
            seed_value = find_arg_value(args, '-s', '--seed')
            if seed_value is not None:
                try:
                    seed = int(seed_value)
                except ValueError:
                    raise ValueError("Seed value must be an integer!")
            else:
                print("USAGE: Provide an integer value following an -s or --seed argument to set the seed value.\n Example: (-s 3030, --seed 3030)")

        # NOTE: the seed will be set in main, the rest of the application need not set it
        random_instance.seed(seed)
        if '-g' in args or '--go' in args:
            run_tests()
    except Exception as e:
        print(get_crashing_behavior_message(e))