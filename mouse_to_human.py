#!/usr/bin/env python

import argparse
import os
import sys
import pdb

#-------------------------------------------------------------------------------

class HiSeqData:

    def __init__(self, hiseq_file):

        self.data = {}

        with open(hiseq_file,'r') as hsf:
            
            lines = hsf.readlines()

            self.header = [column_id.lstrip().rstrip() for column_id in lines[0].split()[1:]]

            for line in lines[1:]:
            
                cels = line.split()
                    
                self.data[cels[0]] = cels[1:]




#-------------------------------------------------------------------------------
# Main function call
def __main__():

    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--table", type=str,required=True,
                        help="The table with the conversion")
    parser.add_argument("-u", "--human", type=str,required=True,
                        help="Human hiseq data")
    parser.add_argument("-m", "--mouse", type=str,required=True,
                        help="Mouse hiseq data")
    parser.add_argument("-o", "--out", type=str,default="mouse_and_human.txt",
                        help="output file")
    

    args = parser.parse_args()


    table_file = args.table
    mouse_file = args.mouse
    human_file = args.human
    outfile = args.out
    
    human_to_mouse = {}
    mouse_to_human = {}
        
    lines = None

    with open(table_file,'r') as tf:
        lines = tf.readlines()
            

        for line in lines:
            
            parts = line.split()

            human_to_mouse[parts[0]] = parts[3] # only going to go human -> mouse
            mouse_to_human[parts[3]] = parts[0]


    hiseq_mouse = HiSeqData(mouse_file)
    hiseq_human = HiSeqData(human_file)

    
    new_table = []
    mouse_exclusive = []
    human_exclusive = []

    for human_id in hiseq_human.data.keys():

        try:
            mouse_id = human_to_mouse[human_id]
        except KeyError:
            # here i collect those human ids without a mouse counterpart
            print "No mouse id for %s" % human_id
            continue

        mrow = []
        hrow = []
        
        try:
            mrow = hiseq_mouse.data[mouse_id]
        except KeyError:
            human_exclusive.append([human_id]+hiseq_human.data[human_id])
            print "No mouse data for %s and human id %s" % (mouse_id,human_id)


        hrow = hiseq_human.data[human_id] # should never happen be missing


        if len(hrow) == 0 or len(mrow) == 0:
            continue
        
        new_row = [human_id, mouse_id] + hrow + mrow
        

        new_table.append(new_row)

    #---------------------------------------------------------------------------
    for mouse_id in hiseq_mouse.data.keys():
        try:
            mouse_to_human[mouse_id]
        except KeyError:
            mouse_exclusive.append([mouse_id]+hiseq_mouse.data[mouse_id])


    #--- done getting stuff ----------------------------------------------------

    print "Writing output file to %s" % outfile
    
    with open(outfile,'w') as of:

        of.write("\t".join(["human_tracking_id","mouse_tracking_id"]+hiseq_human.header+hiseq_mouse.header)+"\n")

        for row in new_table:

            of.write("\t".join(row)+"\n")

    with open("mouse_exclusive.txt",'w') as of:

        of.write("\t".join(["tracking_Id"]+hiseq_mouse.header)+"\n")

        for row in mouse_exclusive:

            of.write("\t".join(row)+"\n")


    with open("human_exclusive.txt",'w') as of:

        of.write("\t".join(["tracking_Id"]+hiseq_human.header)+"\n")

        for row in human_exclusive:

            of.write("\t".join(row)+"\n")


    print "Done!"
    
#-------------------------------------------------------------------------------
if __name__=="__main__": __main__()
