import sys
from project_name.start import *
#import importlib
#import argparse

if len(sys.argv) == 1:
    raise SyntaxError("Please provide a module to load.")
parser = argparse.ArgumentParser(description='Pyspark Job Arguments')
parser.add_argument("--region",type=str)
parser.add_argument("--configFile",type=str)
args    = parser.parse_args()

#configs =  typeSafe.parseConfig(args.configFile,convertToJson=True)[args.region]
main(args.configFile,args.region)

