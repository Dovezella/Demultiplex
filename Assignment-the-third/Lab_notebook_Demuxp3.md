Lab notebook   
Dove Enicks
Assignment the Third:  Demultiplexing
Bi622

In order to demultiplex the fastq files we were given, I first created a python script, tested it, and then created a slurm script to submit as an sbatch on talapas for the final files. 

The python script is called:  Demux.py 
which is located on talapas:  /projects/bgmp/dovee/bioinfo/Bi622/Demultiplex/Assignment-the-third/
or on my computer:  /home/dovee/bioinfo/Bi622/Demultiplex/Assignment-the-third/

The environment I used was bgmp_py311 with python version 3.11.4

The slurm script is called:  Demultiplex.sh
and located in the same folders.

After testing the python script on my test files, which I had created for Assignment-the-First located under the Demultiplex folder, which are: named Test_R1.fq.gz for R1-R4, and correspond to 6 output test files named *_outtest.fq
I had found my script to work as I wanted. 

*NOTE, create a new folder each time you want to run this program so that you can have all the output files in the proper file structure. Run the program from that folder. I named my Test_out_Demux.

To then run on the actual files for the assignment, I called them with my Demultiplex.sh script from a new folder called Answers_Output. 
The final job id is 26426, with .err named as demux_26426.err or .out with an exit status of 0 and
	Percent of CPU this job got: 73%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 1:07:55

This was after a few different runs just to make sure that the automatically generated user report from the Demux.py script output in a way that I preferred. 

All done :)