# -*- coding: utf-8 -*-

import feedparser
from flask import Flask

app = Flask(__name__)

#BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"
feedsDict = { "bbc" : "http://feeds.bbci.co.uk/news/rss.xml", 
              "cnn" : "http://rss.cnn.com/rss/edition.rss" }

@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):

    feed = feedparser.parse(feedsDict[publication])
    first_article = feed['entries'][0]

    return """<html>
		<body> 
			<h1>{0} heads</h1>
			<b>{1}</b><br/>
			<i>{2}</i><br/>
			<p>{3}</p><br/>
		</body>
	     </html>""".format(publication, first_article.get("title"), first_article.get("published"), first_article.get("summary") )

    # return "hej you - good or bad news"

if __name__ == "__main__":
    app.run(port=5000, debug = True)
