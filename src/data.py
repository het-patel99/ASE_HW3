
from typing import List

import os
import csv
import random
import cols
import row
import sys
import data

script_sir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_sir)
os.sys.path.insert(0,parent_dir)
from tests.tests import *

# set to their default values
random_instance = random.Random()
file = '../etc/data/auto93.csv'
seed = 937162211
dump = False

def get_csv_contents(filepath: str) -> list[str]:

    #try to catch relative paths
    if not os.path.isfile(filepath):
        filepath = os.path.join(script_sir, filepath)

    filepath = os.path.abspath(filepath)

    csv_list = []
    with open(filepath, 'r') as csv_file:
        csv_list = list(csv.reader(csv_file, delimiter=','))

    return csv_list


class Data():

    ## constructor created for data.py class
    def __init__(self, src):
        self.rows = []
        self.cols =  None

        ## if the src is string then
        ## it reads the file and then calls the add method to add each row
        src_type = type(src)
        if src_type == str :
            csv_list = get_csv_contents(src)
            for row in csv_list:
                trimmed_row = []
                for item in row:
                    trimmed_row.append(item.strip())
                self.add(trimmed_row)

        elif src_type == List[str]: # else we were passed the columns as a string
            self.add(src)
        else:
            raise Exception("Unsupported type in Data constructor")

    ## add method adds the row read from csv file
    ## It also checks if the col names is being read has already being read or not
    ## if yes then it uses old rows
    ## else add the col rows.
    def add(self, t: list[str]):

        if(self.cols is None):
            self.cols = cols.Cols(t)
        else:
            new_row = row.Rows(t)
            self.rows.append(new_row)
            self.cols.add(new_row)

    def clone(self):
        new_data = Data({self.cols.names})
        for row in self.rows:
            new_data.add(row)
        return new_data



# ------------------- MAIN PROGRAM FLOW -------------------

## run_test counts the number of arguments that have been passed and failed and it also,
## it displays the names tests passed and failed.
def run_tests():
    print("Executing tests...\n")

    passCount = 0
    failCount = 0
    test_suite = [test_csv, test_show_dump, test_syms, test_nums, test_data, test_show_dump] 

    for test in test_suite:
        try:
            test()
            passCount = passCount + 1
        except AssertionError as e:
            failCount = failCount + 1
        

    print("\nPassing: " + str(passCount) + "\nFailing: " + str(failCount))

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

# api-side function to get the current input csv filepath
def get_file() -> str:
    return file

## find_arg_values gets the value of a command line argument
# first it gets set of args
# second it get option A (-h or -d or -s or -f )
# third is get option B (--help or --dump or --seed or --file)
def find_arg_value(args: list[str], optionA: str, optionB: str) -> str:
    index = args.index(optionA) if optionA in args else args.index(optionB)
    if (index + 1) < len(args):
        return args[index + 1]
    return None

help_string = """data.py : an example csv reader script.\n
based on the original script (data.lua) by Tim Menzies <timm@ieee.org>\n
USAGE:   data.lua  [OPTIONS] [-g ACTION]
OPTIONS:
  -d  --dump  on crash, dump stack = false
  -f  --file  name of file         = ../etc/data/auto93.csv
  -g  --go    start-up action      = data
  -h  --help  show help            = false
  -s  --seed  random number seed   = 937162211
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
