from flask import Flask, jsonify, redirect, render_template
import pymongo
import scrape_mars

# Establish MongoDG server connection on local machine
conn = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(conn)

# Initialize Flash
app = Flask(__name__)

# Create Mars DB collection in mongoDB
db = client.mars_db
mars_pull = db.mars_db

# Create scrape route to pull database objects/html into index
@app.route('/scrape')
def scrape_mars_data():
    scrape_results = scrape_mars.scrape()
    mars_pull.replace_one({}, scrape_results, upsert=True)
    return redirect('http://localhost:5000/')

# Create route to assign variables from scrape_mars.py into index.html render template
@app.route("/")
def render_index():
 
    mars_find =  mars_pull.find_one()
    newsTitle = mars_find['news_data']['newsTitle']
    newsHeader = mars_find['news_data']['newsHeader']
    newsIntro = mars_find['news_data']['newsIntro']
    featured_image_url = mars_find['featured_image_url']
    recent_mars_weather = mars_find['mars_weather']
    mars_facts = mars_find['mars_facts']
    hemisphere_title_1 = mars_find['mars_hemispheres'][0]['title']
    hemisphere_image_1 = mars_find['mars_hemispheres'][0]['image_url']
    hemisphere_title_2 = mars_find['mars_hemispheres'][1]['title']
    hemisphere_image_2 = mars_find['mars_hemispheres'][1]['image_url']
    hemisphere_title_3 = mars_find['mars_hemispheres'][2]['title']
    hemisphere_image_3 = mars_find['mars_hemispheres'][2]['image_url']
    hemisphere_title_4 = mars_find['mars_hemispheres'][3]['title']
    hemisphere_image_4 = mars_find['mars_hemispheres'][3]['image_url']

    return render_template("index.html", newsTitle=newsTitle,
                                         newsHeader=newsHeader,
                                         newsIntro=newsIntro,
                                         featured_image_url=featured_image_url,
                                         recent_mars_weather=recent_mars_weather,
                                         mars_facts=mars_facts,
                                         hemisphere_title_1=hemisphere_title_1,
                                         hemisphere_image_1=hemisphere_image_1,
                                         hemisphere_title_2=hemisphere_title_2,
                                         hemisphere_image_2=hemisphere_image_2,
                                         hemisphere_title_3=hemisphere_title_3,
                                         hemisphere_image_3=hemisphere_image_3,
                                         hemisphere_title_4=hemisphere_title_4,
                                         hemisphere_image_4=hemisphere_image_4)


if __name__ == '__main__':
    app.run()


