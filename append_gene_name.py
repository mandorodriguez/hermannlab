#!/usr/bin/env python

import argparse
import os
import sys
import pdb






#-------------------------------------------------------------------------------
# Main function call
def __main__():

    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--table", type=str,required=True,
                        help="The table gene name conversion")
    parser.add_argument("-e", "--ensgene", type=str,required=True,
                        help="Ensegene IDs")
    parser.add_argument("-o", "--out", type=str,default="table.txt",
                        help="output file")
    

    args = parser.parse_args()


    table_file = args.table
    ensgene_file = args.ensgene
    outfile = args.out
    
    ensgene = {}
    gene_name = {}
        
    lines = None

    with open(table_file,'r') as tf:
        lines = tf.readlines()
            
        for line in lines:
            
            parts = line.split()

            gene_name[ parts[0] ] = parts[1]



    #---------------------------------------------------------------------------

    new_ensgene = []

    with open(ensgene_file,'r') as ef:
        lines = ef.readlines()

        for line in lines:
            
            parts = line.split()

            if parts[0] == "tracking_id":

                parts.append("gene_name")

            else:

                # check for the gene name in the ensign ids
                if gene_name.has_key(parts[0]):

                    parts.append( gene_name[parts[0]] )

                else:

                    parts.append("")

            new_ensgene.append(parts)
            


    #--- done getting stuff ----------------------------------------------------

    print "Writing %d lines to output file %s" % (len(new_ensgene),outfile)
    
    with open(outfile,'w') as of:

        for row in new_ensgene:

            of.write("\t".join(row)+"\n")



    print "Done!"
    
#-------------------------------------------------------------------------------
if __name__=="__main__": __main__()
