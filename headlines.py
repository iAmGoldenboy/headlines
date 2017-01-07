from flask import Flask

#test comment

app = Flask(__name__)

@app.route("/")
def  get_news():
    return "hej you - good or bad news"

if __name__ == "__main__":
    app.run(port=5000, debug = True)
