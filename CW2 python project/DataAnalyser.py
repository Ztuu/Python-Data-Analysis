# This work is licensed under the Creative Commons Attribution 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/
# or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

import sys
sys.path.append('pycountry-convert-0.7.2')
import pycountry_convert as pyccvt
import operator


class DataAnalyser:

    countryCounts = {}
    continentCounts = {}
    browserCounts = {}
    shortBrowserCounts = {}

    def countCountry(self, docID, data):
        """Counts the countries a single document has been visited from and how many times it has been visited"""
        for entry in data.genData():
            if 'subject_doc_id' in entry and 'visitor_country' in entry and 'event_type' in entry:
                if entry['event_type'] == 'read':
                    if str(entry['subject_doc_id']) == docID:  # cast to string needed as input is string
                        if entry['visitor_country'] in self.countryCounts:
                            self.countryCounts[entry['visitor_country']] += 1
                        else:
                            self.countryCounts[entry['visitor_country']] = 1

    def countContinent(self):
        """Groups the countries a single document has been visited from into the continents"""
        if self.countryCounts == {}:
            print('No data to count')
            return
        else:
            for country in self.countryCounts:
                try:
                    continent = pyccvt.country_alpha2_to_continent_code(country)
                except ModuleNotFoundError:
                    print('Pycountry-convert module not installed')
                    continue
                except KeyError:
                    print('No continent for country with code %s.' % country)
                    continue
                except:
                    print('Error converting country to continent for country: %s' % country)
                    continue # don't try and add if there isn't a valid continent

                if continent in self.continentCounts:
                    self.continentCounts[continent] += 1
                else:
                    self.continentCounts[continent] = 1

    def countFullBrowser(self, data, docID):
        """Counts how many times each unique browser setup has been used."""
        for entry in data.genData():
            if 'visitor_useragent' in entry and 'event_type' in entry:
                if entry['event_type'] == 'read':
                    if str(entry['subject_doc_id']) == docID:
                        if entry['visitor_useragent'] in self.browserCounts:
                            self.browserCounts[entry['visitor_useragent']] += 1
                        else:
                            self.browserCounts[entry['visitor_useragent']] = 1

    def countShortBrowser(self):
        """Counts the number of times each browser has been used in any setup"""
        if self.browserCounts == {}:
            print('No data to count')
            return
        else:
            for browser in self.browserCounts:
                browserName = browser.split('/')[0] + ' ' + browser.split('/')[-2].split(' ')[-1]
                if browserName in self.shortBrowserCounts:
                    self.shortBrowserCounts[browserName] += self.browserCounts[browser]
                else:
                    self.shortBrowserCounts[browserName] = self.browserCounts[browser]

    def commonVisitor(self, data, docID, visitorID = None):
        """Returns all visitors that have visited a specific document.
        Optionally excludes a single visitor"""
        visitors = []
        for entry in data.genData():
            if 'subject_doc_id' in entry and 'visitor_uuid' in entry and 'event_type' in entry:
                if entry['event_type'] == 'read':
                    if str(entry['subject_doc_id']) == docID and not entry['visitor_uuid'] == visitorID:
                        visitors.append(entry['visitor_uuid'])
        return visitors

    def visitorDocs(self, data, visitorID, docID = None):
        """Returns all documents a visitor has visited.
        Optionally excludes a single document"""
        documents = []
        for entry in data.genData():
            if 'visitor_uuid' in entry and 'subject_doc_id' in entry and 'event_type' in entry:
                if entry['event_type'] == 'read':
                    if str(entry['visitor_uuid']) == visitorID and not str(entry['subject_doc_id']) == docID:
                        documents.append(entry['subject_doc_id'])
        return documents

    def sortByValues(inputDict):
        """Sorts a dictionary in descending order of values.
        Returns the sorted list of keys"""
        # sorting a dictionary: by values https://stackoverflow.com/questions/20944483/python-3-sort-a-dict-by-its-values
        sortedResult = sorted(inputDict.items(), key=operator.itemgetter(1), reverse=True)
        return [item[0] for item in sortedResult]  # list of first index from tuples https://stackoverflow.com/questions/10735282/python-get-list-of-tuples-first-index

    def alsoLikes(self, data, docID, visitorID = None, sortFunc = sortByValues):
        """Original implementationg of also likes that makes use of commonVisitor and visitorDocs methods
        Returns a sorted list of documents relevant to a specific document.
        Optionally takes a visitor who's documents should be omitted."""
        result = {}
        for visitor in self.commonVisitor(data, docID, visitorID):
            if visitor == visitorID:
                continue
            for doc in self.visitorDocs(data, visitor, docID):
                if doc in result:
                    result[doc] += 1
                else:
                    result[doc] = 1
        return sortFunc(result)

    def alsoLikesData(self, data):
        """Method for parsing data set and producing data required for generating also likes results.
        Returns a dict containing all docs and their list of visitors
        and a dict containing all visitors and their list of docs"""
        docVisitors = {}
        userDocuments = {}

        for entry in data.genData():
            if 'visitor_uuid' in entry and 'subject_doc_id' in entry and 'event_type' in entry:
                if entry['event_type'] == 'read':

                    # Add visitor to list of visitors for each document
                    docName = entry['subject_doc_id']
                    visitorName = entry['visitor_uuid']

                    if docName in docVisitors:
                        if visitorName not in docVisitors[docName]:  # Make sure not add duplicates
                            docVisitors[docName].append(visitorName)
                    else:
                        docVisitors[docName] = [visitorName]

                    # Add document to list of documents for each visitor
                    if visitorName in userDocuments: #
                        if docName not in userDocuments[visitorName]:  # Make sure not add duplicates
                            userDocuments[visitorName].append(docName)
                    else:
                        userDocuments[visitorName] = [docName]

        return docVisitors, userDocuments

    def alsoLikesFast(self, data, docID, visitorID=None, sortFunc = sortByValues):
        """Returns a sorted list of documents relevant to a specific document.
        Optionally takes a visitor who's documents should be omitted."""
        result = {}

        docVisitors, userDocuments = self.alsoLikesData(data)

        # Before trying to calculate also likes check that document specified is in the data set
        if docID not in docVisitors:
            print('Document \'%s\' not found in data set' % str(docID))
            return

        for visitor in docVisitors[docID]:
            if visitor != visitorID:
                for document in userDocuments[visitor]:
                    if document != docID:
                        if document in result:
                            result[document] += 1
                        else:
                            result[document] = 1

        sortedResult = sortFunc(result)
        if len(sortedResult) > 10:
            sortedResult = sortedResult[:10]  # Slice list to only first 10 elements if longer than 10
        return sortedResult

    def alsoLikesGraph(self, data, docID, visitorID = None):
        """Generates the data required to draw an also likes graph for a document.
        Optionally takes a visitor uuid which will exclude any documents this user has read other than the input.
        Will exclude users who do not contribute any documents other than the input."""
        result = {}
        docVisitors, userDocuments = self.alsoLikesData(data)

        if docID in docVisitors:
            visitors = docVisitors[docID]
        else:
            print("Document %s not found in data set" % str(docID))
            return

        for user in userDocuments:
            if user == visitorID:
                result[user] = [docID]  # Don't want to include any other docs visitor has seen
            else:
                if user in visitors and not userDocuments[user] == [docID]:  # Don't add visitors who contribute no other documents
                    result[user] = userDocuments[user]
        return result
