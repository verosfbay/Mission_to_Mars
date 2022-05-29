# Import tools
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   mars_data = scraping.scrape_all()
   return render_template("index.html", mars=mars)

# Our next function will set up our scraping route.
# This route will be the "button" of the web application
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

# Tell Flask to run
if __name__ == "__main__":
   app.run(debug=True) 

