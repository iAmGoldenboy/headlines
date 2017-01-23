__author__ = 'Miklas Njor - iAmGoldenboy - http://miklasnjor.com'
__projectname__ = 'headlines / lib_cron.py'
__datum__ = '23/01/17'

import schedule
import time
import pickle
from collections import Counter
from lib_NLP import onlyTheTip, get_news
from Lib_pass import mediaRSSDict, mediaTagDict
from lib_Common import get_social_metrics, getSocialCount
from lib_Update import updateSocialMediaPickle, updateNamedEntityPickle, updateArticleLinksPicle

def updatingSocialMedia():
    # current time
    epoch_time = int(time.time())
    print("EP time", epoch_time)

    # getting social media.
    with open("articleLinkPickle.p", 'rb') as handle:
        alDict = pickle.load(handle)

    collectSocialMediaData = []
    for ids, data in alDict.items():
        print("ids and data", ids, data)
        try:
            smData = getSocialCount(get_social_metrics(ids))
            collectSocialMediaData.append([ids, smData])
        except Exception as e:
            print("Couldnt collect social media for {} due to: ".format(ids, e))

    print("collection of socialmedia data List:  ", collectSocialMediaData)

    try:
        updateSocialMediaPickle(collectSocialMediaData, epoch_time)
    except Exception as e:
        print("Couldnt update social media due to ", e)

    print("Pausing...")


mediaRSSdict = mediaRSSDict()

def pullRSS():
    for paper, paperData in mediaRSSdict.items():
        print("Feed n data:    ", paper, paperData)

        try:
            # get data from each feed and look at each article:
            gettingNews = get_news(mediaRSSdict[paper], verbose=False)
            print("Named entities for Feed:  {}   : {} ".format( paper, gettingNews) )
        except Exception as e:
            print("Couldnt get news due to: ", e)

        if gettingNews:
            try:
                for newArticle in gettingNews:
                    print("starting to update NE dict:     ", newArticle)
                    updateNamedEntityPickle(onlyTheTip(Counter(newArticle[0])), newArticle[1])
            except Exception as e:
                print("Couldnt update entities due to ", e)

    print("Pausing")


# https://github.com/dbader/schedule
def runningSchedule():
    schedule.every(5).minutes.do(pullRSS)
    schedule.every(30).minutes.do(updatingSocialMedia)

    while True:
        schedule.run_pending()
        time.sleep(1)