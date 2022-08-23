#!/usr/bin/python
import re
import tweepy
import gpt_2_simple as gpt2
import os
import requests
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Keys
consumer_key = 'w8Eab6JPxsWnEXe52GNmjwyc6'
consumer_secret = '6qG541Hymq05uk12tdD9E6u0RzMs9FF7962cqxaiJHnuM5YliZ'
access_token = '1221871418817830912-jlSxLkCrFePE1qe7cpppe546Wq9Ali'
access_token_secret = 'SSkQKYVNfseAgTd8ePigV6tidh32YAEfSYuEhqOvOfZm0'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
def get_tweets(api, username, amt, txtfile, return_id):
        print("Getting Tweets from @" + username)
        end = False
        page = 1
        count = 0
        coumt_temp = 0
        file_tweets = open(txtfile, "a")
        while True:
                tweets = api.user_timeline(screen_name=username, page = page, tweet_mode = 'extended')
                for tweet in tweets:
                        if (count <= amt):
                                if(not tweet.retweeted) and ('RT @' not in tweet.full_text):
                                        file_tweets = open(txtfile, "ab")
                                        #Tweet is encoded in unicode-8
                                        full_tweet = tweet.full_text.encode('UTF-8')
                                        clean_tweet = re.sub(r"http\S+", "", full_tweet.decode('UTF-8'))
                                        clean_tweet = clean_tweet.encode('UTF-8')
                                        file_tweets.write(clean_tweet)
                                        file_tweets.close()
                                        #Adds newline
                                        file_tweets = open(txtfile, "a")
                                        if (return_id == True):
                                                file_tweets.write("idnum=" + str(tweet.id))
                                        file_tweets.write("\n")
                                        file_tweets.close()
                                        #print(count)
                                        count+=1
                                        count_temp = 0
                                        '''
                                        #ID of Tweets
                                        id_tweets = open(idfile, "a")
                                        id_tweets.write(str(tweet.id))
                                        id_tweets.write("\n")
                                        id_tweets.close()
                                        '''

                        else:
                                end = True
                                return
                if not end:
                        if (count_temp >= 2):
                                end = True
                                return
                                #print("stuck")
                        else:
                                count_temp += 1
                                #print("PAGE TURNED")
                                page+=1

#txtfile is the text file to be trained on
def model_train(txtfile, steps):
        while not os.path.exists(txtfile):
                time.sleep(1)
        if os.path.isfile(txtfile):
                model_name = "124M"
                if not os.path.isdir(os.path.join("models", model_name)):
                    print(f"Downloading {model_name} model...")
                    gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/
                file_name = txtfile
                sess = gpt2.start_tf_sess()
                gpt2.finetune(sess,
                              file_name,
                              model_name=model_name,
                              steps=steps)   # steps is max number of training steps
                gpt2.reset_session(sess)
        else:
                raise ValueError("%s there is no file" % txtfile)

def vader_analysis_full_text(txtfile):
        analyzer = SentimentIntensityAnalyzer()

        file = open(txtfile, "r").read()
        file.decode("UTF-8")
        file.encode("ascii", "ignore")
        vs = analyzer.polarity_scores(file)
        print(vs)

def vader_tweet_analysis(txtfile):
        analyzer = SentimentIntensityAnalyzer()
        sess = gpt2.start_tf_sess()
        model_name = "124M"
        gpt2.load_gpt2(sess, model_name=model_name)

        with open(txtfile, "r") as f:
                for line in f.read().split('\n'):
                        name = ""
                        tweet = ""
                        if 'Rufus T. Firefly' in line:
                                name = 'Rufus T. Firefly'
                        elif 'Freedonia' in line:
                                name = 'Freedonia'
                        elif 'Sylvania' in line:
                                name = 'Sylvania'
                        elif 'Ambassador Trentino' in line:
                                name = 'Ambassador Trentino'
                        vs = analyzer.polarity_scores(line)
                        compound_freedonia = vs['compound']
                        if (compound_freedonia >= 0.05 and name == 'Sylvania'): #positive
                                tweet = (gpt2.generate(sess, model_name= model_name, length=20, nsamples=1, batch_size=1, prefix="I agree, " + name, return_as_list = True))
                                compound_tweet = analyzer.polarity_scores(tweet[0])
                                while (compound_tweet['compound'] < 0.5):
                                        tweet = (gpt2.generate(sess, model_name=model_name, length=20, nsamples=1,
                                                               batch_size=1, prefix="I agree, " + name,
                                                               return_as_list=True))
                                        compound_tweet = analyzer.polarity_scores(tweet[0])
                        elif (compound_freedonia <= -0.05 and name == 'Sylvania'):
                                tweet = (gpt2.generate(sess, model_name=model_name, length=20, nsamples=1, batch_size=1, prefix="I disagree, " + name, return_as_list = True))
                                compound_tweet = analyzer.polarity_scores(tweet[0])
                                while (compound_tweet['compound'] > -0.5):
                                        tweet = (gpt2.generate(sess, model_name=model_name, length=20, nsamples=1,
                                                               batch_size=1, prefix="I disagree, " + name,
                                                               return_as_list=True))
                                        compound_tweet = analyzer.polarity_scores(tweet[0])
                        elif (compound_freedonia >= 0.05 and name == 'Ambassador Trentino'): #positive
                                tweet = (gpt2.generate(sess, model_name= model_name, length=20, nsamples=1, batch_size=1, prefix="I agree, " + name, return_as_list = True))
                                compound_tweet = analyzer.polarity_scores(tweet[0])
                                while (compound_tweet['compound'] < 0.5):
                                        tweet = (gpt2.generate(sess, model_name=model_name, length=20, nsamples=1,
                                                               batch_size=1, prefix="I agree, " + name,
                                                               return_as_list=True))
                                        compound_tweet = analyzer.polarity_scores(tweet[0])
                        elif (compound_freedonia <= -0.05 and name == 'Ambassador Trentino'):
                                tweet = (gpt2.generate(sess, model_name=model_name, length=20, nsamples=1, batch_size=1, prefix="I disagree, " + name, return_as_list = True))
                                compound_tweet = analyzer.polarity_scores(tweet[0])
                                while (compound_tweet['compound'] > -0.5):
                                        tweet = (gpt2.generate(sess, model_name=model_name, length=20, nsamples=1,
                                                               batch_size=1, prefix="I disagree, " + name,
                                                               return_as_list=True))
                                        compound_tweet = analyzer.polarity_scores(tweet[0])
                        elif (compound_freedonia >= 0.05 and name == 'Freedonia'): #positive
                                tweet = (gpt2.generate(sess, model_name= model_name, length=20, nsamples=1, batch_size=1, prefix="I disagree, " + name, return_as_list = True))
                                compound_tweet = analyzer.polarity_scores(tweet[0])
                                while (compound_tweet['compound'] > -0.5):
                                        tweet = (gpt2.generate(sess, model_name=model_name, length=20, nsamples=1,
                                                               batch_size=1, prefix="I disagree, " + name,
                                                               return_as_list=True))
                                        compound_tweet = analyzer.polarity_scores(tweet[0])
                        elif (compound_freedonia <= -0.05 and name == 'Freedonia'):
                                tweet = (gpt2.generate(sess, model_name=model_name, length=20, nsamples=1, batch_size=1, prefix="I agree, " + name, return_as_list = True))
                                compound_tweet = analyzer.polarity_scores(tweet[0])
                                while (compound_tweet['compound'] < 0.5):
                                        tweet = (gpt2.generate(sess, model_name=model_name, length=20, nsamples=1,
                                                               batch_size=1, prefix="I agree, " + name,
                                                               return_as_list=True))
                                        compound_tweet = analyzer.polarity_scores(tweet[0])
                        elif (compound_freedonia >= 0.05 and name == 'Rufus T. Firefly'): #positive
                                tweet = (gpt2.generate(sess, model_name= model_name, length=20, nsamples=1, batch_size=1, prefix="I disagree, " + name, return_as_list = True))
                                compound_tweet = analyzer.polarity_scores(tweet[0])
                                while (compound_tweet['compound'] > -0.5):
                                        tweet = (gpt2.generate(sess, model_name=model_name, length=20, nsamples=1,
                                                               batch_size=1, prefix="I disagree, " + name,
                                                               return_as_list=True))
                                        compound_tweet = analyzer.polarity_scores(tweet[0])
                        elif (compound_freedonia <= -0.05 and name == 'Rufus T. Firefly'):
                                tweet = (gpt2.generate(sess, model_name=model_name, length=20, nsamples=1, batch_size=1, prefix="I agree, " + name, return_as_list = True))
                                compound_tweet = analyzer.polarity_scores(tweet[0])
                                while (compound_tweet['compound'] < 0.5):
                                        tweet = (gpt2.generate(sess, model_name=model_name, length=20, nsamples=1,
                                                               batch_size=1, prefix="I agree, " + name,
                                                               return_as_list=True))
                                        compound_tweet = analyzer.polarity_scores(tweet[0])
                        id = line.partition('idnum=')[2]
                        #print(id)
                        #Posts Status Replies
                        api.update_status(tweet[0], in_reply_to_status_id = id)
                        print("Posted Tweet responding to tweetid:" + id)
                        #print(name)
                        #print(compound_freedonia)
                        #compound_tweet = analyzer.polarity_scores(tweet[0])
                        #print(compound_tweet)

if __name__ == '__main__':
        #TO_CHANGE NUMBER OF TWEET GRABS, replace the x in get_tweets(api, "name", x, "file", boolean) with the number of tweets
        get_tweets(api, "BernieSanders", 1000, "practice_tweets.txt", False)
        get_tweets(api, "FreedoniaNews", 10, "freedonia_tweets.txt", True)
        #TO CHANGE STEPS, replace the x in function model_train("file", x) with the number of training steps
        model_train("practice_tweets.txt", 1)
        vader_tweet_analysis("freedonia_tweets.txt")