#!/usr/bin/env python

import bioinfo
import matplotlib.pyplot as plt
import argparse 
import gzip

def get_args():
    parser = argparse.ArgumentParser(description="A program for PS6")
    parser.add_argument("-f", "--filename", help="filename", required=True, type=str)
    parser.add_argument("-o", "--outfile", help="output file name", type=str)
    parser.add_argument("-bp", "--basepairlen", help="lenght of sequence for file", required=True, type= int)
    return parser.parse_args()

args=get_args()
filename=args.filename
outfile=args.outfile
bp=args.basepairlen

bplist=bp
def init_list(lst: list, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with 101 values of 0.0.'''
    i=0
    while i<=bplist:
        lst.append(value)
        i+=1
    return lst

my_list: list = []
my_list = init_list(my_list)

def populate_list(file: str) -> tuple[list, int]:
    """This will populate a list based off of the file chosen to go through and take the quality score of each base in the sequence for every record and return a list that has the sum of those values and the total lines in the file"""
    # my_list: list = []
    # my_list = init_list(my_list)  this is defined outside the function already
    i=0
    with gzip.open(file, "rt") as fh:        #this is basically python version of zcat, rt species to read as a text file (w/o rt binary is assumed)
        for line in fh:
            line= line.strip()
            i+=1
            if i%4 == 0:
                j=0
                for letter in line:
                    qscore=bioinfo.convert_phred(letter)
                    my_list[j]+=qscore
                    j+=1
    return(my_list, i)

my_list, num_lines = populate_list(filename)

for i, summedq in enumerate(my_list):
    meanq=summedq/(num_lines/4)
    my_list[i]=meanq

plt.plot(my_list)
plt.ylabel("Mean Q-score per position in sequence")
plt.ylim(0, 45)
plt.xlabel("Position in sequence")
plt.title("Mean Quality Score")
plt.savefig(f'{outfile}.png')