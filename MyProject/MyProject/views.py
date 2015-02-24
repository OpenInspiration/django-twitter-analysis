# importing required modules

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render

import numpy
import MySQLdb

# global variables

store_tweets = []
array_val = ['#facts', '#food', '#google', '#html5', '#apple', '#io13']
result = []


# Database Connection

def conn():
	db_con = MySQLdb.connect("127.0.0.1", "root", "root", "PyTwit")
# creating cursor to read data
	cursor = db_con.cursor()
	cursor.execute("select * from sample_tweets")
	results = cursor.fetchall()
	for row in results:
		store_tweets.append(row[2])
	return store_tweets

# TopicR relation

def TopicR():
	store_tweets = conn()
	for tweet in store_tweets:
		result.append([])
		for hash in array_val:
			length = len(result) - 1
			if tweet.find(hash) != -1:
				result[length].append(1)
			else:
				result[length].append(0)
	return result


# Matrix Factorization


def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.05):
    Q = Q.T
    print Q
    for step in xrange(steps):
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = numpy.dot(P,Q)
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in xrange(K):
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
        if e < 0.001:
            break
    return P, Q.T

	
res = TopicR()
	
R = numpy.array(res)
N = len(R)
M = len(R[0])
K = 2

P = numpy.random.rand(N,K)
Q = numpy.random.rand(M,K)
nP, nQ = matrix_factorization(R, P, Q, K)
nR = numpy.dot(nP, nQ.T)

# Connection Establishment 
	
def connection_estab(request):
	return render(request, 'index.html', {'TopicR': res, 'nP' : nP, 'nQ' : nQ })
	
	
	