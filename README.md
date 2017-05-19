# Real-Time-Presidential-Vote-Prediction

## For collecting Real Time tweets on Donald Trump we have used the Twitter Streaming API.

This program has four python files namely: 
	- collect
	- cluster
	- classify
	- summarize.


## The functionality of each of the sections of the program has been defined below:

### collect.py : 
	- This file extracts the tweets from twitter and save the tweets in tweets.txt file
	and also save the top users in nodes.txt

### cluster.py : 
	- This file fetch the friends of all the users we saved from the previous step and
	find similarity between these using their friends. Then we find the weak edges based 
	on the similarities and keep on deleting the edges till we get more than one cluster.

### classify.py : 
	- This file uses the tweets we previously saved and using the train data that are stored in positive.txt 
	and negative.txt. We use logistic regression as our prediction model and we predict the label for our test data.
	1 means positive tweet and 0 means negative tweet.

### summarize.py : 
	- This file prints out certain details.


### The main aim of this program is to detect the sensitivity of tweets and making clusters according to the community with different relations as here it is determined by the commanality between them using their friends which affects the sentiments of the voters and in turn can be their voting decisions.
