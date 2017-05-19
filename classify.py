# classify

import json
import re
import sys
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


def generateStopWordList():

    stopWords_dataset = "stopwords.txt"

    stopWords = []

    try:
        fp = open(stopWords_dataset, 'r')
        line = fp.readline()
        while line:
            word = line.strip()
            stopWords.append(word)
            line = fp.readline()
        fp.close()
    except:
        print("ERROR: Opening File")

    return stopWords

# processing of the data i.e. cleaning

def preprocessing(dataSet):

    processed_data = []

    stopWords = generateStopWordList()

    for tweet in dataSet:

        temp_tweet = tweet

        tweet = re.sub('@[^\s]+','',tweet).lower()
        tweet.replace(temp_tweet, tweet)

        tweet = re.sub('[\s]+',' ', tweet)
        tweet.replace(temp_tweet,tweet)

        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

        tweet = re.sub('[0-9]+', "",tweet)
        tweet.replace(temp_tweet,tweet)

        for sw in stopWords:
            if sw in tweet:
                tweet = re.sub(r'\b' + sw + r'\b'+" ","",tweet)

        tweet.replace(temp_tweet, tweet)

        tweet = re.sub('[^a-zA-z ]',"",tweet)
        tweet.replace(temp_tweet,tweet)

        tweet = re.sub('[\s]+',' ', tweet)
        tweet.replace(temp_tweet,tweet)
        
        tweet = tweet.strip()
        


        processed_data.append(tweet)

    return processed_data


positive_data = open("positive.txt").readlines()
positive_data = preprocessing(positive_data)

negative_data = open("negative.txt").readlines()
negative_data = preprocessing(negative_data)

test_data = open("tweets.txt").readlines()
test_data = preprocessing(test_data)

train_data = positive_data + negative_data
train_label = [1]*len(positive_data)+[0]*len(negative_data)


vectorizer = CountVectorizer(min_df=1, stop_words='english')
train_vector = vectorizer.fit_transform(train_data)
# print("number of instances and number of features are : ",X.toarray().shape[0],X.toarray().shape[1])
# features = vectorizer.get_feature_names()
# print(len(features))
test_vector = vectorizer.transform(test_data)



lr = LogisticRegression()
clfr = lr.fit(train_vector,train_label)
pred = lr.predict(test_vector)
print(pred)



pw = open("prediction.txt","w")

for i in pred:
    pw.write(str(i))
    pw.write("\n")
pw.close()


pred1 = pred.tolist()


ow = open("output.txt","a")
ow.write("Number of instances for positive class :  " + str(sum(pred)) )
ow.write("\n")
ow.write("Number of instances for negative class :  " + str(len(pred)-sum(pred)))
ow.write("\n")
ow.write("One example from positive class :  " + test_data[pred1.index(1)])
ow.write("\n")
ow.write("One example from negative class :  " + test_data[pred1.index(0)])
ow.write("\n")

ow.close()


