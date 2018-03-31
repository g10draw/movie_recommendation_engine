import os
import pickle
import urllib

import numpy
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, session, url_for, redirect

with open(r'pkl_objects/corr_mat.pickle', 'rb') as f:
	corr_mat = pickle.load(f)

with open(r'pkl_objects/movie_names.pickle', 'rb') as f:
	movie_names = pickle.load(f)

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

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
	picked_movies = request.form.getlist('movie_data')
	corr_mats = []
	for movie in picked_movies:
		corr_mats.append(corr_mat[int(movie)])
	recommendations = []
	for cm in corr_mats:
		recommendations.append(list(movie_names[(cm < 1.0) & (cm > 0.9)]))
	recommendations = sum(recommendations, [])
	movie_details = [movie_data_scraper(movie) for movie in recommendations]
	return render_template('recommendations.html', movies = movie_details)


def movie_data_scraper(movie_name):
	movie_name = movie_name[:movie_name.find('(')-1].replace(':', '')  # remove (year) part
	url = base_url+'/search?query='+movie_name.replace(' ', '+')

	html_data = urllib.request.urlopen(url)
	soup = BeautifulSoup(html_data, 'html.parser')
	next_url = base_url+soup.find('p', attrs={'class': 'view_more'}).a['href']

	html_data = urllib.request.urlopen(next_url)
	soup = BeautifulSoup(html_data, 'html.parser')

	title = soup.find('div', attrs={'class':'title'}).text.replace('\n', '')
	img_src = soup.find('img', attrs={'class':'poster'})['src']
	overview = soup.find('div', attrs={'class':'overview'}).p.text
	return [title, img_src, overview]
