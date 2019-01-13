# This work is licensed under the Creative Commons Attribution 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/
# or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

import DataManager as dm
import DataAnalyser as da
import GraphDisplay as gd


class TaskController:

    def countCountries(self):
        """Will loop through the data counting the countries that have visited the input doc.
        Then it will draw a histogram of the results"""
        self.data_ana.countCountry(self.inputDoc, self.datamng)
        self.gdisp.drawHistogram(self.data_ana.countryCounts, title="Country counts", label="Number of visits")

    def countContinents(self):
        """Will loop through the data counting the countries that have visited the input doc then grouping them by continent
        Then it will draw a histogram of the results"""
        self.data_ana.countCountry(self.inputDoc, self.datamng)
        self.data_ana.countContinent()
        self.gdisp.drawHistogram(self.data_ana.continentCounts, title="Continent counts", label="Number of visits")

    def countFullBrowser(self):
        """Will loop through the data counting the browsers that have visite the input doc.
        Takes into account full browser string with all information.
        Then it will draw a histogram of the results"""
        self.data_ana.countFullBrowser(self.datamng, self.inputDoc)
        self.gdisp.drawHistogram(self.data_ana.browserCounts, title="Browser counts", label="Number of users")

    def countShortBrowser(self):
        """Will loop through the data counting the browsers that have visite the input doc.
        Only takes into account short browser information with title and program.
        Then it will draw a histogram of the results"""
        self.data_ana.countFullBrowser(self.datamng, self.inputDoc)
        self.data_ana.countShortBrowser()
        self.gdisp.drawHistogram(self.data_ana.shortBrowserCounts, title="Short browser counts", label="Number of users")

    def alsoLikes(self):
        """Returns a sorted list of documents that have been read by readers of the input document
        By default the returned list is sorted by highest number of readers
        """
        relatedDocs = self.data_ana.alsoLikesFast(self.datamng, self.inputDoc, self.inputUser)
        if relatedDocs:
            print(relatedDocs)

    def alsoLikesGraph(self):
        """Graphically displays also likes information for a document and optionally a user.
        If a user is provided documents that user has seen will not be shown.
        Saves the produced graph as a pdf."""
        graphdata = self.data_ana.alsoLikesGraph(self.datamng, self.inputDoc, self.inputUser)
        if graphdata:
            self.gdisp.drawAlsoLikesGraph(graphdata, self.inputDoc, self.datamng.lineCount, self.inputUser)

    tasks = {
        '2a': countCountries,
        '2b': countContinents,
        '3a': countFullBrowser,
        '3b': countShortBrowser,
        '4d': alsoLikes,
        '5': alsoLikesGraph
    }

    def __init__(self, filename, task_id, document_uuid, user_uuid = None):
        self.filename = filename
        self.task = task_id
        self.inputDoc = document_uuid
        self.inputUser = user_uuid

        self.datamng = dm.DataManager(self.filename)
        self.data_ana = da.DataAnalyser()
        self.gdisp = gd.GraphDisplay()

        if self.task not in self.tasks:
            print('Task \'%s\' is not a valid task.\nPlease type -h for help on program usage' % self.task)
        else:
            if self.inputDoc is not None:
                self.tasks[self.task](self)
            else:
                print('Please provide an input document')
