#!/usr/bin/env python

import argparse
import os
import sys
import pdb

#-------------------------------------------------------------------------------

class HiSeqData:

    def __init__(self, hiseq_file,column_prefix):

        self.data = {}

        with open(hiseq_file,'r') as hsf:
            
            lines = hsf.readlines()

            self.header = [column_id.lstrip(column_prefix) for column_id in lines[0].split()[1:]]
            
            for line in lines[1:]:
            
                parts = line.split()

                #self.data[parts[0]] = parts[1:]

                row = {}
                           
                # putting this into a row that's keyed to the header ids
                for i,v in enumerate(parts[1:]):

                    row[self.header[i]] = v

                    
                self.data[parts[0]] = row


                pdb.set_trace()

#-------------------------------------------------------------------------------
# Main function call
def __main__():

    parser = argparse.ArgumentParser()
    #parser.add_argument("snp_table", type=str,
    #                    help="The snp table to input")
    parser.add_argument("-t", "--table", type=str,required=True,
                        help="The table with the conversion")
    parser.add_argument("-u", "--human", type=str,required=True,
                        help="Human hiseq data")
    parser.add_argument("-m", "--mouse", type=str,required=True,
                        help="Mouse hiseq data")

    args = parser.parse_args()


    table_file = args.table
    mouse_file = args.mouse
    human_file = args.human
    
    human = {}
    mouse = {}
        
    lines = None

    with open(table_file,'r') as tf:
        lines = tf.readlines()
            

        for line in lines:
            
            parts = line.split()

            human[parts[0]] = (parts[3], parts[1:3])
            mouse[parts[3]] = parts[4:]


    hiseq_mouse = HiSeqData(mouse_file,"Id4GFP-Seq1_")
    hiseq_human = HiSeqData(human_file,"HsSgSeq1-")
    
#-------------------------------------------------------------------------------
if __name__=="__main__": __main__()
