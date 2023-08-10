#!/usr/bin/env python

import bioinfo
import matplotlib.pyplot as plt         #I didn't end up using this one.
import argparse 
import gzip                             #Important b/c these are zipped files!

def get_args():
    parser = argparse.ArgumentParser(description="Demux")
    parser.add_argument("-f1", "--R1_file", help="R1 filename", type=str)
    parser.add_argument("-f2", "--R2_file", help="R2 filename", type=str)
    parser.add_argument("-f3", "--R3_file", help="R3 filename", type=str)
    parser.add_argument("-f4", "--R4_file", help="R4 filename", type=str)
    parser.add_argument("-i", "--indexfile", help="file containing indices", type=str)
    return parser.parse_args()

args=get_args()
R1_read=args.R1_file                    #R1 file
R2_read=args.R2_file                    #R2 file
R3_read=args.R3_file                    #R3 file
R4_read=args.R4_file                    #R4 file
indexname=args.indexfile                #known index text file

rev_dict={"A":"T","T":"A","G":"C","C":"G","N":"N"}      #this is important for the rev_comp function

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

index_set=set()         #initialize an empty dictionary to populate with known indices

with open (indexname,"r") as indices:           #this is where the dictionary gets populated with known indices from text file
    indices.readline()
    for line in indices:
        line=line.split()
        index_set.add(line[4])

# print(index_set)  This correctly tested that I could grab the right set of indices with /projects/bgmp/shared/2017_sequencing/indexes.txt

filehands={}            #I created this to populate it with all the files that I am opening, so I can loop through at the end to close them all at one time.
for ind in index_set:               #This is where I create the files to write to for any matched index pairs
    R1out=open(f'{ind}_R1_out.fq', "w")
    R2out=open(f'{ind}_R2_out.fq',"w")
    filehands[ind]=[R1out, R2out]          

hopR1_out=open("hopped_R1_out.fq","w")
hopR2_out=open("hopped_R2_out.fq","w")
filehands.update({"hop":[hopR1_out,hopR2_out]})     #This is where I create the hopped index files to write to 

unkR1_out=open("unknown_R1_out.fq","w")
unkR2_out=open("unknown_R2_out.fq","w")
filehands.update({"unk":[unkR1_out,unkR2_out]})     #This is where I create the unknown/low-quality index files to write to

def read_rec(fq_filehand) -> list:          #This function is important to be able to read files R1-R4 one record at a time, which I used later in a while true loop
    '''This function can read the first record of the file called with the file handle. It should be used in a while true loop to be able to go through all the records and can be used in conjuntion with other files at the same time by calling them by their file handles'''
    header=fq_filehand.readline().strip()
    seq=fq_filehand.readline().strip()
    plus=fq_filehand.readline().strip()
    quality=fq_filehand.readline().strip()
    return [header,seq,plus,quality]

unk_count=0             #This will count the number of unknown records I wrote out
uniq_matches={}         #This dictionary will be populated with the unique matched index with a value of the number of times of occurence
uniq_hops={}            #This dictionary will be populated with unique hopped index pairs with a frequency of occurence for value
records=0               #This counter is to count the number of records in the files, to calculate percents with later in the user report

with gzip.open(R1_read,"rt") as R1, gzip.open(R2_read,"rt") as R2, gzip.open(R3_read,"rt") as R3, gzip.open(R4_read,"rt") as R4:
    while True:
        recR1=read_rec(R1)
        recR2=read_rec(R2)          #These four lines will grab one record at a time as it loops through 
        recR3=read_rec(R3)
        recR4=read_rec(R4)
        if recR1==["","","",""]:        #This will break out of the loop when it reaches the end of the file and the record is an empty string
            break
        records+=1              #count up for every occurence of record
        index2=rev_comp(recR3[1])       #This is important to reverse complement the Read 2 index (Index 2) so you can compare to index 1
        index1=recR2[1]                 
        if "N" in index1 or "N" in index2:      #filtering out if sequence contains low quality of undetermined base calls "N"
            unkR1_out.write(f'{recR1[0]}\n{index1}-{index2}\n{recR1[2]}\n{recR1[3]}\n')
            unkR2_out.write(f'{recR4[0]}\n{index1}-{index2}\n{recR4[2]}\n{recR4[3]}\n')
            unk_count+=1        
        elif (index1 not in index_set) or (index2 not in index_set):        #further filtering out so you are only left with known indices that are from the indexes.txt
            unkR1_out.write(f'{recR1[0]}\n{index1}-{index2}\n{recR1[2]}\n{recR1[3]}\n')
            unkR2_out.write(f'{recR4[0]}\n{index1}-{index2}\n{recR4[2]}\n{recR4[3]}\n')
            unk_count+=1 
        elif (index1 == index2) and (index1 in index_set):              #this is where I write out the matched index pairs
            filehands[index1][0].write(f'{recR1[0]}\n{index1}-{index2}\n{recR1[2]}\n{recR1[3]}\n')
            filehands[index1][1].write(f'{recR4[0]}\n{index1}-{index2}\n{recR4[2]}\n{recR4[3]}\n')
            if index1 in uniq_matches:          #this is adding the indexes to the dictionary and counting up
                uniq_matches[index1]+=1
            else:
                uniq_matches[index1]=1
        elif (index1 != index2) and (index1 in index_set) and (index2 in index_set):    #this is where I evaluate if the indexes have been hopped and write to the files
            hopR1_out.write(f'{recR1[0]}\n{index1}-{index2}\n{recR1[2]}\n{recR1[3]}\n')
            hopR2_out.write(f'{recR4[0]}\n{index1}-{index2}\n{recR4[2]}\n{recR4[3]}\n')
            if index1+":"+index2 in uniq_hops:          #this is where we count up and add to the dictionary for every index-hopped pair as we come across them
                uniq_hops[index1+":"+index2] += 1
            else:
                uniq_hops[index1+":"+index2]=1
        else:
            raise Exception("impossible")       #this is useful in general to make sure that if any exceptions to the various parameters I specify are encountered it will alert me to that 
        


for files in filehands:     #close all open files not with opened!!
    filehands[files][0].close()
    filehands[files][1].close()

tot_hops = sum(uniq_hops.values())      #total hopped records
tot_match = sum(uniq_matches.values())      #total matched records
perc_unk=float((unk_count/records)*100)     #percent unknown records/low-quality
report=open("user_report.txt","w")          #write out the user report after this point!
report.write(f'User Report Demux\n\n')
report.write(f'Input files:\n{R1_read}\n{R2_read}\n{R3_read}\n{R4_read}\n\n')
report.write(f'Total records per file:  {records}\n\n')         
report.write(f'Number unknown reads:\tPercent of total data:\n{unk_count}\t{round(perc_unk,2)}%\n\n')
report.write(f'Number matched reads:\tPercent of total data:\n{tot_match}\t{round(((tot_match/records)*100),2)}%\n\n')
report.write(f'Number hopped reads:\tPercent of total data:\n{tot_hops}\t{round(((tot_hops/records)*100),2)}%\n\n')
report.write(f'Matched Indices\tNumber of Matches\tPercent of Data\n')

for match in uniq_matches:
    x=uniq_matches[match]
    report.write(f'{match}\t{x}\t{round(((x/records)*100),2)}%\n')

report.write(f'\nHopped Indices\tNumber of Hops\tPercent of Data\n')

for hops in uniq_hops:
    y=uniq_hops[hops]
    report.write(f'{hops}\t{y}\t{round(((y/records)*100),2)}%\n')

report.close()