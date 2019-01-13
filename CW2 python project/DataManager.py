# This work is licensed under the Creative Commons Attribution 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/
# or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

import json
import io
import sys


class DataManager:

    def __init__(self, filename):
        self.filename = filename
        self.lineCount = 0

    def genData(self):
        """This method is a generator that allows looping through a json file line by line"""
        try:
            with io.open(self.filename, 'r', -1, 'utf-8') as f:
                # Code based on https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
                for line in f:
                    self.lineCount += 1
                    yield json.loads(line)
        except FileNotFoundError:
            print('The file \'%s\' does not exist' % str(self.filename))
            sys.exit()  # Exit the program if there is not data to process
