__author__ = 'Miklas Njor - iAmGoldenboy - http://miklasnjor.com'
__projectname__ = 'headlines / lib_Common.py'
__datum__ = '23/01/17'


from Lib_pass import apikey
# from lib_NLP import scrubString, dk_tokenizer
import requests
# import string
from time import sleep
import json
import time

def bumper(bumm, width=35):

    # print((width - len(bumm)), "yo")
    return ((width - len(bumm)) * " ")

def get_social_metrics(url, pause=3):
    api_key = apikey()
    formalcall = "{}{}{}{}".format( 'https://free.sharedcount.com/?url=', url , '&apikey=' , api_key )

    dataDict = {}
    try:
        sharedcount_response = requests.get(formalcall)

        sleep(pause)

        if sharedcount_response.status_code == 200:
            data = sharedcount_response.text
            dataDict = dict(json.loads(data))
            return dataDict

    except Exception as e:
        print("Moving onwards due to", e)
        return dataDict



def getSocialCount(socialDict, spread=True):

    accumCount = 0
    if spread and socialDict is not None:
        # print(socialDict)

        try:
            for key, data in socialDict.items():
                if isinstance(data, int):
                    accumCount += data

                elif key == "Facebook":
                    accumCount += data.get("total_count")
        except Exception as e:
            print("Social Counter died:", e)

    # print(accumCount)
    return accumCount



def convertDate(datevalue):

    epoch = None

    try:
        p = "%a, %d %b %Y %H:%M:%S %z"
        epoch = int(time.mktime(time.strptime(datevalue,p)))

    except Exception as e:
        p = "%a, %d %b %Y %H:%M:%S %Z"
        epoch = int(time.mktime(time.strptime(datevalue,p)))

    except Exception as e:
        print("No time convert")

    return epoch




def getKey1st(item): return item[0]

def getKey2nd(item):  return item[1]

def getKey3rd(item):  return item[2]

def getKey4th(item): return item[3]

def getKey5th(item):  return item[4]