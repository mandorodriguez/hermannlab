#!/usr/bin/env python

import argparse
import os
import sys
import pdb


class GeneConvert:

    def __init__(self,table_file):


        self.human = {}
        self.mouse = {}
        
        lines = None

        with open(table_file,'r') as tf:
            lines = tf.readlines()
            

        for line in lines:
            
            parts = line.split()

            self.human[parts[0]] = (parts[3], parts[1:3])
            self.mouse[parts[3]] = parts[4:]


        pdb.set_trace()

#-------------------------------------------------------------------------------
# Main function call
def __main__():

    parser = argparse.ArgumentParser()
    #parser.add_argument("snp_table", type=str,
    #                    help="The snp table to input")
    parser.add_argument("-t", "--table", type=str,required=True,
                        help="The table with the conversion")

    args = parser.parse_args()


    gc = GeneConvert(args.table)

#-------------------------------------------------------------------------------
if __name__=="__main__": __main__()