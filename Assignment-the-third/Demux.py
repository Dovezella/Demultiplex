#!/usr/bin/env python

import bioinfo
import matplotlib.pyplot as plt
import argparse 
import gzip

def get_args():
    parser = argparse.ArgumentParser(description="Demux")
    parser.add_argument("-f1", "--R1_file", help="R1 filename", type=str)
    parser.add_argument("-f2", "--R2_file", help="R2 filename", type=str)
    parser.add_argument("-f3", "--R3_file", help="R3 filename", type=str)
    parser.add_argument("-f4", "--R4_file", help="R4 filename", type=str)
    parser.add_argument("-i", "--indexfile", help="file containing indices", type=str)
    return parser.parse_args()

args=get_args()
R1_read=args.R1_file
R2_read=args.R2_file
R3_read=args.R3_file
R4_read=args.R4_file
indexname=args.indexfile

rev_dict={"A":"T","T":"A","G":"C","C":"G","N":"N"}

def rev_comp(seq: str) -> str:
    '''This function will take a sequence and return the reverse complement of that sequence'''
    assert bioinfo.validate_base_seq(seq)
    seq=seq[::-1]
    rev=""
    for i in seq:
        rev += rev_dict[i]
    return rev

# a="AACCTTGG"
# print(rev_comp(a))   These correctly tested my new function yay!

index_set=set()

with open (indexname,"r") as indices:
    indices.readline()
    for line in indices:
        line=line.split()
        index_set.add(line[4])

# print(index_set)  This correctly tested that I could grab the right set of indices with /projects/bgmp/shared/2017_sequencing/indexes.txt

filehands=set()
for ind in index_set:
    R1out=open(f'{ind}_R1_out.fq', "w")
    R2out=open(f'{ind}_R2_out.fq',"w")
    filehands.add(R1out)
    # filehands(ind)=R1out          make a dictionary to be able to write out to the appropriate files USE A LIST
    filehands.add(R2out)


hopR1_out=open("hopped_R1_out.fq","w")
filehands.add(hopR1_out)
hopR2_out=open("hopped_R2_out.fq","w")
filehands.add(hopR2_out)
unkR1_out=open("unknown_R1_out.fq","w")
filehands.add(unkR1_out)
unkR2_out=open("unknown_R2_out.fq","w")
filehands.add(unkR2_out)

# rec1,rec2,rec3,rec4=["","","",""],["","","",""],["","","",""],["","","",""]  This is cute, remember for future uses

def read_rec(fq_filehand) -> list:
    '''This function can read the first record of the file called with the file handle. It should be used in a while true loop to be able to go through all the records and can be used in conjuntion with other files at the same time by calling them by their file handles'''
    header=fq_filehand.readline().strip()
    seq=fq_filehand.readline().strip()
    plus=fq_filehand.readline().strip()
    quality=fq_filehand.readline().strip()
    return [header,seq,plus,quality]

unk_count=0

with gzip.open(R1_read,"rt") as R1, gzip.open(R2_read,"rt") as R2, gzip.open(R3_read,"rt") as R3, gzip.open(R4_read,"rt") as R4:
    while True:
        recR1=read_rec(R1_read)
        recR2=read_rec(R2_read)
        recR3=read_rec(R3_read)
        recR4=read_rec(R4_read)
        index2=rev_comp(recR3[1])
        index1=rec2[1]
        if "N" in index1 or "N" in index2:
            unkR1_out.write(f'{recR1[0]}\n{index1}-{index2}\n{recR1[2]}\n{recR1[3]}\n')
            unkR2_out.write(f'{recR4[0]}\n{index1}-{index2}\n{recR4[2]}\n{recR4[3]}\n')
            unk_count+=1        
        if index1 == index2:













