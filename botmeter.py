#!/usr/bin/python

import botometer

rapidapi_key = "68db7803b4msha2d13c663f3d76ep107d5cjsna1fd6969eb59" # now it's called rapidapi key
twitter_app_auth = {
    'consumer_key': 'w8Eab6JPxsWnEXe52GNmjwyc6',
    'consumer_secret': '6qG541Hymq05uk12tdD9E6u0RzMs9FF7962cqxaiJHnuM5YliZ',
    'access_token': '1221871418817830912-jlSxLkCrFePE1qe7cpppe546Wq9Ali',
    'access_token_secret': 'SSkQKYVNfseAgTd8ePigV6tidh32YAEfSYuEhqOvOfZm0',
  }

bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

# Check a single account by screen name
def check_user(user):
    result = bom.check_account(user)
    print("Total Results: ", result['display_scores'])
    english = result['display_scores']['english']
    universal = result['display_scores']['universal']
    total = (english + universal)/2
    if (total <= 2):
        print("Account is not a bot")
    elif (total >= 3):
        print("Account is a bot")
    else:
        print("Account is inconclusive")

if __name__ == '__main__':
    #TO CHANGE USER, replace "@name" in check_user("@name") with a username with the "@" before it
    check_user("@BotFreedonia")