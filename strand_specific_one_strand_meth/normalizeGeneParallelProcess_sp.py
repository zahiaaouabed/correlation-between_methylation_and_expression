#!/usr/bin/env python

import sys
import csv
import os.path
import multiprocessing as mp
import random
import string



filename = sys.argv[1]
nb_partition = int(sys.argv[2])
tcontext = sys.argv[3]
output_file = sys.argv[4]
subjects_file = sys.argv[5]

f = open(subjects_file, 'r')

subjects = []
for line in f:
    subjects.append(line.strip()),


counts = []
mets = []
mets_combined = []
counts_combined = []
for x in range(0, nb_partition):
       mets_combined.append(0),
       counts_combined.append(0),
       mets.append(0),
       counts.append(0)

def readProfile(i, profile, achr, tss, tts, bin_size, nb_partition) :
    sys.stdout.write(".")
    sys.stdout.flush()
    output_filename = "met/"+tcontext+"/s"+str(i)+".met_chr"+achr+"_"+str(tss)+"_"+str(tts)+".gene."+tcontext+".met"
    print output_filename
    if (os.path.exists(output_filename)) :
        print "already exists";
    else :
        mets = normalize(profile, achr, tss, tts, bin_size, nb_partition)
        f = open(output_filename, 'w')
        for x in range(0, nb_partition):
            f.write(str(mets[x]))
            f.write(",")
        f.close()


def normalize(profile, achr, tss, tts, bin_size, nb_partition) :
    with open(profile, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for row in spamreader:
            if (len(row) >= 8) :
                chr = row[0]
                position = int(row[1])
                strand = row[3]
                if (len(row) < 17) :
                    print row
                    sys.exit()
                context = row[16];
                met = float(row[5]);
                cov = float(row[6]);                   
                for x in range(0, nb_partition):

                    if ((position > tss + 5000 + x * bin_size) and (position < tss + 5000 + (x+1) * bin_size)) :


                        if ((cov >= 3) and (context == tcontext) and (strand == "+")) :
                            counts[x] = counts[x] + 1
                            mets[x] = float(mets[x]) + float(float(met)/cov)
        mean_met = []
        for x in range(0, nb_partition):
            mean_met.append(-1)
        for x in range(0, nb_partition):
            if (counts[x] > 0) :
                mean_met[x] = mets[x]/counts[x]
            else :
                mean_met[x] = "NA"
    return mean_met


all_processes = []
processes = []
with open(filename, 'r') as csvfile:

     spamreader = csv.reader(csvfile, delimiter='\t')
     r = 1
     for row in spamreader:
         size = float(row[2])-float(row[1])
         beg = str(int(row[1])-5000);
         end = str(int(row[2])+5000);
         print "\nRegion #"+str(r)+":"+row[0]+":"+row[1]+"-"+row[2]+"\t"+str(size)+"\n",
         j = 0
         for i in subjects:
             profile = "chr"+row[0]+"/"+tcontext+"/s"+i+".met_chr"+row[0]+"_"+beg+"_"+end+"."+tcontext+".METH.gene5k.profile";
             if (os.path.exists(profile)) :
                  bin_size = (float(row[2])-float(row[1]))/nb_partition
                  print bin_size 
                  t = mp.Process(name = i+"_"+beg+"_"+end+"_"+row[2], target = readProfile, args = (i, profile, row[0], int(beg), int(end), bin_size, nb_partition))
                  processes.append(t)
                  all_processes.append(t)
                  if (len(processes) > 20) :
                     for process in processes:
                         process.start()
                     for process in processes:
                         process.join()
                     processes = []
             else :
                 print "WARNING!!! : "+profile+" has not been found\n";
             j = j + 1
         r = r + 1
         for process in processes:
             process.start()
         for process in processes:
             process.join()
         processes = []
                     



for process in processes:
    print "@"

f = open(output_file, 'w')
for x in range(0, nb_partition):
   if (counts_combined[x] > 0) :
       av = mets_combined[x]/counts_combined[x],
       f.write((str(x)+"\t"+str(mets_combined[x]/counts_combined[x])).strip()+"\n")
   else:
       f.write("NA\t0\n")
f.close()
