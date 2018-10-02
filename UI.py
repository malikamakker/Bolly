from flask import Flask, render_template, request, json, session, url_for, redirect, flash
#from passlib.hash import sha256_crypt
import time
import datetime
import word_cloud
import trend1
import cluster_predict
from pathlib import Path
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60
#import MySQLdb

@app.route("/trends", methods = ['POST', 'GET'])
def trends():
        return render_template("catalog.html")

@app.route("/script", methods = ['POST', 'GET'])
def character_sketch():

        if request.method == 'POST' :
                
                if 'script' in request.form:
                        script_text = str(request.form['script'])
                        return_list = word_cloud.word_cloud(script_text)
                        return render_template("character_sketch.html", item = return_list)
    
        return render_template("twitter.html")

@app.route("/climax", methods = ['POST', 'GET'])
def climax_prediction():

        if request.method == 'POST' :
                
                if 'trailer' in request.form:
                        script_text = str(request.form['trailer'])
                        trend1.plot_climax(script_text)
                        return render_template("climax_results.html")
    
        return render_template("climax.html")

@app.route("/genre", methods = ['POST', 'GET'])
def genre_prediction():

        if request.method == 'POST' :
                
                if 'image' in request.form:
                        script_text = str(request.form['image'])
                        print(script_text)
                        text = cluster_predict.getGenre(script_text)
                        print(text)
                        return render_template("genre_results.html", text = text)
    
        return render_template("genre.html")

                         
if __name__ == "__main__":
    app.run(debug = False)
