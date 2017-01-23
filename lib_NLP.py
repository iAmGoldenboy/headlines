__author__ = 'Miklas Njor - iAmGoldenboy - http://miklasnjor.com'
__projectname__ = 'headlines / lib_NLP.py'
__datum__ = '23/01/17'


# from nltk.tokenize import sent_tokenize
# from nltk.stem import SnowballStemmer, snowball
# from nltk.tokenize import RegexpTokenizer
# from nltk.corpus import stopwords
# from nltk import tree, trigrams, word_tokenize, pos_tag, ne_chunk, ne_chunk_sents
# from bs4 import BeautifulSoup
# from collections import Counter
from lib_Update import updateSocialMediaPickle, updateArticleLinksPicle
from lib_Common import getKey1st, getKey3rd, getKey2nd, getKey4th, getKey5th, convertDate
from Lib_pass import mediaTagDict
# import requests
# import string
# from fuzzywuzzy import fuzz
# import time
# from time import sleep
# import json
# import pickle
# import os.path
# from datetime import datetime
# import xmltodict
# import nltk
# from nltk.collocations import *
#
# from nltk.tokenize import sent_tokenize
from nltk.stem import SnowballStemmer, snowball
# from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk import tree, trigrams, word_tokenize, pos_tag, ne_chunk, ne_chunk_sents
from bs4 import BeautifulSoup
from collections import Counter
import requests
import string
from fuzzywuzzy import fuzz
#import feedparser
import time
from time import sleep
# import json
import pickle
# import os.path
# from datetime import datetime


import xmltodict
#import untangle
import nltk
from nltk.collocations import *

tagDict = mediaTagDict()

udvidestopwords = ["ham", "derfor", "seks", "begge", "dermed", "arkivfoto", "kan", "endnu", "modtag e-mail", "anmeldelse", "måske", "følg", "dengang", "live", "berlingske", "anmeldelse", "ja", "nej", "ritzau", "reuters" "kun", "læs", "foto", "siger", "sagde", "mente", "mens", "både", "desuden", "eksperter", "ifølge", "føler", "følte", "flere", "mange", "udover", "samlet", "mener", "fortæller", "håber", "så", "altså", "hvem", "hvad", "hvor", "hvorfor", "hvordan", "hvilket", "hvilken", "tror", "troede"]
dk_Stopwords = stopwords.words('danish') + udvidestopwords
dk_tokenizer = nltk.data.load("tokenizers/punkt/danish.pickle")
dk_Stemmer = SnowballStemmer('danish')


bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()



def nltkGit(sample):

    sentences = nltk.sent_tokenize(removeStopwords(sample),language="danish")
    tokenized_sentences = [nltk.word_tokenize(sentence,language="danish") for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.chunk.ne_chunk_sents(tagged_sentences, binary=True)

    def extract_entity_names(t):
        entity_names = []

        if hasattr(t, 'label') and t.label:
            if t.label() == 'NE':
                entity_names.append(' '.join([child[0] for child in t]))
            else:
                for child in t:
                    entity_names.extend(extract_entity_names(child))

        return entity_names

    entity_names = []
    for tree in chunked_sentences:
        #print("tree", tree)
        # Print results per sentence

        #print("EXO", extract_entity_names(tree))

        entity_names.extend(extract_entity_names(tree))

    # Print all entity names
    #print("EX2", entity_names)

    # Print unique entity names
    return entity_names




def collectNamedEntities(stringToSearchIn):

    #  First we tokenise all the sentences
    tokenizedText = word_tokenize(stringToSearchIn,language="danish")
    #print("Tokenized Articles   ", tokenizedText)


    ##########################
    ### First do own setup ###

    # Collect Trigrams
    trigramText = list(trigrams(tokenizedText))
    #print("Trigrams", trigramText)

    count = 0
    namedEntityList = []
    for trigram in trigramText:

        # Trigrams
        try:
            if not trigram[0].islower() and not trigram[1].islower() and not trigram[2].islower() \
                    and trigram[0].isalpha() and trigram[1].isalpha() and trigram[2].isalpha():
                namedEntityList.append("{} {} {}".format( trigram[0], trigram[1], trigram[2]) )
        except Exception as e:
            print("Trigrams", e)

        # Bigrams
        try:
            if not trigram[0].islower() and not trigram[1].islower()  \
                    and trigram[0].isalpha() and trigram[1].isalpha()  and trigram[0].lower() not in dk_Stopwords:
                namedEntityList.append("{} {}".format( trigram[0], trigram[1] ) )
        except Exception as e:
            print("Bigrams", e)

        # singles
        try:
            if not trigram[0].islower() and not trigram[0].isupper()   \
                    and trigram[0].isalpha() and trigram[1].isalpha() and trigram[2].isalpha()  and trigram[0].lower() not in dk_Stopwords:
                namedEntityList.append("{}".format( trigram[0] ) )
        except Exception as e:
            print("Singles", e)

        # Trigrams with Digits at the end
        try:
            if not trigram[0].islower() and not trigram[1].isupper() and trigram[2].isdigit()  \
                    and trigram[0].isalpha() and trigram[1].isalpha() and trigram[2].isalpha()  and trigram[0].lower() not in dk_Stopwords:
                namedEntityList.append("{} {}".format( trigram[0], trigram[1] ) )
        except Exception as e:
            print("Trigrams Digits", e)

        # ABBR and Title
        try:
            if not trigram[0].islower() and trigram[1].islower() and trigram[2].islower() \
                    and trigram[0].isalpha() and trigram[1].isalpha() and trigram[2].isalpha():
                if trigram[0].isupper() and trigram[0].lower() not in dk_Stopwords:
                    namedEntityList.append("{}".format( trigram[0] ) )

                if trigram[0].istitle() and trigramText[count] != 0  and trigram[0].lower() not in dk_Stopwords\
                        or trigram[0] != trigramText[count-1][1]:
                    namedEntityList.append("{}".format( trigram[0] ) )
        except Exception as e:
            print("ABBR", e)


        # quadgrams and more - looking backwards
        # Quadgrams
        try:
            if not trigram[0].islower() and not trigram[1].islower() and not trigram[2].islower() \
                    and trigram[0].isalpha() and trigram[1].isalpha() and trigram[2].isalpha()\
                    and trigramText[count] != 0 and not trigramText[count-1][0].islower() and trigramText[count-1][0].isalpha():
                namedEntityList.append("{} {} {} {}".format( trigramText[count-1][0], trigram[0], trigram[1], trigram[2]) )
        except Exception as e:
            print("Quadgrams", e)

        # Cincograms
        try:
            if not trigram[0].islower() and not trigram[1].islower() and not trigram[2].islower() \
                    and trigram[0].isalpha() and trigram[1].isalpha() and trigram[2].isalpha()\
                    and trigramText[count] != 0 and trigramText[count] != 1 \
                    and not trigramText[count-2][0].islower() and not trigramText[count-2][1].islower() \
                    and trigramText[count-2][0].isalpha() and trigramText[count-2][1].isalpha():
                namedEntityList.append("{} {} {} {} {}".format( trigramText[count-2][0], trigramText[count-2][1], trigram[0], trigram[1], trigram[2]) )
        except Exception as e:
            print("cinogram", e)

        # Update counter for looking forward or backward
        count += 1


    ##########################
    ### Do correct process ###

    # Do Part of Speach tagging of all elements.
    posTags = pos_tag(stringToSearchIn.split())
    # print("POS                  ", posAllArticles)
    #print("posTagss", posTags)


    # Chunk the sentences and find Named Entities
    neTags = ne_chunk(posTags)
    # print("NE Articles          ", neAllArticles)
    # print("neTags" , neTags)

    collectedNE = []
    for wordTags in neTags:

        if isinstance(wordTags, tree.Tree):

            #print(wordTags)
            realWord = ""
            for realTag in wordTags:
                realWord += "{} ".format(realTag[0])


            # Convert wordTags to string to be able to search
            if "GPE" in str(wordTags):

                collectedNE.append(realWord.strip())
                #print("gpe      ", wordTags)

            elif "ORGANIZATION" in str(wordTags):

                collectedNE.append(realWord.strip())
                #print("Orgs     ", wordTags)

            elif "PERSON" in str(wordTags):

                collectedNE.append(realWord.strip())
                #print("Person   ", wordTags)

    return collectedNE


def stopWordRemover(listCollection):

    listCo = []

    for sent in listCollection.split():

        if sent.isalpha() and sent.lower not in dk_Stopwords:
            listCo.append(sent)
        elif sent in string.punctuation:
            listCo.append(sent)
            print(sent)

    cleanString = " ".join(listCo)

    print(cleanString)

    return cleanString


def removeStopwords(stringToREMOVEstopwordsFrom):

    if isinstance(stringToREMOVEstopwordsFrom, list):
        joinedList = ''
        joinedList += " ".join(stringToREMOVEstopwordsFrom)
        stringToREMOVEstopwordsFrom = joinedList

    dk_Stopwords = stopwords.words('danish')

    stringWithoutStopWords = ""

    for unique in stringToREMOVEstopwordsFrom.split():
        if unique not in dk_Stopwords:
            stringWithoutStopWords += "{} ".format(unique)

    return stringWithoutStopWords




def getTagContent(soup, tagList):

    if isinstance(tagList, str):
        tagList = [tagList]

    finalOutput = []
    for tag in tagList:

        getTagSoup = soup.select(tag)

        contents = [scrubString(content.get_text()) for content in getTagSoup]

        output = []
        for sentences in contents:
            sentencesList = dk_tokenizer.tokenize(sentences)

            for sentence in sentencesList:
                sentenceNoStopwords = []
                keepPunkt = ""
                if sentence[len(sentence)-1:] in string.punctuation:
                    keepPunkt += sentence[len(sentence)-1:]

                for token in word_tokenize(sentence, language="danish"):
                    if token.lower() not in dk_Stopwords:
                        sentenceNoStopwords.append(token.strip())

                sentenceClear = "{}{} ".format(" ".join(sentenceNoStopwords).strip(), keepPunkt.strip())
                output.append(sentenceClear)

        finalOutput.append("".join(output))

    return "".join(finalOutput)



def scrubString(string):

    cleanString = string.strip().replace("  ", " ").replace("»", ", ").replace("’"," ").replace(":", ", ").replace(" - ", ", ").replace("«", ", ").replace("\n", ", ").replace('"', ", ").replace("'", ", ")

    return cleanString






def pruneNECollection(listItems):

    seenList = []
    removeDict = {}
    for item in listItems:
        for reversedItem in sorted(listItems, reverse=True):
            score = fuzz.ratio(item, reversedItem)
            if score > 85 and score < 100 and reversedItem[1] not in seenList:
                shortest = list([item, reversedItem])
                removeIt = sorted(list(shortest), reverse=True)[0][1]
                keep = sorted(list(shortest), reverse=True)[1][1]
                seenList.append(removeIt[1])
                try:
                    removeDict[removeIt[1]] = keep[1]
                except Exception as e:
                    pass

    counter = 0
    newlist, deadstuff = [], []

    for itemkey in listItems:

        if removeDict.get(itemkey[1]):
            try:
                for rounds in range(int(itemkey[0])):
                    newlist.append(removeDict.get(itemkey[1]))
            except Exception as e:
                print("Error on removal", e)

            # print("adding to deadstuff ->:", listItems[counter][1])
            deadstuff.append(listItems[counter][1])

        else:
            if itemkey[1] not in deadstuff:
                try:
                    for rounds in range(int(itemkey[0])):
                        newlist.append(itemkey[1])
                except Exception as e:
                    print("Error on adding", e)

        counter += 1

    return newlist

def getCollocations(stringContent):

    #stringNoPuncuation = tokenizeRemovePunctuation(str(cleanAndBuild(soup, ".article__summary")).strip())
    #stringNoStopNoPunct = [word for word in stringNoPuncuation if word.lower() not in dk_Stopwords]

    #print("stringerbell", stringNoPuncuation)
    # Find collocations spanning over four words
    finder = TrigramCollocationFinder.from_words(word_tokenize(stringContent), window_size=3)

    # Must occur at least three times
    finder.apply_freq_filter(2)

    # Add the twenty top most collocations to a list
    trigramCollocations = finder.nbest(bigram_measures.pmi, 20)

    #print( "trigrams:   ", trigramCollocations)

    return trigramCollocations


def onlyTheTip(prunedCounter):

    iceberg = []
    for id, data in prunedCounter.items():
        if data > 1:
            # print("include", id, data)
            iceberg.append([id, data])

    return sorted(iceberg, key=getKey2nd, reverse=True)



def get_news(publication="p-indland", verbose=False):

    collectOutput, articleLinkList = [], []
    feedsDict = None

    try:
        feed = requests.get(publication.get('rsslink'))

        feedsDict = xmltodict.parse(feed.content, process_namespaces=True)
    except Exception as e:
        print("No feed: ", e)
    # print(feedsDict)

    try:
        with open("static/data/articleLinkPickle.p", 'rb') as handle:
            alDict = pickle.load(handle)

    except Exception as e:
        print("Couldn't get article dict for checking for new links: ", e )

    if feedsDict:
        try:
            for feedItem in feedsDict["rss"]["channel"]["item"]:

                articleLink = feedItem["link"].replace("?referrer=RSS", "")

                if alDict.get(articleLink) is None:

                    # Convert date
                    dated = convertDate(feedItem["pubDate"])

                    # print where we are getting data from
                    print("Title: {}    Link: {}".format( feedItem["title"], feedItem["link"]))
                    # print("Date", feedItem["pubDate"], dated) # Thu, 19 Jan 2017 16:17:00


                    # print("desc ", feedItem["description"])
                    # articleLink = feedItem["link"].replace("?referrer=RSS", "")

                    updateArticleLinksPicle(articleLink, dated, publication.get("kategori"), publication.get("avis"))

                    articleLinkList.append(articleLink)

                    # Get the webpage
                    getLinkData = requests.get(articleLink)
                    soup = BeautifulSoup(getLinkData.content, "lxml")

                    # Extract only the article text
                    textData = getTagContent(soup, tagList=tagDict.get(publication.get("avis") ))
                    print("Processed text:  ", textData)

                    # Find and extract the Named Entities
                    NEdata = extractNE(textData)


                    collectOutput.append([NEdata, articleLink, dated])

                    sleep(4)

                else:
                    print("Already seen:    ", feedItem["link"])

        except Exception as e:
            print("could not get {} article data".format(publication, e))

    if verbose == True:
        print("Done with", publication)

    epoch_time = int(time.time())
    updateSocialMediaPickle(articleLinkList, epoch_time )

    return collectOutput


def extractNE(textData, verbose=False):

    # Create a list of collocations
    collocationsList = [" ".join(bits for bits in chunk) for chunk in getCollocations(textData)]

    # and extract named entities from collocations
    NEcollocations = collectNamedEntities(" - ".join(collocationsList))

    # Extract the named entities via two methods
    NEcollection = collectNamedEntities(textData) + nltkGit(textData)

    # Merge all three Methods
    mergedNEs = NEcollection + NEcollocations

    # Create counter object
    NEcounter = [[data, id] for id, data in Counter(mergedNEs).items()]

    # Prune the NEcounter object to remove dublicates (could refine this mor)
    NEdata = pruneNECollection(NEcounter)

    if verbose:
        print("Newlist      ",  Counter(NEdata))
        print()

    return NEdata