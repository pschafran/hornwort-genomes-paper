#! /usr/bin/env python
import sys

def pyTable(list):
    dict = {}
    for i in list:
        i = i.strip("\n")
        try:
            dict[i] += 1
        except:
            dict.update({i : int(1)})
    return(dict)

with open(sys.argv[1], "r") as infile:
    table = pyTable(infile)
    for key in table:
        print("%s\t%d" %(key,table[key]))
