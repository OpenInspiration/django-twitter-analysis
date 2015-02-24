# Import Required Modules
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render

import cmath
import MySQLdb
import random
import numpy
#from testwithpython import RateSentiment


	# Required Module for SentiStrength Analysis
# Global Variables

tweets = []

social_matrix = []
social_matrix_build = []

articles = ['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','was','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your', ":):):)", "nomore", ":)", ":):)", "<3", "...<3", "!", ":-(", 'gonna', 'give', 'others', '#facts', "io13", '#html5', '#google', '#apple', '#share', '#data', '#tweets', '#help', 'let', 'out', ":", 'write', 'wrote']

hashtags = ['#facts', '#food', '#google', '#html5', '#apple', '#io13']

loca = 0
# Functions and Definitions

def Output(request):
	sc = social_context()
	scm = social_context_matrix()
	# test = user_matrix_social()
	users_name = Retrive_Users()
	lm = location_matrix()
	return render(request, 'test.html', {'sc': social_context, 'scm':social_context_matrix, 'users_name' : users_name, 'hashtags': hashtags, 'lomat': location_matrix})

	
def social_context_matrix():
	tweets = Retrive_Tweets()
	for tweet in tweets:
		social_matrix.append([])
		for hashtag in hashtags:
			length = len(social_matrix) - 1
			if tweet.find(hashtag) != -1:
				social_matrix[length].append(1)
			else:
				social_matrix[length].append(-1)
	return social_matrix
	

def social_context():
	social_matrix_build = []
	db_con = MySQLdb.connect("127.0.0.1", "root", "root", "PyTwit")
			# creating cursor to read data
	cursor = db_con.cursor()
	cursor.execute("select * from friends_list")
	results = cursor.fetchall()
	cursor.execute("select * from sample_tweets")
	res = cursor.fetchall()
	for rows in res:
		social_matrix_build.append([])
		length = len(social_matrix_build) - 1
		for row in results:
			user1 = row[0]
			user2 = row[1]
			val = int(row[2])		
			if rows[1] == user1:
				social_matrix_build[length].append(val)
	return social_matrix_build						


def user_opinion_similarity(request):
	v1, v2, v3 = 0, 0, 0
	user1_m = user_matrix_social(request.GET['user1'])
	user2_m = user_matrix_social(request.GET['user2'])
	for i in xrange(0, len(user1_m)):
		for k in xrange(0, len(hashtags)):
			v1 += user1_m[i][k] * user2_m[i][k]
	for i in xrange(0, len(user1_m)):
		for k in xrange(0, len(hashtags)):
			v2 += (user1_m[i][k] ** 2)
	v2 = cmath.sqrt(v2)
	for i in xrange(0, len(user2_m)):
		for k in xrange(0, len(hashtags)):
			v3 += (user2_m[i][k] ** 2)
	v3 = cmath.sqrt(v2)
	uopinions =  (v1 / v2 * v3).real
	return render(request, 'opinionsimilarity.html', {'user1': request.GET['user1'], 'user2' : request.GET['user2'], 'user1_m': user1_m, 'user2_m': user2_m,  'opinion' : uopinions})
	#return HttpResponse(user1_m)


def topic_opinion_similarity(request):
	#tweets = Retrive_Tweets()
	tweet1 = []
	tweet2 = []
	topic_matrix1, topic_matrix2 = [], []
	v1, v2, v3 = 0, 0, 0
	global loca
	user1 = request.GET['user1']
	user2 = request.GET['user2']
	tweets1 = topic_tweet(user1)
	tweets2 = topic_tweet(user2)
	tweet1 = remove_stop_words(tweets1)
	tweet2 = remove_stop_words(tweets2)
	for hashtag in hashtags:
		topic_matrix1.append([])
		length = len(topic_matrix1) - 1
		for tweet in tweet1:
			if tweets1.find(tweet) != -1:
				topic_matrix1[length].append(1)
			else:
				topic_matrix1[length].append(0)
	
	length = 0
	for hashtag in hashtags:
		topic_matrix2.append([])
		length = len(topic_matrix2) - 1
		for tweet in tweet2:
			if tweets2.find(tweet) != -1:
				topic_matrix2[length].append(1)
			else:
				topic_matrix2[length].append(0)

	for i in xrange(0, len(topic_matrix1)):
		for k in xrange(0, len(hashtags)):
			v1 += (topic_matrix1[i][k])
	for i in xrange(0, len(topic_matrix1)):
		for k in xrange(0, len(hashtags)):
			v2 += (topic_matrix1[i][k] * 2)
	for i in xrange(0, len(topic_matrix2)):
		for k in xrange(0, len(hashtags)):
			v3 += (topic_matrix2[i][k] * 2)

	tos = (v1 / cmath.sqrt(v2 * v3)).real
	return render(request, 'topicopinion.html', {'tweet1' : user1, 'tweet2': user2, 'top1': topic_matrix1, 'top2':topic_matrix2, 'tos' : tos})


def forchart(request):
	tweet1 = []
	tweet2 = []
	topic_matrix1, topic_matrix2 = [], []
	v1, v2, v3 = 0, 0, 0
	global loca
	user1 = request.GET['user_1']
	user2 = request.GET['user_2']
	tweets1 = topic_tweet(user1)
	tweets2 = topic_tweet(user2)
	tweet1 = remove_stop_words(tweets1)
	tweet2 = remove_stop_words(tweets2)
	for hashtag in hashtags:
		topic_matrix1.append([])
		length = len(topic_matrix1) - 1
		for tweet in tweet1:
			if tweets1.find(tweet) != -1:
				topic_matrix1[length].append(1)
			else:
				topic_matrix1[length].append(0)
	
	length = 0
	for hashtag in hashtags:
		topic_matrix2.append([])
		length = len(topic_matrix2) - 1
		for tweet in tweet2:
			if tweets2.find(tweet) != -1:
				topic_matrix2[length].append(1)
			else:
				topic_matrix2[length].append(0)

	for i in xrange(0, len(topic_matrix1)):
		for k in xrange(0, len(hashtags)):
			v1 += (topic_matrix1[i][k])
	for i in xrange(0, len(topic_matrix1)):
		for k in xrange(0, len(hashtags)):
			v2 += (topic_matrix1[i][k] * 2)
	#for i in xrange(0, len(topic_matrix2)):
	#	for k in xrange(0, len(hashtags)):
	#		v3 += (topic_matrix2[i][k])

	tos = (v1 / cmath.sqrt(v2)).real	
	
	l, v2, v3 = 0, 0, 0
	alpha = random.uniform(0.01, 0.04)
	beta = random.uniform(-0.5, -0)
	user1_tweet = topic_tweet(user1)
	user2_tweet = topic_tweet(user2)
	user1_location = get_location(user1)
	user2_location = get_location(user2)
	lo = get_location('')
	lo_mat = location_matrix()
	for i in xrange(0, len(lo_mat)):
		for k in xrange(0, len(lo)):
			v2 += (lo_mat[i][k])
	for i in xrange(0, len(lo_mat)):
		for k in xrange(0, len(lo)):
			v3 += (lo_mat[i][k])
		
	l = (cmath.sqrt(v2).real * v3 * alpha) / 10
	
	v1, v2, v3 = 0, 0, 0
	user1_m = user_matrix_social(user1)
	user2_m = user_matrix_social(user2)
	for i in xrange(0, len(user1_m)):
		for k in xrange(0, len(hashtags)):
			v1 += user1_m[i][k] * user2_m[i][k]
	for i in xrange(0, len(user1_m)):
		for k in xrange(0, len(hashtags)):
			v2 += (user1_m[i][k] ** 2)
	v2 = cmath.sqrt(v2)
	for i in xrange(0, len(user2_m)):
		for k in xrange(0, len(hashtags)):
			v3 += (user2_m[i][k] ** 2)
	v3 = cmath.sqrt(v2)
	uopinions =  (v1 / v2 * v3).real
	ur = "http://www.chartgo.com/create.do?chart=bar&dimension=3d&width=300&height=400&orientation=vertical&title=Location+similarity&subtitle=locationbased&xtitle=user1&ytitle=user2&source=&fonttypetitle=bold&fonttypelabel=normal&labelorientation=horizontal&chrtbkgndcolor=gradientblue&max_yaxis=&transparency=1&labels=1&min_yaxis=&roundedge=1&shadow=1&border=1&xaxis1=t1%0D%0As1%0D%0A1l1&yaxis1=%0D%0A"+ str(tos) +"%0D%0A"+ str(uopinions) +"%0D%0A"+ str(l) +"&group1=Group+1&add=&rem=&from=generaljsp&lang=en"
	temp_values = {'t1': tos, 'l1':l, 's1': uopinions, 'url':ur, 'user_1': user1, 'user_2': user2 }

	return render(request, 'chartanalysis.html', temp_values)
	
	
def location_context(request):
	v, v2, v3 = 0, 0, 0
	alpha = random.uniform(0.01, 0.04)
	beta = random.uniform(-0.5, -0)
	user1 = request.GET['l1']
	user2 = request.GET['l2']
	user1_tweet = topic_tweet(user1)
	user2_tweet = topic_tweet(user2)
	user1_location = get_location(user1)
#	user1_location = matrix_factorization(user1_location)
	user2_location = get_location(user2)
#	user2_location = matrix_factorization(user2_location)
	lo = get_location('')
	lo_mat = location_matrix()
	for i in xrange(0, len(lo_mat)):
		for k in xrange(0, len(lo)):
			v2 += (lo_mat[i][k])
	for i in xrange(0, len(lo_mat)):
		for k in xrange(0, len(lo)):
			v3 += (lo_mat[i][k])
		
	v = (cmath.sqrt(v2).real * v3 * alpha) / 10
	
	Temp_values = { 'user1': user1,
					'user2': user2,
					'l1': user1_location,
					'l2': user2_location,
					'lores' : v
					}	
	return render(request, 'location.html', Temp_values)




def user_matrix_social(user):
	user_matrix = []
	db_con = MySQLdb.connect("127.0.0.1", "root", "root", "PyTwit")
			# creating cursor to read data
	cursor = db_con.cursor()
	cursor.execute("select * from sample_tweets where username= %s", user)
	results = cursor.fetchall()
	for row in results:
		user_matrix.append([])
		length = len(user_matrix) - 1
		for hashtag in hashtags:
			if row[2].find(hashtag) != -1:
				user_matrix[length].append(1)
			else:
				user_matrix[length].append(-1)
	return user_matrix

def Tryone():
	pass

def Retrive_Tweets(user=None):
	db_con = MySQLdb.connect("127.0.0.1", "root", "root", "PyTwit")
			# creating cursor to read data
	cursor = db_con.cursor()
	cursor.execute("select * from sample_tweets")
	results = cursor.fetchall()
	for row in results:
		tweets.append(row[2])
	cursor.close()
	return tweets

def Retrive_Users():
	users = []
	db_con = MySQLdb.connect("127.0.0.1", "root", "root", "PyTwit")
	# creating cursor to read data
	cursor = db_con.cursor()
	cursor.execute("select * from sample_tweets")
	results = cursor.fetchall()
	for row in results:
		users.append(row[1])
	return users
	
def remove_stop_words(wordlist, stopwords=articles):
    # ask for sentence if wordlist is empty
    sentence = wordlist
    wordlist = sentence.split()
    marked = []
    for t in wordlist:
        if t.lower() in stopwords:
            marked.append('*')
        else:
            marked.append(t)
    return marked

def topic_tweet(user):
	db_con = MySQLdb.connect("127.0.0.1", "root", "root", "PyTwit")
	# creating cursor to read data
	cursor = db_con.cursor()
	cursor.execute("select * from sample_tweets where username=%s", user)
	results = cursor.fetchall()
	for row in results:
		users = row[2]
	return users
	
def get_location(user):
	locations = []	
	db_con = MySQLdb.connect("127.0.0.1", "root", "root", "PyTwit")
	# creating cursor to read data
	cursor = db_con.cursor()
	if user == "":
		cursor.execute("select * from sample_tweets ")
		results = cursor.fetchall()
		for row in results:
			locations.append(row[3])
		return locations
	else:
		cursor.execute("select * from sample_tweets where username=%s", user)
		results = cursor.fetchall()
		for row in results:
			location = row[3]
		return location

def location_matrix():
	location_mat = []
	db_con = MySQLdb.connect("127.0.0.1", "root", "root", "PyTwit")
	# creating cursor to read data
	cursor = db_con.cursor()
	cursor.execute("select * from sample_tweets")
	results = cursor.fetchall()
	for row in results:
		location_mat.append([])
		length = len(location_mat) - 1
		locations = get_location('')
		for lo in locations:
			if row[3] == lo:
				location_mat[length].append(1)
			else:
				location_mat[length].append(0)
	return location_mat


	