# This work is licensed under the Creative Commons Attribution 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/
# or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

import argparse  # https://docs.python.org/2/howto/argparse.html
import TaskController as tc
import DataGUI as dg
import sys

# Define the arguments for command line usage
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", type=str, help="Name of file storing json")
parser.add_argument("-u", "--user_uuid", type=str, help="User id of visitor to search for")
parser.add_argument("-d", "--document_uuid", type=str, help="Document id of the document to search for")
parser.add_argument("-t", "--task_id", type=str, help="ID identifying which task the program should carry out.")

# Read in the arguments
args = parser.parse_args()

# Run the gui if the user passed no arguments
if len(sys.argv) == 1:  # There will always be one argument which is this file's name
    dg.DataGUI()
else:
    if args.filename is None or args.document_uuid is None or args.task_id is None:
        # Don't run if necessary arguments aren't present
        print('Invalid arguments passed. For instruction on usage use the -h argument or to run GUI pass no arguments')
        sys.exit()
    else:
        tc.TaskController(args.filename, args.task_id, args.document_uuid, args.user_uuid)
