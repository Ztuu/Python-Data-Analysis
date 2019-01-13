# This work is licensed under the Creative Commons Attribution 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/
# or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

import sys
sys.path.append("graphviz-0.10.1")

import matplotlib.pyplot as plt
from graphviz import Digraph


class GraphDisplay:

    savename = 'dot_graph'

    def drawHistogram(self, data, label="Count", title="title"): # Adapted from simple_histo.py sample source
        """Draws a histogram from an input dictionary.
        Keys become bars, value is count that will be shown on chart."""
        bar_fun = plt.barh  # NB: this assigns a function to bar_fun!
        bar_ticks = plt.yticks
        bar_label = plt.xlabel

        n = len(data)
        bar_fun(range(n), list(data.values()), align='center', alpha=0.4)
        bar_ticks(range(n), list(data.keys()))
        bar_label(label)
        plt.title(title)
        plt.show()

    def drawAlsoLikesGraph(self, data, docID, lineCount, visitorID = None):
        """This method draws a dot graph based on also likes data passed to it and saves it as a pdf"""
        # Some code basics taken from https://graphviz.readthedocs.io/en/stable/manual.html
        if data is None or not type(data) == dict:
            print('invalid data of type %s cannot be used for dot graph creation' % str(type(data)))
            return

        if lineCount // 1000000 != 0:
            size = str(lineCount // 1000000) + 'm lines'
        elif lineCount // 1000 != 0:
            size = str(lineCount // 1000) + 'k lines'
        else:
            size = str(lineCount) + ' lines'

        dot = Digraph(name='The graph')
        dot.node('Readers', shape='none')
        dot.node('Documents', shape='none')
        dot.edge('Readers', 'Documents', label=('Size: %s' % size))

        try:
            for visitor in data:
                if visitor == visitorID:
                    dot.node(str(visitor)[-4:], fillcolor='green', style='filled', shape='box')
                else:
                    dot.node(str(visitor)[-4:], shape='box')
                for document in data[visitor]:
                    if document == docID:
                        dot.node(str(document)[-4:], fillcolor='green', style='filled')
                    else:
                        dot.node(str(document)[-4:])
                    dot.edge(str(visitor)[-4:], str(document)[-4:])
        except TypeError:
            print('Incorrect type passed to drawAlsoLikesGraph')
        except:
            print('Unexpected error when trying to create also likes graph')

        try:
            dot.render(self.savename, view=True)
        except:
            print('Cannot save graph to file with filename \'%s\'. Check if the file is open or locked' % self.savename)
