# import required modules

import MySQLdb
import shlex
import subprocess

# Variables
store_tweets = []
result = []
array_val = ['#facts', '#food', '#google', '#html5', '#apple', '#io13']

# def show tweets

def get_tweets():
	global store_tweets
	db_con = MySQLdb.connect("127.0.0.1", "root", "root", "PyTwit")
# creating cursor to read data
	cursor = db_con.cursor()
	cursor.execute("select * from Tweets")
	results = cursor.fetchall()
	for row in results:
		store_tweets.append(row[2])
	return store_tweets

def show_tweets():
	global  tweet
	for	twit in tweet:	
		tweet_results.append(senti_strength(twit))
	print tweet_results	



def senti_strength(data):
#open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar SentiStrength.jar stdin sentidata SentiStrength_Data/"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
#communicate via stdin the string to be rated. Note that all spaces are replaced with +
    stdout_text, stderr_text = p.communicate(data.replace(" ","+"))
      
#remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
    stdout_text = stdout_text.rstrip().replace("\t","")
    
    return stdout_text
    

def defineR():
	global tweet
	for i in xrange(0, 6):
		result.append([])
		for tweets in tweet:
			if any(word in tweets for word in array_val):	
				result[i].insert(i, 1)
			else:
				result[i].insert(i, 0)
	
	print result
	
	
	


tweet = get_tweets();
defineR()
