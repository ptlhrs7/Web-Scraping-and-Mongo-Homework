import imp
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# use flask pymongo to set up the connection to the database
app.config["MONGO_URL"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)


@app.route("/")
def index():
    #access information from the database
    mars_data = mongo.db.marsData.find_one()

    return render_template("index.html", mars=mars_data)


@app.route("/scrape")
def scrape():
    #reference to a database collection (table)
    marsTable = mongo.db.marsData

    # drop the table if it exisits
    mongo.db.marsData.drop()

    #call scrape mars script
    mars_data = scrape_mars.scrape_all()

    #take the dictionary and load it into mongoDB
    marsTable.insert_one(mars_data)

    # go back to the index route
    return redirect("/")


if __name__ == "__main__":
    app.run()

# Refence code used from Dr.A's Videos
