#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import feedparser
from flask import Flask, render_template
import pickle
import time
import os
from lib_Common import bumper



app = Flask(__name__)

#BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"
# feedsDict = { "bbc" : "http://feeds.bbci.co.uk/news/rss.xml",
#               "cnn" : "http://rss.cnn.com/rss/edition.rss",
#               "pol" : "http://politiken.dk/rss/indland.rss" }

articlePickle = "static/data/articleLinkPickle.p"
namedEntPickle = "static/data/namedEntityPickle.p"

@app.route("/")
# @app.route("/<publication>")
def get_news(publication="bbc"):

    # feed = feedparser.parse(feedsDict[publication])
    # first_article = feed['entries'][0]

#     return """<html>
#                 <body>
#                         <h1>{0} headsss</h1>
#                         <b>{1}</b><br/>
#                         <i>{2}</i><br/>
#                         <p>{3}</p><br/>
#                         <p>{4} - {5}</p>
#
#                 </body>
#              </html>""".format(publication, first_article.get("title").encode("utf-8"), first_article.get("published").encode("utf-8"), first_article.get("summary").encode("utf-8"), first_article,
# type(first_article)  )

    # with open(articlePickle, 'rb') as handle:
    #     aDict = pickle.load(handle)
    # # print("hej")
    # # for id, data in aDict.items():
    # #     print(id,data)
    # mystrint = ""
    #
    # try:
    #     for article, articleData in aDict.items():
    #         mystrint += "<br> Avis: {}\t, \t- Tid: {}, Sektion: {}, Link: {}".format(articleData.get("paper"),  articleData.get("time"), articleData.get("section"), article )
    # except Exception as e:
    #     print("crap", e)
    inhere = "ddd"
    for i in range(10):
        inhere += str(i)
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        inhere += " -/- {}".format(f)
        # do something

    return render_template("index.html", jammi=inhere)

@app.route("/avislinks")
def avislinks():

    with open(articlePickle, 'rb') as handle:
        aDict = pickle.load(handle)

    with open(namedEntPickle, 'rb') as handle:
        neDict = pickle.load(handle)

    timedDict = {}
    for id, data in aDict.items():

        timed = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data.get("time")))
        timedDict[id] = {'time' : timed, 'paper' : data.get("paper"), "section" : data.get("section") }

    return render_template("listarticles.html",
                           title="yo",
                           output=timedDict)

@app.route("/namedentities")
def listNEs():
    pass


if __name__ == "__main__":
    app.run(port=5000, debug = True)
