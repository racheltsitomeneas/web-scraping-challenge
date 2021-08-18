# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os



# Create an instance of Flask app
app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")    # index.html 
def index():
    mars = mongo.db.mars_db.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape") #
def scraper():
    mars = mongo.db.mars_db
    mars_data = scrape_mars.scrapeall()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

