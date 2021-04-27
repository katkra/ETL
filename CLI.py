import os
import sys
import argparse
import main


# Create the parser
my_parser = argparse.ArgumentParser(prog='CLI',description='Organization information from GitHub')

# Add the arguments
my_parser.add_argument('Organization',
                       metavar='organization',
                       type=str,
                       help='the organization to get from GitHub')

# Execute the parse_args() method
args = my_parser.parse_args()

input_path = args.Organization

if not os.path.isdir(input_path):
    print('The path specified does not exist')
    sys.exit()


#print('\n'.join(os.listdir(input_path)))