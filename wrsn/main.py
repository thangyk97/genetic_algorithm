import numpy as np
import os
import sys, getopt
from utils import read_data_wrsn, calculate_distances, get_max_needed_energy, decode
from wrsn import WRSN

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o")
   except getopt.GetoptError:
      print ('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print ('Input file is :', inputfile)
   print ('Output file is :', outputfile)
   print (args)

if __name__ == "__main__":
    # Load data
    # path = os.getcwd()
    # data = read_data_wrsn(path + "/datatsp/infor_cm.txt", path + "/datatsp/u40.txt")
    # data['distances'] = calculate_distances(data['cordination'])

    # s = WRSN(data=data, maxIter=1000, size=100)
    # s.solver()
    # i = s.get_result()
    # print("Finished !")
    # print("Result: ", decode(data, i.gens))
    # temp = get_max_needed_energy(data=data, gens=decode(data, i.gens))
    # print("Max energy: ", temp) 
    
    
    main(sys.argv[1:])
