__author__ = 'Miklas Njor - iAmGoldenboy - http://miklasnjor.com'
__projectname__ = 'headlines / lib_Update.py'
__datum__ = '23/01/17'

import pickle
import os

def updateArticleLinksPicle(articleLink, epoch, section, paper, verbose=False):

    articlePicle = "articleLinkPickle.p"
    # articleLink - epoch - section - paper

    # open the dict (try)
    # if articleLinkDict.p not exists create
    # else open it
    # update the dict with the article link details
    # save the updated dict.

    try:
        if not os.path.isfile(articlePicle):
            with open(articlePicle, 'wb') as handle:
                # print("creating articlePickle")
                mydict = {}
                mydict[articleLink] = {"time" : epoch,  "section" : section,  "paper" : paper }
                pickle.dump(mydict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            with open(articlePicle, 'rb') as handle:
                aDict = pickle.load(handle)
                # print("First", aDict)

            if aDict.get(articleLink) is None:
                aDict[articleLink] = {"time" : epoch,  "section" : section,  "paper" : paper }

                with open(articlePicle, 'wb') as handle:
                    pickle.dump(aDict, handle, protocol=pickle.HIGHEST_PROTOCOL)

            else:
                if verbose == True:
                    print("     Already here: ", articleLink)

            # with open(articlePicle, 'rb') as handle:
            #     aDict = pickle.load(handle)
            #     # print("second:", aDict)

    except Exception as e:
        print("Pickle error:", e)


# articleNEs
# name - articleLinksList - friendsList - closeFriendsList



def updateNamedEntityPickle(inputList, articleLink, verbose=False):

    namedEntityPickle = "namedEntityPickle.p"

    print("Input:   ", inputList, articleLink)

    if not os.path.isfile(namedEntityPickle):
        # print("ok, not here")
        with open(namedEntityPickle, 'wb') as handle:
            mydict = {}

            pickle.dump(mydict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(namedEntityPickle, 'rb') as handle:
        neDict = pickle.load(handle)

    for namedEntity in inputList:

        if neDict.get(namedEntity[0]):
            newfriends   = set([item[0] for item in inputList if item[0] is not namedEntity[0]])
            oldFriends   = set([name for name in neDict.get(namedEntity[0]).get("friendsList")])
            articleLinks = [artLink for artLink in neDict[namedEntity[0]].get("articleLinks")]

            neDict[namedEntity[0]] = {   'mentionCount' : int(neDict[namedEntity[0]].get("mentionCount")) + namedEntity[1],
                                         'friendsList' : oldFriends.union(newfriends),
                                         'closeFriends' : (newfriends).intersection(oldFriends),
                                         'articleCount' : neDict[namedEntity[0]].get("articleCount") + 1,
                                         'articleLinks' : articleLinks + [articleLink]
                                     }

        else:
            neDict[namedEntity[0]] = {   'mentionCount' : int(namedEntity[1]),
                                         'friendsList' : set([item[0] for item in inputList if item[0] is not namedEntity[0]]) ,
                                         'closeFriends' : [],
                                         'articleCount' : 1,
                                         'articleLinks' : [articleLink]
                                     }

    with open(namedEntityPickle, 'wb') as handle:
        pickle.dump(neDict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def updateSocialMediaPickle(articleLinkList, timeValue, verbose=False):

    socialMediaPickle = "socialMediaPickle.p"

    # articleLink - SMtimeList - SM-countList

    print("Input Social:   ", articleLinkList, timeValue)

    if not os.path.isfile(socialMediaPickle):
        with open(socialMediaPickle, 'wb') as handle:
            # print("opening")
            mydict = {}
            pickle.dump(mydict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(socialMediaPickle, 'rb') as handle:
        smDict = pickle.load(handle)

    for articleLink in articleLinkList:
        print(articleLink)

        if smDict.get(articleLink[0]):

            smDict[articleLink[0]] = {   'time' : smDict.get(articleLink[0]).get("time") + [timeValue],
                                         'smCount' : smDict.get(articleLink[0]).get("smCount") + [articleLink[1]]  }

        else:
            smDict[articleLink[0]] = {   'time' : [timeValue],
                                         'smCount' : [articleLink[1]]  }

    with open(socialMediaPickle, 'wb') as handle:
        pickle.dump(smDict, handle, protocol=pickle.HIGHEST_PROTOCOL)