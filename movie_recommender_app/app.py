import os
import pickle

from flask import Flask, render_template, request, session, url_for, redirect
import numpy

with open(r'pkl_objects/corr_mat.pickle', 'rb') as file:
	corr_mat = pickle.load(file)

with open(r'pkl_objects/movie_names.pickle', 'rb') as file:
	movie_names = pickle.load(file)

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

movies_list = list(movie_names)
base_url = 'https://www.themoviedb.org'  # url to scrape movie details

@app.route('/')
def index():
	return render_template('starter.html')


if __name__ == '__main__':
	app.run(debug=True)
	# app.run(debug=False)