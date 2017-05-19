
# collect.py


from TwitterAPI import TwitterAPI
import re
import sys
import time
import os
tweet_list = []
donald = []

# twitter keys

consumer_key = 'xxxxxxxxxxxxxxxxxxx'
consumer_secret = 'xxxxxxxxxxxxxxxxxxxx'
access_token_key = 'xxxxxxxxxxxxxxxxxxxxx'
access_token_secret = 'xxxxxxxxxxxxxxxxxxxxx'



def get_twitter():
    return TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)



def robust_request(twitter, resource, params, max_tries=5):
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)


def get_tweets(twitter):

    c = 0


    nd=open("nodes.txt","w")
    tw = open("tweets.txt","w")
    while True and c<=200:

        r = robust_request(twitter,'statuses/filter', {'track':'realdonaldtrump','language':'en'})
        for item in r:

            if item['user']['friends_count'] >= 1000:
                if len(donald)<=28 and item['user']['screen_name'] not in donald:
                    donald.append(item['user']['screen_name'].strip())
                    nd.write(item['user']['screen_name'].strip())
                    nd.write("\n")
            
            tweet = item['text'].lower()
            if not tweet.startswith('rt') and tweet not in tweet_list:
                tweet = re.sub('@[^\s]+','',tweet)
                tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
                tweet = re.sub('[0-9]+', " ",tweet)
                tweet = re.sub('[\s]+'," ", tweet)
                tweet = re.sub('http\S+', " ", tweet)
                tweet = re.sub('@\S+', "", tweet)
                tweet = re.sub('\W+', " ", tweet)
                tweet = tweet.strip()

                tweet_list.append(tweet)
                tw.write(tweet)
                tw.write("\n")

                c +=1
                if c >= 200:
                    break
    nd.close()
    tw.close()



def main():
    twitter = get_twitter()
    get_tweets(twitter)
    ow = open("output.txt","a")
    ow.write("Number of users collected:" + str(len(donald)))
    ow.write("\n")
    ow.write("Number of messages collected:" + str(len(tweet_list)))
    ow.write("\n")

    ow.close()



if __name__ == '__main__':
    main()

