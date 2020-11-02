#!/usr/bin/env python

import sys
import csv
import os.path
import string
import os.path

i = sys.argv[2]

counts = []
for x in range(0, 500):
    counts.append(0)

datas = []
filename = sys.argv[1] 
context = sys.argv[3]
with open(filename, 'r') as csvfile:

     spamreader = csv.reader(csvfile, delimiter='\t')
     r = 0
     for row in spamreader:

         beg = str(int(row[1])-5000);
         end = str(int(row[2])+5000);
         met_filename = "met/"+context+"/s"+i+".met_chr"+row[0]+"_"+beg+"_"+end+".gene."+context+".met"
         
         if (os.path.exists(met_filename)) :
             f2 = open(met_filename, 'r')
             data = f2.readlines()
             line = data[0].strip()
             j = 0
             values = []
             for x in line.split(','):
                 if ((x <> "NA") and (x <> "")) :

                     values.append(float(x))

                     counts[j] = counts[j] + 1

                 else :
                     values.append(0)
                 j = j + 1


             datas.append(values)
             r = r + 1

                  

print "position,sum,count,res"

for x in range(0, 500):
    sum = 0
    for y in range(0, r):
        sum = sum + datas[y][x]
    if (counts[x] > 0) :
      res = 100 * sum / counts[x]
      print str(x)+","+str(sum)+","+str(counts[x])+","+str(res)
    else:
      print str(x)+","+str(sum)+","+str(counts[x])+",NA"
