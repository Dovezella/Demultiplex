Dove Enicks
Bi622- Demultiplexing Report

So after completing this assignment, here are some thoughts about the data and the process:
- I chose to filter index quality scores just based on whether or not there was an N in the sequence
  - On one hand, this was a good thing to be able to filter out those reads which had unknown base calls meaning we don't know what index they would be
  - On the other, you could do a little more coding to try and see if despite an N or two, maybe you can see if it is a known index just with a bad base call
    - In the future, it might behoove me to attempt this so as not to lose a lot of data and confidence in a realignment. It could also be more informative to have more reads to evaluate for mutations or other specifics about the alignment and samples
    - I could also re-code to be able to include a cutoff score if I ever needed to filter out calls less than a certain value. Since N has a quality of 2, it would technically be built in.

For example, 8.47% of unknown reads out of all records is about ~30,500,000 reads in which a large number could have useful information if there were records that might've been known but contained some "N" base calls.
This would mean that there is a higher level of unknown indexes than there might truly be, which would be something to improve in the code. Otherwise unknown indexes would indicate mistakes in sequencing.
Hopefully with the massive amount of reads, even the smallest percentage of matched reads would hopefully have enough coverage of reads for downstream purposes.
For example, for index TCGGATTC with 1.27% of the data yielding 4,611,350 would be a good amount of data to compare to a known reference, but maybe not enough for more specific purposes like looking at rare mutations.

Thankfully, the index-hopping from these sequences were only 0.19% of the total data which adds to the error rate, but it is not too much, only around 700,000 reads across all samples.
