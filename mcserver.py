import ConfigParser, logging, datetime, os, json, requests

from flask import Flask, render_template, request

import mediacloud

import chartkick

from API_config import MY_API_KEY

app=Flask(__name__,static_folder=chartkick.js(), static_url_path='/static/js/')
app.jinja_env.add_extension("chartkick.ext.charts")

CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

# load the settings file
config = ConfigParser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

# set up logging
log_file_path = os.path.join(basedir,'logs','mcserver.log')
logging.basicConfig(filename=log_file_path,level=logging.DEBUG)
logging.info("Starting the MediaCloud example Flask app!")

# clean a mediacloud api client
mc = mediacloud.api.MediaCloud( config.get('mediacloud','api_key') )

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("search-form.html")

@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']
    startdate_post = request.form['startdate']
    enddate_post = request.form['enddate']

    startdate = datetime.datetime.strptime(startdate_post, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(enddate_post, '%Y-%m-%d')

    parameters = {'split':'1', 'split_start_date':startdate_post,'split_end_date':enddate_post, 'key':MY_API_KEY}

    results = requests.get("https://api.mediacloud.org/api/v2/sentences/count?q=sentence:"+str(keywords)+"+AND+tags_id_media:8875027", params=parameters)
    data = results.json()

    return render_template("search-results.html", 
        keywords=keywords, startdate=startdate, enddate=enddate, sentenceCount=data['count'], data=data)



if __name__ == "__main__":
    app.debug = True
    app.run()
